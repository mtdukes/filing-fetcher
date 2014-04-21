# Filing fetcher
Automatically grab FCC political filings from a defined list of stations.

##Workflow
There are two versions of the script, one you can run locally (fetcher.py), the other you can upload onto an Amazon EC2 instance, which uploads files to Amazon S3 (fetcher_s3.py). Both essentially work the same.

1. Run script with [CSV of stations/RSS feeds](https://github.com/mtdukes/filing-fetcher/blob/master/stations.csv) as an argument
2. Script checks if files have already been downloaded
3. If not, downloads each political file at each provided RSS location
4. Creates a log (if one does not exist), and records the download time, station name and file name

Heavily influenced by great work at the [Sunlight Foundation](https://github.com/sunlightlabs/fcc_political_ads/blob/develop/fcc_adtracker/scraper/fcc_scraper.py)

##Example
Enter csv, file destination.

```
python ../fetcher.py ../stations.csv
```

##Debug mode
Takes RSS from single stations and downloads all files. Will create a log to track downloads and will NOT download files if they've already been downloaded.

```
python ../fetcher.py https://stations.fcc.gov/station-profile/wral-tv/rss/feed-/political_file/2014 1 wral
```

##Amazon upload
The server-based version of the script (fetcher_s3.py) uses [Boto](https://aws.amazon.com/sdkforpython/) to upload to Amazon S3, provided [appropriate credentials are defined](http://stackoverflow.com/questions/9197385/getting-credentials-file-in-the-boto-cfg-for-python) in ~/.boto or /etc/boto.cfg.

TK: More about how to spin up an Amazon EC2 instance here

Use SFTP client like Cyberduck to [connect to EC2](http://blog.ryanparman.com/2013/08/10/uploading-web-files-to-a-new-amazon-ec2-instance/) and upload the script.

- Hostname: {public-hostname}
- User: ec2-user
- Key: {path-to-keypair-pem}

Test the script by using Terminal of PuTTY to SSH into your EC2 instance. You'll need local access to your [keypair file](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html).

```
ssh -i {path-to-keypair-pem} ec2-user@{public-hostname}
```

Most required packages should be installed, with the exception of [BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/). Download with wget.

```
wget http://www.crummy.com/software/BeautifulSoup/bs4/download/4.3/beautifulsoup4-4.3.2.tar.gz
```

Unpack the tarball file, switch to the director and install with python.

```
tar xvf beautifulsoup4-4.3.2.tar.gz
cd beautifulsoup4-4.3.2.tar.gz
python setup.py install
```

##Set up a cron job
On your server, [use cron](https://help.ubuntu.com/community/CronHowto) to run script regularly (recommended four to six hours)

```
0 0,04,08,12,16,20 * * * python fetcher_s3.py stations.csv
```

##TODO
- Additional data fields in log.csv pulled from FCC file location
- Add DocumentCloud integration
- Database integration
- mTurk module
- Refactor???