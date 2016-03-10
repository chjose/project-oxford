__author__ = 'Christin'

########### Python 2.7 #############
import httplib, urllib, base64

headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': '--',
  
}

params = urllib.urlencode({
    # Request parameters
    'faceRectangles': '{string}',
})

try:
    conn = httplib.HTTPSConnection('api.projectoxford.ai')
    conn.request("POST", "/emotion/v1.0/recognize", '{ "url": "http://www.weareteachers.com/images/default-source/blog-images/smiling-baby.jpg" }', headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))
