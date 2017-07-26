#!/usr/bin/python
# -*- coding: utf-8 -*-

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from random import randint, seed
import json
import time
import urllib2


seed(time.time)
outImage = Image.new('L',(600,800),(255))
draw = ImageDraw.Draw(outImage)

BLACK = 0

def drawCent(pos,text,font):
	px,py,sx,sy = pos
	w,h = draw.textsize(text,font=font)
	if sx == 0:
		w = 0
	if sy == 0:
		h = 0
	draw.text(((sx-w)/2+px,(sy-h)/2+py),text,BLACK,font=font)

def drawRight(pos,text,font):
	px,py = pos
	w,h = draw.textsize(text,font=font)
	draw.text((px-w,py),text,BLACK,font=font)

workingDir = '/home/weatherman/weather-display/'

hugeFont = ImageFont.truetype(workingDir+'Roboto-Regular.ttf',120)
bigFont = ImageFont.truetype(workingDir+'Roboto-Regular.ttf',64)
bigishFont = ImageFont.truetype(workingDir+'RobotoCondensed-Regular.ttf',64)
largeFont = ImageFont.truetype(workingDir+'Roboto-Regular.ttf',36)
largeishFont = ImageFont.truetype(workingDir+'RobotoCondensed-Regular.ttf',36)
normalFont = ImageFont.truetype(workingDir+'Roboto-Regular.ttf',28)
normalishFont = ImageFont.truetype(workingDir+'RobotoCondensed-Regular.ttf',28)
smallFont = ImageFont.truetype(workingDir+'Roboto-Regular.ttf',18)
tinyFont = ImageFont.truetype(workingDir+'Roboto-Regular.ttf',12)

bigWeatherFont = ImageFont.truetype(workingDir+'meteocons.ttf',300)
smallWeatherFont = ImageFont.truetype(workingDir+'meteocons.ttf',150)

iconDict = {
	'chanceflurries' : 'U',
	'chancerain' : 'R',
	'chancesleet' : 'X',
	'chancesnow' : 'W',
	'chancetstorms' : 'O',
	'clear' : 'B',
	'cloudy' : 'N',
	'flurries' : 'U',
	'fog' : 'M',
	'hazy' : 'A',
	'mostlycloudy' : 'H',
	'mostlysunny' : 'H',
	'nt_chanceflurries' : '"',
	'nt_chancerain' : '8',
	'nt_chancesleet' : '$',
	'nt_chancesnow' : '#',
	'nt_chancetstorms' : '6',
	'nt_clear' : 'C',
	'nt_cloudy' : '5',
	'nt_flurries' : '"',
	'nt_fog' : 'M',
	'nt_hazy' : 'K',
	'nt_mostlycloudy' : '4',
	'nt_mostlysunny' : '4',
	'nt_partlycloudy' : '4',
	'nt_partlysunny' : '4',
	'nt_rain' : '8',
	'nt_sleet' : '$',
	'nt_snow' : '#',
	'nt_sunny' : 'C',
	'nt_tstorms' : '6',
	'partlycloudy' : 'H',
	'partlysunny' : 'H',
	'rain' : 'R',
	'sleet' : 'X',
	'snow' : 'W',
	'sunny' : 'B',
	'tstorms' : 'O'
}

def icon(url):
	return url.split('/')[-1][:-4]

if int(time.strftime('%M',time.localtime()))%15==0:
	response = urllib2.urlopen('http://api.wunderground.com/api/[API KEY]/conditions/forecast/alerts/q/[ZIP CODE].json').read()
	outfile = open(workingDir+'weatherdata.json','w')
	outfile.write(response)
	outfile.close()
	weth = json.loads(response.decode('utf-8'))
else:
	wethjson = open(workingDir+'weatherdata.json','r')
	weth = json.loads(wethjson.read().decode('utf-8'))
	wethjson.close()

now = weth['current_observation']


dateText = time.strftime('%A, %B %d, %Y',time.localtime())
#drawCent((0,10,600,0),dateText,largeFont)
draw.text((10,10),dateText,font=largeFont)

timeText = time.strftime('%I:%M %p',time.localtime())
drawRight((590,10),timeText,largeFont)

draw.text((330,70),u'%d°F' % round(now['temp_f']),BLACK,font=hugeFont)

drawCent((15,70,300,300),iconDict[icon(now['icon_url'])],bigWeatherFont)

chill = now['windchill_f']
heatindex = now['heat_index_f']
if chill != "NA":
	draw.text((340,210),u'Wind Chill: %s°F' % chill,BLACK,font=normalFont)
elif heatindex != "NA":
	draw.text((340,210),u'Heat Index: %s°F' % heatindex,BLACK,font=normalFont)
else:
	draw.text((340,210),u'Wind Chill: --°F',BLACK,font=normalFont)

windDir = now['wind_dir']
windSpeed = int(round(now['wind_mph']))
if windSpeed == 0:
	draw.text((340,250),'Wind: Calm',BLACK,font=normalFont)
else:
	draw.text((340,250),'Wind: %s %s' % (windDir,windSpeed),BLACK,font=normalFont)
draw.text((340,290),'Humidity: %s' % now['relative_humidity'],BLACK,font=normalFont)
draw.text((340,330),'Pressure: %s mbar' % now['pressure_mb'],BLACK,font=normalishFont)

threeDaysForecast = weth['forecast']['simpleforecast']['forecastday'][0:3]

for dayCast,i in zip(threeDaysForecast, range(3)):
	if i == 0 and dayCast['qpf_day']['in'] == None: #it's nighttime, so show overnight forecast only
		forecastIcon = iconDict['nt_' + icon(dayCast['icon_url'])]
		dayText = 'Tonight'
		hiTemp = u'––'
	else:
		forecastIcon = iconDict[icon(dayCast['icon_url'])]
		dayText = 'Today'
		hiTemp = dayCast['high']['fahrenheit']
	if i != 0: 
		dayText = dayCast['date']['weekday']

	shift = 200*i
	drawCent((shift,400,200,0),dayText,largeFont)

	draw.text((shift+25,450),forecastIcon,BLACK,font=smallWeatherFont)
	draw.text((shift+25,610),"High",BLACK,font=smallFont)
	
	draw.text((shift+35,625),u"%s°F" % hiTemp,BLACK,font=bigFont)
	lowTemp = dayCast['low']['fahrenheit']
	draw.text((shift+25,690),"Low",BLACK,font=smallFont)
	draw.text((shift+35,705),u"%s°F" % lowTemp,BLACK,font=bigFont)

	draw.line((200+shift,410,200+shift,770),BLACK,width=2)


#weatherTime = time.strftime('%I:%M %p',time.localtime(int(weth['current_observation']['local_epoch'])))
nowTime = time.strftime('%I:%M %p', time.localtime())

draw.text((5,782),"Updated %s" % nowTime,BLACK,font=tinyFont)


outImage.save(workingDir+'weather.png')
