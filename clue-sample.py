"""
To get started, check out the "Device Simulator Express: Getting Started" command in the command pallete, which you can access with `CMD + SHIFT + P` For Mac and `CTRL + SHIFT + P` for Windows and Linux.
To learn more about the CLUE and CircuitPython, check this link out:
https://learn.adafruit.com/adafruit-clue/circuitpython
Find example code for CPX on:
https://blog.adafruit.com/2020/02/12/three-fun-sensor-packed-projects-to-try-on-your-clue-adafruitlearningsystem-adafruit-circuitpython-adafruit/
"""

from adafruit_clue import clue
import paho.mqtt.client as mqtt

def display_text(slider):
    clue_data[0].text = "Accel: {} {} {} m/s^2".format(*(slider["dave/x-accel"],slider["dave/y-accel"],slider["dave/z-accel"]))#display the publish data(x,y,z accelerometer) in index 0.
    clue_data[1].text = "Gyro: {} {} {} dps".format(*(slider["dave/x-gyro"],slider["dave/y-gyro"],slider["dave/z-gyro"]))#display the publish data(x,y,z gyroscope) in index 1.
    clue_data[2].text = "Magnetic: {} {} {} uTesla".format(*(slider["dave/x-mag"],slider["dave/y-mag"],slider["dave/z-mag"]))#display the publish data(x,y,z magnetic) in index 2.
    clue_data[3].text = "Pressure: {} hPa".format(slider["dave/pres"])#display the publish data(pressure) in index 3.
    clue_data[4].text = "Temperature: {} C".format(slider["dave/temp"])#display the publish data(temperature) in index 4.
    clue_data[5].text = "Humidity: {} %".format(slider["dave/humi"])#display the publish data(humidity) in index 5.
    clue_data[6].text = "Proximity: {}".format(slider["dave/prox"])  #display the publish data(proximity) in index 6.
    clue_data[7].text = "Color: R: {} G: {} B: {} C: {}".format(*(slider["dave/r-c"],slider["dave/g-c"],slider["dave/b-c"],slider["dave/lgt"]))#display the publish data(colors) in index 7.
    clue_data.show()

#json that initialize all to 0.
dave = {"dave/x-accel":0,
        "dave/y-accel":0,
        "dave/z-accel":0,
        "dave/x-gyro":0,
        "dave/y-gyro":0,
        "dave/z-gyro":0,
        "dave/x-mag":0,
        "dave/y-mag":0,
        "dave/z-mag":0,
        "dave/pres":0,
        "dave/temp":0,
        "dave/humi":0,
        "dave/prox":0,
        "dave/r-c":0,
        "dave/g-c":0,
        "dave/b-c":0,
        "dave/lgt":0
        }

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.subscribe("dave/#")
        display_text(dave)
     

def on_message(client, userdata, msg):
    dave[msg.topic] = msg.payload.decode()
    display_text(dave)

  

clue.sea_level_pressure = 1020

clue_data = clue.simple_text_display(text_scale=2)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("mqtt.eclipseprojects.io", 1883, 60)

client.loop_forever()