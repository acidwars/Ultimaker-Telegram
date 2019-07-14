#!/usr/bin/env python3
from ultimaker import Ultimaker3
import sys
from time import sleep

api = Ultimaker3("192.168.1.119", "heasdas")
api.loadAuth("/home/henrik/bin/ultimaker/auth.data")

def changeColor(b, s, h):
    print(b, s, h)
    led = api.put("api/v1/printer/led", data=\
            {"brightness": b, "saturation": s, "hue": h})

def blink():
    blink = api.post("api/v1/printer/led/blink", data=\
            {"frequency": 20, "count": 80})


def strobo():
    for i in range(0,100,20):  
        changeColor(0, 0, 0)
        sleep(0.1)
        changeColor(100, i, 100)


def colorCLI():
    #while True:
        #b, s, h = input(">> ").split()
    changeColor(sys.argv[1], sys.argv[2], sys.argv[3])

colorCLI()
#strobo()
