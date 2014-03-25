import urllib2
from bs4 import BeautifulSoup
import re

#read in a web page
def get_response():
   url_define = "https://stations.fcc.gov/station-profile/wral-tv/rss/feed-/political_file/2014"
   response = urllib2.urlopen("https://stations.fcc.gov/station-profile/wral-tv/rss/feed-/political_file/2014")
   html = response.read()
   file_loc =[]
   
   #print html

   soup = BeautifulSoup(html)
   #print(soup.prettify())

   #grab URLs for PDFs, starting with "collect"
   #have to deal with some weird RSS parsing, which is messing me up
   #do I need to search for repeated strings? with re: Political File.*Political File
   #should probably build in a test for this if it's widespread
   for link in soup.find_all('a', href=re.compile("collect")):
   	unclean_url = link.get('href')
   	clean_url = re.sub(r'Political File.*Political File','Political File',unclean_url)
   	file_loc.append(clean_url)

   for l in file_loc:
   	print l

if __name__ == '__main__':
	get_response()
	print 'Done'