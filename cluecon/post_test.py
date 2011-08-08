#!/usr/bin/env python

import urllib, urllib2

url = "http://cluecon.plivo.org/speaker/vote/"

POST_PARAMS = {
    "To": "16465884366",
    "From": "919611055344",
    "Direction": "inbound",
}

params = urllib.urlencode(POST_PARAMS)
request = urllib2.Request(url, params)
result = urllib2.urlopen(request).read()
print(result)
