# Here we have the application that will determine whether the chicken or the egg came first
# using twitter and the Hubble telescope. And also math.
from urllib2 import Request, urlopen, URLError
from datetime import datetime, timedelta
import json

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

get_thousand_nasa_images(NASA_FIRST_DAY)
