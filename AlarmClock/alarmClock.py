import time
from grove_rgb_lcd import *
from grovepi import *
import datetime
import time
import sys
import os
import math

# rotary A1
# botton D3
# buzzer D2
# dhtSensor D4
# light A0
# led D6
sensor = 1
button = 3
buzzer = 2
dhtSensor = 4
lightSensor = 0
led = 6

pinMode(sensor, "INPUT")
pinMode(button, "INPUT")
pinMode(buzzer, "OUTPUT")
pinMode(lightSensor, "INPUT")
pinMode(led, "OUTPUT")

fileAlarm = open("/home/pi/Mycode/AlarmClock/alarm.txt", "r")
onoffAlarm = open("/home/pi/Mycode/AlarmClock/onoff.txt", "r")

indexAlarm = str(fileAlarm.readline())
onoff = str(onoffAlarm.readline())
fileAlarm.close()
onoffAlarm.close()

digitalWrite(buzzer, "OUTPUT")

print(indexAlarm)
print(onoff)

def restartProgram():
	python = sys.executable
	os.execl(python, python, * sys.argv)
	
lastSound = 0

while True:
	# print("in loop")
	try:
		# read from Tempreture & Humidity Sensor
		temp = 0.01
		humidity = 0.01
		[temp, humidity] = dht(dhtSensor, 0)
		if not math.isnan(temp) and not math.isnan(humidity):
			tempStr = str(temp)
			humidityStr = str(humidity)
		print(F"temp:{tempStr}, humidity:{humidityStr}")
		
		# read from light sensor
		lightSensorValue = analogRead(lightSensor)
		lightSensorValue = int(lightSensorValue / 2)
		if lightSensorValue >= 255:
			lightSensorValue = 255
		elif lightSensorValue <= 5:
			lightSensorValue = 5
		print(lightSensorValue)
		
		# display
		day = time.strftime("%d-%m-%Y")
		hour = time.strftime("%H:%M")
		if onoff == "1":
			analogWrite(led, lightSensorValue)
		else:
			analogWrite(led, 0)
		setRGB(0, 0, lightSensorValue)
		setText_norefresh(day + " " + tempStr + "C\n" + onoff + "  *" + hour + "* " + humidityStr + "%")
		print(day + hour)
		
		# alarm rings
		if hour == indexAlarm and onoff == "1":
			for count in range(0, 5):
				digitalWrite(buzzer, 0)
				setRGB(200, 5, 5)
				setText(" W A K E  UP \n   IT'S " + indexAlarm)
				while True:
					digitalWrite(buzzer, 1)
					time.sleep(.3)
					setRGB(0, 5, 5)
					digitalWrite(buzzer, 0)
					time.sleep(.3)
					setRGB(200, 5, 5)
					if digitalRead(button):
						break
					# digitalWrite(buzzer, 1)
					# time.sleep(.3)
					# setRGB(0, 5, 5)
					# digitalWrite(buzzer, 0)
				hour = time.strftime("%H:%M")
				setRGB(0, 0, lightSensorValue)
				setText_norefresh(str(day + " " + "SLEEP\n" + onoff + "  *" + hour + "* "))
				counter = 0
				while counter <= 12:
					time.sleep(5)
					if digitalRead(button):
						setText("Exit Sleeping Mode")
						time.sleep(5)
						setText_norefresh(day + " " + tempStr + "C\n" + onoff + "  *" + hour + "* " + humidityStr + "%")
						time.sleep(55)
						restartProgram()
					counter += 1
				for count in range(0, 3):
					for i in range(0, 10):
						setRGB(200, 5, 5)
						setText(" ARE YOU STILL\n  IN BED?")
						digitalWrite(buzzer, 1)
						time.sleep(.1)
						setRGB(0, 5, 5)
						digitalWrite(buzzer, 0)
						time.sleep(.1)
						setRGB(200, 5, 5)
						digitalWrite(buzzer, 1)
						time.sleep(.2)
						setRGB(0, 5, 5)
						digitalWrite(buzzer, 0)
						if digitalRead(button):
							restartProgram()
						time.sleep(.5)
				restartProgram()
			digitalWrite(buzzer, 0)
			time.sleep(.5)
		time.sleep(5)
		if digitalRead(button):
			time.sleep(1)
			break
	except (IOError, TypeError) as e:
		print("Error")
		restartProgram()
		
	except KeyboardInterrupt as e:
		print(str(e))
		# since we're exiting the program
		# it's better to leave the LCD with a blank text
		digitalWrite(led, 0)
		digitalWrite(buzzer, 0)
		break
		
