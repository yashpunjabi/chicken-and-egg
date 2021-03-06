# Here we have the application that will determine whether the chicken or the egg came first
# using twitter and the Hubble telescope. And also math.

from __future__ import division
from urllib2 import Request, urlopen, URLError
from datetime import datetime, timedelta
import json
import numpy

import matplotlib.pyplot as plt

#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import simplejson
#Variables that contains the user credentials to access Twitter API

NASA_FIRST_DAY = '1995-9-22'
eggfirst = True


import re
import urllib2


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

    for i in range(1):
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
        if imgUrl != None:
            avgList.append(getAveragePixelValue(imgUrl))

    return numpy.mean(avgList)

def callServerForLessThan128(n):
    request = Request("http://cloaca.azurewebsites.net/determineChickenOrEgg/" + str(n))
    try:
        response = urlopen(request)
        s = response.read()
        return s == "true"
    except URLError, e:
        print ' eggz. Got an error code:', e
        return False

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):
    def __init__(self):
        self.eggcount = 0
        self.chickencount = 0
        self.first = True
        self.time1 = 0
        fig = plt.figure()
        fig.set_facecolor('white')

    def on_data(self, data):
        try:
            parsedData = simplejson.loads(data)
            text =  parsedData['text'].encode('utf-8')
            time =  int(parsedData['timestamp_ms'].encode('utf-8'))
            print text
            if self.first:
                self.time1 = time
                self.first = False
                plt.xlabel("time in miliseconds")
                plt.ylabel("Number of tweets")
            plt.axis([self.time1-10000, time+10000,-5,self.chickencount+10])
            plt.ion()
            plt.scatter(time, self.chickencount)
            plt.scatter(time, self.eggcount,color="red")


            if (self.eggcount+self.chickencount) > 0:
                plt.title(str(100-(self.chickencount/(self.eggcount+self.chickencount)*100)) + "% chance CHICKEN came first",color="blue",loc="left")
                plt.title(str(100-(self.eggcount/(self.eggcount+self.chickencount)*100)) + "% chance EGG came first",color="red",loc="right")
            plt.pause(0.001)



            #Adding to the chicken
            if eggfirst:
                self.eggcount+= 1 if ('egg' in text.lower()) else 0
                self.chickencount+= 1 if ('chicken' in text.lower()) else 0
            else:
                self.chickencount+= 1 if ('chicken' in text.lower()) else 0
                self.eggcount+= 1 if ('egg' in text.lower()) else 0

            return True
        except Exception as e:
            print e
            return False

    def on_error(self, status):
        print status


if __name__ == '__main__':
    avg = findTheMainAverageOfAllTheImages()
    eggfirst = callServerForLessThan128(int(avg))

    f = open('config.txt','r')
    lines = f.readlines()
    access_token = lines[0].strip()
    access_token_secret = lines[1].strip()
    consumer_key = lines[2].strip()
    consumer_secret = lines[3].strip()


    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=['chicken', 'egg'])
