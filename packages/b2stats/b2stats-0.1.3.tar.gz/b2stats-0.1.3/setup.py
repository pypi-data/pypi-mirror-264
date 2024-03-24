from setuptools import setup

setup(
    name='b2stats',
    version='0.1.3',
    description='Scrape Backblaze web interface for B2 bucket & caps statistics',
    url='https://github.com/matthew-kilpatrick/b2stats',
    author='Matthew Kilpatrick',
    author_email='github@matthewkilpatrick.uk',
    license='MIT',
    packages=['b2stats'],
    install_requires=[
        'bs4',
        'mintotp',
        'python-dateutil',
        'requests'
    ],
    classifiers=[],
)
