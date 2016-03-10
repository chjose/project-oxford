import time

__author__ = 'Christin'

import httplib, urllib, base64, csv, json

#Get all image URLs from the xls file
URL = []
with open("C:\Users\Christin\Dropbox\Shy_Rutgers\H dataset\sessions_0plus_to_10_metadata.csv",'r') as f:
    data = [row for row in csv.reader(f.read().splitlines())]
    for row in data:
        URL.append([row[205],row[212]])

# print URL
# exit()
URL = URL[1:]
#print len(URL)

headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': '--',
}

params = urllib.urlencode({
    # Request parameters
    'visualFeatures': 'All',
})


with open('instagram_image_features.csv', 'wb') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)

    header = []
    header.append('Image ID')
    header.append('Image Link')
    header.append('Category Name')
    header.append('Category Score')
    header.append('Is Adult')
    header.append('Adult score')
    header.append('Is Racy')
    header.append('Racy score')
    header.append('Faces JSON')
    header.append('Dominant foreground color')
    header.append('Dominant background color')
    header.append('Dominant colors')

    spamwriter.writerow(header)

    for url in URL:
        try:
            while True:
                conn = httplib.HTTPSConnection('api.projectoxford.ai')
                conn.request("POST", "/vision/v1/analyses?%s" % params, '{ "url": "%s" }'%url[0], headers)
                response = conn.getresponse()
                data = response.read()
                json_format = json.loads(data)
                print(json_format)
                if "Rate limit is exceeded" in data:
                    time.sleep(10)
                    continue
                if "code" not in data:
                    row = []
                    row.append(url[1])
                    row.append(url[0])
                    cate = []
                    cat_score = []
                    if "categories" in json_format:
                        for cat in json_format["categories"]:
                            cate.append(cat["name"])
                            cat_score.append(cat["score"])
                    row.append(str(cate).replace(","," "))
                    row.append(str(cat_score).replace(","," "))
                    if "adult" in json_format:
                        row.append(json_format["adult"]["isAdultContent"])
                        row.append(json_format["adult"]["adultScore"])
                        row.append(json_format["adult"]["isRacyContent"])
                        row.append(json_format["adult"]["racyScore"])
                    else:
                        row.append("NA")
                        row.append("NA")
                        row.append("NA")
                        row.append("NA")
                    row.append(str(json_format["faces"]).replace(","," "))
                    row.append(json_format["color"]["dominantColorForeground"])
                    row.append(json_format["color"]["dominantColorBackground"])
                    row.append(str(json_format["color"]["dominantColors"]).replace(","," "))
                    spamwriter.writerow(row)
                    print(row)
                    #exit()
                conn.close()
                break
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))