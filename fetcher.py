import urllib2, urllib
from bs4 import BeautifulSoup
import re
import argparse

#read in a web page and station call letters defined by users
#eventually would like to read in csv with these args predefined
def get_response(url_define, station_define):
   #url_define = "https://stations.fcc.gov/station-profile/wral-tv/rss/feed-/political_file/2014"
   #station_define = "wral"
   response = urllib2.urlopen(url_define)
   html = response.read()
   file_loc =[]

   soup = BeautifulSoup(html)

   #grab URLs for PDFs, starting with "collect"
   #have to deal with some weird RSS parsing, which is messing me up
   #do I need to search for repeated strings? with re: Political File.*Political File
   #should probably build in a test for this if it's widespread
   for link in soup.find_all('a', href=re.compile("collect")):
   	unclean_url = link.get('href')
   	clean_url = re.sub(r'Political File.*Political File','Political File',unclean_url)
   	file_loc.append(clean_url)

   for l in file_loc:
      #check for spaces and replace with "%20"
      pdf_url = urllib.quote("https://stations.fcc.gov//" + l, safe="%/:=&?~#+!$,;'@()*[]")
      pdf_file = urllib2.urlopen(pdf_url)
      #Use regex ^.*\/(.*) to grab filename
      output = open(station_define+"/"+re.findall(r'^.*\/(.*)',l)[0],'wb')
      output.write(pdf_file.read())
      output.close()
      print re.findall(r'^.*\/(.*)',l)[0]


if __name__ == '__main__':
   parser = argparse.ArgumentParser(description='Process the input')
   parser.add_argument('path',help='Enter the station rss path')
   parser.add_argument('call_sign',help='Enter the station call sign')
   args = parser.parse_args()
   get_response(args.path, args.call_sign)
   print 'Done'