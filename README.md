# python-simple-timezone-localizer
Given time and date, plus latitude and longitude, outputs the local time and time zone

Runs on python 2.7

system setup if there are issues
pip install sudo pip install pytz

pip install tzwhere

pip install pyOpenSSL ndg-httpsclient pyasn1

# Design notes

tzwhere does not handle timezones over water very well, in those instances the Google API is called. Substitute your own API key. I guess in theory, that reduces your google api requests.

I make no authorship claims to the indjango info, but it's a really good article for google api access info if you are new.
http://www.indjango.com/google-api-to-get-timezone-from-lat-long-coordinates-in-python/
Or more direct link to the google docs
https://developers.google.com/maps/documentation/timezone/start

# Proper usage:
cat data.csv | python localizer.py > out.csv
