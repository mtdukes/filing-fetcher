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

OR

python fetcher.py stations.csv wral/ 1

##TODO
- Add scheduler (where will this run?)
- Error handling (MOAR)
- Checker for existing files
- Database integration
- Add DC integration
- Log creation
- Refactor BECAUSE YOU ARE AWFUL AT THIS