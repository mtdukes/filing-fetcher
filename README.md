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
python fetcher.py https://stations.fcc.gov/station-profile/wral-tv/rss/feed-/political_file/2014 wral/

(Debug) Takes RSS from single stations and downloads all files. Will create a log to track downloads and will NOT download files if they've already been downloaded.

OR

python fetcher.py stations.csv wral/ 1
(Will eventually be default) enter csv, file destination and "1" flag to pass list of stations and their RSS feeds. Currently set for a scheduled run of every 60 seconds for debug purposes, but will evetually be set to run every four hours (14400 seconds).

##TODO
- Set up server functionality (where will this live?)
- Database integration
- Add DC integration
- Switch single filing entry to nondefault mode
- Refactor BECAUSE I AM AWFUL AT THIS