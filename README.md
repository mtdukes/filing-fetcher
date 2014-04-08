# Filing fetcher
Automatically (eventually) grab FCC political filings from a defined list of stations.

Eventually, this might look something like:

1. Feed in station list
2. Start app
3. Monitor station political filing RSS
4. Check for existing political file in storage location
5. Upload new political file to storage location
6. Upload to DocumentCloud?
7. Update log/database

Heavily influenced by great work at the Sunlight Foundation
https://github.com/sunlightlabs/fcc_political_ads/blob/develop/fcc_adtracker/scraper/fcc_scraper.py

##Example
python ../fetcher.py ../stations.csv

Enter csv, file destination and "1" flag to pass list of stations and their RSS feeds. Currently set for a scheduled run of every 60 seconds for debug purposes, but will evetually be set to run every four hours (14400 seconds).

##Debug mode

python ../fetcher.py https://stations.fcc.gov/station-profile/wral-tv/rss/feed-/political_file/2014 1 wral

Takes RSS from single stations and downloads all files. Will create a log to track downloads and will NOT download files if they've already been downloaded.

##Amazon upload
Using boto
Will currently upload to Amazon S3, provided appropriate credentials are defined in ~/.boto

python fetcher_s3.py stations.csv

Still need to:

- Figure out how to upload log.csv
- Add error checking
- Set files to public on upload

##TODO
- Set up server functionality (https://devcenter.heroku.com/articles/getting-started-with-python)
- Additional data fields in log.csv pulled from FCC file location
- Database integration
- Add DC integration
- Refactor BECAUSE I AM AWFUL AT THIS