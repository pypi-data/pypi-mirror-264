import requests
import mintotp
from bs4 import BeautifulSoup
import dateutil.parser


class B2Stats:

    email = None
    password = None
    totp = None
    cookies = None

    # Dictionary for mapping size suffixes to bytes
    byte_suffix = {
        "bytes": 1,
        "kb": 1024,
        "mb": 1024 ** 2,
        "gb": 1024 ** 3,
        # Assuming below are true for large buckets (& that exabyte+ is not required), though am yet to reach these units
        "tb": 1024 ** 4,
        "pb": 1024 ** 5
    }

    def __init__(self, email, **kwargs):
        """

        :param email:
        :param kwargs:
        """
        self.email = email
        self.password = kwargs.get("password", None)
        self.totp = kwargs.get("totp", None)

    def __get_cookies(self):
        """
        Get authentication cookies for web interface
        :return:
        """
        if self.cookies is not None:
            return self.cookies

        email_auth = requests.post("https://api.backblazeb2.com/b2api/v1/b2_create_session", json={
            "identity": {
                "email": self.email,
                "identityType": "accountEmail"
            },
            "clientInfo": {
                "clientType": "webui",
                "deviceName": "Backblaze B2 Stats Scrape"
            }
        })

        if email_auth.status_code != 200:
            raise Exception(email_auth.json().message)

        auth = email_auth.json()

        while auth["challenge"] is not None:
            # TODO: if same challenge twice in a row, this likely means invalid creds, so fail to prevent infinite loop
            # Still another authentication process to perform, so determine what is required
            body = {
                "authToken": auth["authToken"],
                "credentials": {
                    "credentialsType": auth["challenge"]["challengeType"]
                },
                "infoRequested": ["accountProfile", "groupsApi"]
            }
            if auth["challenge"]["challengeType"] == "password":
                body["credentials"]["password"] = self.password
            elif auth["challenge"]["challengeType"] == "totp":
                body["credentials"]["code"] = mintotp.totp(self.totp)
            else:
                raise ValueError("Unrecognised authentication challenge '{}'".format(auth["challenge"]))

            auth_request = requests.post(auth["apiUrl"] + "/b2api/v1/b2_present_credentials", json=body)

            auth = auth_request.json()
            if auth_request.status_code != 200:
                raise Exception(auth["message"])

        cookie_request = requests.post("https://secure.backblaze.com/api2/bz_get_session_cookies", json={
            "accountId": auth["info"]["accountProfile"]["accountId"],
            "authToken": auth["authToken"]
        })

        self.cookies = cookie_request.cookies

        return self.cookies

    def get_buckets(self):
        """
        Get list of buckets alongside their stats (object count, size, ...)
        :return dict:
        """
        buckets_request = requests.get("https://secure.backblaze.com/b2_buckets.htm", cookies=self.__get_cookies())
        soup = BeautifulSoup(buckets_request.text, features="html.parser")
        buckets = []
        for bucket in soup.select(".b2-overview"):
            labels = [
                el.text.strip()[:-1].lower().replace(" ", "_")
                # Strip trailing ":" from key, and map to snake case labels
                for el in bucket.select(".b2-bucket-left .b2-stats-label")
            ]
            label_data = [el.text.strip() for el in bucket.select(".b2-bucket-left .b2-stats-data")]
            data = dict(zip(labels, label_data))  # Use labels as key & data as val

            # Additional processing for some keys in data dict
            # Change created date to ISO8601 format
            data["created"] = dateutil.parser.parse(data["created"]).strftime("%Y-%m-%d")

            # Change current file count to int
            data["current_files"] = int(data["current_files"].replace(",", ""))

            # Change current size to byte int
            size, unit = data["current_size"].split(" ", 1)
            size = float(
                size.replace(", ", ""))  # Though I'm not sure a comma is ever shown (as it'd just increase suffix)
            unit = unit.lower()

            data["current_size"] = int(
                size * self.byte_suffix[unit])  # Due to rounding this may be fraction of byte, so cast to int

            # Change snapshots value to int
            data["snapshots"] = int(data["snapshots"].replace(",", ""))

            # Add bucket name title to data dict
            data["bucket_name"] = bucket.select_one(".b2-bucket-bucket-name").text

            # Handle S3 endpoint being empty for old buckets / rename key to s3_endpoint for clarity
            s3_endpoint = data["endpoint"]
            del data["endpoint"]
            if s3_endpoint[0] == "-":
                s3_endpoint = None
            data["s3_endpoint"] = s3_endpoint

            # Append bucket data to list
            buckets.append(data)

        return buckets

    def get_caps(self):
        """
        Scrape B2 stats page to get information on current (daily) usage, caps, and alert settings
        :return dict:
        """
        caps_request = requests.get("https://secure.backblaze.com/b2_caps_alerts.htm", cookies=self.__get_cookies())
        soup = BeautifulSoup(caps_request.text, features="html.parser")
        caps = []
        for cap in soup.select(".b2-caps-box"):
            cap_id = cap.select_one(".b2-caps-progressbar").attrs["id"].replace("progress-wrap-", "")
            usage_percent = float(cap.select_one('.b2-caps-progressbar').attrs["data-progress-percent"])

            usage_cost = float(cap.select_one(".b2-caps-left .text_green").text.replace("$", "").replace(",", "").strip())
            cap_cost = float(cap.select_one(".b2-caps-amount").text.replace("$", "").replace(",", "").strip())

            # Substring to remove brackets
            # Also process to convert suffix to bytes if included (for storage / bw usage)
            usage_value = cap.select(".b2-caps-left .text_65grey")[-1].text.strip()[1:-1].replace(",", "")  # First text_65grey is heading
            usage_parts = usage_value.split(" ", 1)
            if len(usage_parts) == 1:
                # Is API request count
                usage_value = int(usage_value)
            else:
                # Is value with unit
                size, unit = usage_parts[0], usage_parts[1]
                size = float(size.strip())
                unit = unit.lower().strip()
                usage_value = int(size * self.byte_suffix[unit])

            cap_value = cap.select_one(".b2-caps-right .text_65grey").text.strip()[1:-1].replace(",", "")
            cap_parts = cap_value.split(" ", 1)
            if len(cap_parts) == 1:
                # Is API request count
                cap_value = int(cap_value)
            else:
                # Is value with unit
                size, unit = cap_parts[0], cap_parts[1]
                size = float(size.strip())
                unit = unit.lower().strip()
                cap_value = int(size * self.byte_suffix[unit])

            # Determine if SMS/email alert checkboxes are selected (alerts enabled)
            email_alerts = "checked" in soup.select_one("#checkbox-email-" + cap_id).attrs
            sms_alerts = "checked" in soup.select_one("#checkbox-sms-" + cap_id).attrs

            # Map class ID to a clearer label
            cap_label = {
                "storage": "storage",
                "downloadBandwidth": "bandwidth_download",
                "downloadTransactions": "transactions_class_b",
                "miscTransactions": "transactions_class_c"
            }[cap_id]

            caps.append({
                "cap": cap_label,
                "usage": {
                    "cost": usage_cost,
                    "value": usage_value,
                    "percent": usage_percent
                },
                "limit": {
                    "cost": cap_cost,
                    "value": cap_value
                },
                "alerts": {
                    "email": email_alerts,
                    "sms": sms_alerts
                }
            })

        return caps
