import urllib2, urllib
from bs4 import BeautifulSoup
import re, argparse, csv, os.path

#read in a web page and station call letters, which serves as file destination
def get_response(url_define, station_define):
   try:
      response = urllib2.urlopen(url_define)
      html = response.read()
   except:
      print 'ERROR: invalid feed url'
      return
   file_loc =[]

   soup = BeautifulSoup(html)

   #grab URLs for PDFs, starting with "collect"
   #need a test for:search for repeated strings with re: Political File.*Political File
   for link in soup.find_all('a', href=re.compile("collect")):
   	unclean_url = link.get('href')
   	clean_url = re.sub(r'Political File.*Political File','Political File',unclean_url)
   	file_loc.append(clean_url)   
   
   #loop through all the file locations and download each file to a directory
   for l in file_loc:
      try:
         #check for spaces and replace with "%20"
         pdf_url = urllib.quote("https://stations.fcc.gov//" + l, safe="%/:=&?~#+!$,;'@()*[]")
         pdf_file = urllib2.urlopen(pdf_url)
         #Use regex ^.*\/(.*) to grab filename
         file_name = station_define + re.findall(r'^.*\/(.*)',l)[0]
         #Only download file if it doesn't alrady exist
         if not os.path.isfile(file_name):
            try:
               output = open(file_name,'wb')
               output.write(pdf_file.read())
               output.close()
               print 'DOWNLOADED: ' + file_name
            except:
               print 'ERROR: File ' + file_name + ' failed to save'
         else:
            print 'ALERT: File ' + file_name + " already exists in this directory. Not downloaded."
      except:
         print 'ERROR: URL ' + pdf_url + ' failed to load. Check URL.'

#take a csv and prepare to pass it to get_response
def parse_csv(csv_define, save_loc):
   with open(csv_define,'rb') as csvfile:
      station_reader = csv.reader(csvfile,delimiter=',')
      for row in station_reader:
         get_response(row[1],save_loc)

if __name__ == '__main__':
   parser = argparse.ArgumentParser(description='Download the files from a station RSS feed')
   parser.add_argument('path',help='Enter the station rss path')
   parser.add_argument('call_sign',default="",nargs='?',help='Enter the file destination (default is pwd)')
   #need to deal with the positional problem. flag maybe?
   parser.add_argument('arg_type',default=0,type=int,nargs='?',help='0 if single station, 1 if csv path (default is 0)')
   args = parser.parse_args()

   #if csv is passed in, run parse_csv, otherwise, run once
   if args.arg_type == 1:
      parse_csv(args.path,args.call_sign)
   else:
      get_response(args.path, args.call_sign)
   print "...done downloading"