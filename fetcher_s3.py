import urllib2, urllib
from bs4 import BeautifulSoup
from datetime import datetime
import re, argparse, csv, os.path
import sched, time
import boto

#read in a web page and station call letters, which serves as file destination
def get_response(url_define, station):
   conn = boto.connect_s3()
   mybucket = conn.get_bucket('mtduk.es')

   try:
      response = urllib2.urlopen(url_define)
      html = response.read()
   except:
      print 'ERROR: invalid feed url'
      return
   file_loc =[]
   #If log.csv does not already exist, create one
   if not os.path.isfile('log.csv'):
      log_writer = csv.writer(open('log.csv','wb'))
      log_writer.writerow(['dl_time', 'station', 'file_name'])
      print 'ALERT: New log created...'
   #if log.csv exists, alert user that future entries will append onto existing file
   else:
      log_writer = csv.writer(open('log.csv','a'))
      print 'ALERT: Log exists, appending...'

   soup = BeautifulSoup(html)

   #grab URLs for PDFs, starting with "collect"
   #need a test for:search for repeated strings with re: Political File.*Political File because FCC RSS feeds are jacked up
   for link in soup.find_all('a', href=re.compile("collect")):
   	clean_url = re.sub(r'Political File.*Political File','Political File',link.get('href'))
   	file_loc.append(clean_url)
   
   #loop through all the file locations and download each file to a directory
   for l in file_loc:
      try:
         #check for spaces and replace with "%20"
         pdf_url = urllib.quote("https://stations.fcc.gov//" + l, safe="%/:=&?~#+!$,;'@()*[]")
         pdf_file = urllib2.urlopen(pdf_url)
         #Use regex ^.*\/(.*) to grab filename
         file_name = re.findall(r'^.*\/(.*)',l)[0]
         #Only download file if it doesn't alrady exist
         if not os.path.isfile(file_name):
            try:
               output = open(file_name,'wb')
               output.write(pdf_file.read())
               output.close()

               #Upload to Amazon
               key = mybucket.new_key('data/'+file_name)
               key.set_contents_from_filename(file_name)

               #add new row for each file
               log_writer.writerow([str(datetime.now()),station,file_name])
               print 'DOWNLOADED: ' + file_name
            except:
               print 'ERROR: File ' + file_name + ' failed to save'
         else:
            print 'ALERT: File ' + file_name + " already exists in this directory. Not downloaded."
      except:
         print 'ERROR: URL ' + pdf_url + ' failed to load. Check URL.'

#take a csv and prepare to pass it to get_response
def parse_csv(csv_define, sc):
   with open(csv_define,'rb') as csvfile:
      station_reader = csv.reader(csvfile,delimiter=',')
      for row in station_reader:
         get_response(row[1],row[0])
   #Repeat every 4 hours (14400 seconds). Set to 60, commented for debug purposes.
   sc.enter(60,1,parse_csv,(csv_define, sc))

if __name__ == '__main__':
   parser = argparse.ArgumentParser(description='Download the files from a station RSS feed')
   parser.add_argument('path',help='Enter the station rss path')
   parser.add_argument('arg_type',default=0,type=int,nargs='?',help='1 if single station, 0 if csv path (default)')
   parser.add_argument('call_sign',default="",nargs='?',help="For a single station's files, enter station id")
   args = parser.parse_args()

   #if csv is passed in, run parse_csv, otherwise, run once
   if args.arg_type != 1:
      #parse_csv(args.path)
      #tentative functionality for scheduler, repeats until user stops it
      s = sched.scheduler(time.time, time.sleep)
      s.enter(0,1,parse_csv,(args.path,s))
      s.run()
   else:
      get_response(args.path, args.call_sign)
   print "...done downloading"