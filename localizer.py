#!/user/bin/python
import csv
import string
import sys, getopt
#import requests
import calendar
from datetime import datetime
from datetime import timedelta

import time
import requests
import pytz
from pytz import timezone

# Runs on python 2.7
#
# system setup if there are issues
# pip install sudo pip install pytz
# pip install tzwhere
# pip install pyOpenSSL ndg-httpsclient pyasn1
#
# Design notes
#
# tzwhere does not handle timezones over water very well, 
# in those instances the Google API is called.  
# I referenced information at inDjango to do it.  The
# api_key is against your own google dev account (just a heads up)
#
# Proper usage:
# cat data.csv | python localizer.py > out.csv
#
#

TIMEFORMAT = "%Y-%m-%d %H:%M:%S"

def get_time_zone_from_google(lat, lon):
   api_key = "############################"
  
   latitude  = lat
   longitude = lon
   timestamp = time.time()

   api_response = requests.get('https://maps.googleapis.com/maps/api/timezone/json?location={0},{1}&timestamp={2}&key={3}'.format(latitude,longitude,timestamp,api_key))
   api_response_dict = api_response.json()

   if api_response_dict['status'] == 'OK':
      timezone_id = api_response_dict['timeZoneId']
      timezone_name = api_response_dict['timeZoneName']
      return timezone_id
   return 'UTC'

def get_time_zone(lat, lon):
   from tzwhere import tzwhere

   tzwhere = tzwhere.tzwhere()
  
   rv = tzwhere.tzNameAt(lat, lon)
   if not rv:
      rv = get_time_zone_from_google(lat, lon)      
   return rv

def utc_to_local(dt, offset):
   return dt - timedelta(seconds = -offset)

def main(argv):
   for row in sys.stdin:
      row = row.strip()
      array = row.split(',');
      raw_utc_time = array[0]
      lat = string.atof (array[1])
      lon = string.atof (array[2])
      tz_str = get_time_zone(lat, lon)
      
      formatted_utc = datetime.strptime(raw_utc_time, TIMEFORMAT)
      formatted_tz = pytz.timezone(tz_str)
      localize_utc = formatted_tz.localize(formatted_utc)

      target_tz = pytz.timezone(tz_str)
      offset = target_tz.utcoffset(datetime.now()).total_seconds()
      localtimewithextras = utc_to_local(localize_utc, offset)
      
      localtimeclean = localtimewithextras.strftime(TIMEFORMAT)

      print array[0], ",", lat,",", lon, ",", tz_str, ",", localtimeclean

if __name__ == "__main__":
   main(sys.argv[1:])
