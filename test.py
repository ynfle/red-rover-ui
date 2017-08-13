#!/usr/bin/pythonRoot
#This is a script


#flup helps implement fastcgi, which lets our requests run quickly
#and with little overhead
from flup.server.fcgi import WSGIServer
import sys, urlparse
#This module governs the 16-channel Adafruit PWM
import Adafruit_PCA9685
pwm = Adafruit_PCA9685.PCA9685()
#300 frequency is good for driving DC motors
pwm.set_pwm_freq(300)

#pin addresses
m1coast   = 0
m1pwm     = 1
m1forward = 2

m3coast   = 4
m3pwm     = 5
m3forward = 6

m2coast   = 8
m2pwm     = 9
m2forward = 10

m4coast   = 12  
m4pwm     = 13
m4forward = 14


def app(environ, start_response):
	#parse the http request into x and y percentages
	start_response("200 OK", [("Content-Type", "text/html")])
	i = urlparse.parse_qs(environ["QUERY_STRING"])
	if "x" in i and "y" in i:
		x = int(i["x"][0])
		y = int(i["y"][0])
		#the max difference between the two wheels 
		#as a percentage of the faster wheel's speed
		maxDif = .5
		#the speed of the faster wheel
		maxSpeed = int( round( abs(y * 2048) / 100 ) )
		#the speed of the slower wheel
		maxLower = maxSpeed - int(maxSpeed * abs(x) /100)
		m2max = maxSpeed #int(maxSpeed * 0.9)
		m2lower = maxLower #int (maxLower * 0.9)
		#debug string for the client
		string = "x: " + str(x) + " y: " + str(y)
		pwm.set_pwm(m1coast, 0, 4095)
                pwm.set_pwm(m3coast, 0, 4095)
                pwm.set_pwm(m2coast, 0, 4095)
                pwm.set_pwm(m4coast, 0, 4095)

		#if y is positive, set the motors to forward mode
		if y < 0:
			pwm.set_pwm(m1forward, 0, 0)
			pwm.set_pwm(m3forward, 0, 0)
                        pwm.set_pwm(m2forward, 0, 4095)
			pwm.set_pwm(m4forward, 0, 4095)

			string += " Moving forward "
		else:
			pwm.set_pwm(m1forward, 0, 4095)
			pwm.set_pwm(m3forward, 0, 4095)
			pwm.set_pwm(m2forward, 0, 0)
			pwm.set_pwm(m4forward, 0, 0)
			string += " Moving backward"
		#set the speed of each wheel according to direction
		if x >= 0:
			if y < 0:
				pwm.set_pwm(m1pwm, 0, maxSpeed)
				pwm.set_pwm(m3pwm, 0, maxSpeed)
                		pwm.set_pwm(m2pwm, 0, m2lower)
				pwm.set_pwm(m4pwm, 0, m2lower)
				string += " and moving right"
			else:
				pwm.set_pwm(m1pwm, 0, maxSpeed)
				pwm.set_pwm(m3pwm, 0, maxSpeed)
				pwm.set_pwm(m2pwm, 0, m2lower)
				pwm.set_pwm(m4pwm, 0, m2lower)
				string += " and moving right"
		else:
			if y < 0:
				pwm.set_pwm(m1pwm, 0, maxLower)
				pwm.set_pwm(m3pwm, 0, maxLower)
                        	pwm.set_pwm(m2pwm, 0, m2max)
				pwm.set_pwm(m2pwm, 0, m2max)
				string += " and moving left"
			else:
				pwm.set_pwm(m1pwm, 0, maxLower)
				pwm.set_pwm(m3pwm, 0, maxLower)
				pwm.set_pwm(m2pwm, 0, m2max)
				pwm.set_pwm(m4pwm, 0, m2max)
				string += " and moving left"
		#return the debug string
		yield(string);
	#something went wrong. blarg!
	else:
		yield ('blargh')

#run the app!
WSGIServer(app).run()