for count in range(0, 10):
	try:
		rSensorValue = analogRead(sensor)
		setRGB(20, 20, 255)
		setText(" < OFF      ON > ")
		time.sleep(0.5)
		onoff = str(int(rSensorValue / 512))
		if onoff == "0" and digitalRead(button):
			setText("ALARM OFF")
			onoffAlarm = open("/home/pi/Mycode/AlarmClock/onoff.txt", "w")
			onoffAlarm.write("0")
			onoffAlarm.close()
			time.sleep(1)
			restartProgram()
		if onoff == "1" and digitalRead(button):
			setText("ALERT ON")
			onoffAlarm = open("/home/pi/Mycode/AlarmClock/onoff.txt", "w")
			onoffAlarm.write("1")
			onoffAlarm.close()
			time.sleep(1)
			while True:
				try:
					rSensorValue = analogRead(sensor)
					setRGB(200, 20, 255)
					setText(" < SET TIME\n  ALREADY DONE > ")
					time.sleep(.5)
					onoff = str(int(rSensorValue / 512))
					if onoff == "0" and digitalRead(button):
						setRGB(200, 20, 255)
						setText("   SET HOUR")
						time.sleep(1)
						while True:
							try:
								if digitalRead(button):
									time.sleep(1)
									sethour = str(" SETTED HOUR:\n         " + whour)
									setRGB(0, 255, 255)
									setText(sethour)
									time.sleep(1)
									setRGB(200, 20, 255)
									setText("   SET MINUTE")
									time.sleep(1)
									while True:
										try:
											if digitalRead(button):
												time.sleep(1)
												alarmTime = str("  WAKE UP AT\n   " + whour + ":" + wmin)
												print(alarmTime)
												setRGB(0, 255, 255)
												setText(" SETTED MINUTE:\n   " + wmin)
												time.sleep(1)
												setText(alarmTime)
												time.sleep(1)
												fileAlarm = open("/home/pi/Mycode/AlarmClock/alarm.txt", "w")
												fileAlarm.write(whour + ":" + wmin)
												fileAlarm.close()
												time.sleep(1)
												restartProgram()
											rSensorValue = analogRead(sensor)
											setRGB(255, 0, 255)
											minutes = int(rSensorValue / 17.1)
											wmin = str("%02d"%minutes)
											setText(wmin)
											time.sleep(.1)
										except IOError:
											print("Error")
								rSensorValue = analogRead(sensor)
								setRGB(0, 0, 255)
								hours = int(rSensorValue / 44.478)
								whour = str("%02d"%hours)
								setText(whour)
								time.sleep(.3)
							
							except IOError:
								print("Error")
					
					if onoff >= "1" and digitalRead(button):
						setRGB(100, 20, 255)
						setText("  WAKE UP AT:\n   " + indexAlarm)
						time.sleep(2)
						restartProgram()
				except IOError:
					print("Error")
		time.sleep(1)
	
	except(IOError, TypeError) as e:
		print("Error")
		restartProgram()
	
	except KeyboardInterrupt as e:
		print(str(e))
		# since we're exiting the program
		# it's better to leave the LCD with a blank text
		digitalWrite(led, 0)
		digitalWrite(buzzer, 0)
		break
	
print("bye~")
restartProgram()