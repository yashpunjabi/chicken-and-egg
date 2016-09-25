# Here we have the application that will determine whether the chicken or the egg came first
# using twitter and the Hubble telescope. And also math.
from urllib2 import Request, urlopen, URLError
from datetime import datetime, timedelta
import json
import numpy

NASA_FIRST_DAY = '1995-9-22'


def get_nasa_image(dateString):
    baseUrl = "https://api.nasa.gov/planetary/apod?api_key=IbhfsZ8fqnVtpYL1AffkWMyZRt63mnpcpLiqbX56&hd=true&date="
    request = Request(baseUrl + dateString)
    try:
    	response = urlopen(request)
    	jsonString = response.read()
        parsedJson = json.loads(jsonString)
        return parsedJson['hdurl']
    except URLError, e:
        print 'No eggz. Got an error code:', e


def get_thousand_nasa_images(fromDay):
    d = datetime.strptime(fromDay,'%Y-%m-%d')
    image_urls = []

    for i in range(1000):
        currentImage = get_nasa_image(d.strftime('%Y-%m-%d'))
        print d.strftime('%Y-%m-%d') + ":",  currentImage
        image_urls.append(currentImage)
        d = d+timedelta(days=1)

    return image_urls

def getAveragePixelValue(imgUrl):
    request = Request("http://mkweb.bcgsc.ca/color-summarizer/?url=" + imgUrl + "&precision=low&json=1")
    try:
        response = urlopen(request)
        jsonString = json.loads(response.read())

        rgbStats = jsonString['stats']['rgb']

        rVal = rgbStats['r']['avg'][0]
        gVal = rgbStats['g']['avg'][0]
        bVal = rgbStats['b']['avg'][0]

        avg = numpy.mean([rVal, gVal, bVal])

        print "WE HAVE NOW COMPUTED THE AVERAGE TO BE: ", avg
        return avg


    except URLError, e:
        print 'Average was f\'d :( Got an error code:', e

def findTheMainAverageOfAllTheImages():
    imgUrls = get_thousand_nasa_images(NASA_FIRST_DAY)

    avgList = []
    for imgUrl in imgUrls:
        if imgUrl != None
            avgList.append(getAveragePixelValue(imgUrl))

    return numpy.mean(avgList)

print getAveragePixelValue("static.flickr.com/37/88847543_d1eb68c5b9_m.jpg")
