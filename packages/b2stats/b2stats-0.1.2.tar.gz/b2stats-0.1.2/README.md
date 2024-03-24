# Backblaze B2 Stats
This repository contains code to extract some stats relating to B2 object storage from the Backblaze web interface, which are currently not exposed by the API.

## Usage
```python
import b2stats

b2 = b2stats.B2Stats("your@email.com", password="password123", totp="totp_key_if_enabled")

# Get bucket stats (eg. size, file count)
bucket_stats = b2.get_buckets()

# Get account usage & caps (overall storage, daily bandwidth / API calls)
caps = b2.get_caps() 
```