# 13.09.2022
# Version 4 of Joystick firmware

#from re import L
#rom pyparsing import Or
import board
import digitalio
import time
from analogio import AnalogIn
import math
import adafruit_dotstar as dotstar

import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
key = Keyboard(usb_hid.devices)

print('\n','\t','\t','\t','########',"Startin new session",'########')

### RGB LED setup
dots = dotstar.DotStar(board.GP14, board.GP15, 2, brightness=0.2)
dots[0] = (0,0,0)
dots[1] = (0,0,0)
## ONBOARD LED setup
led = digitalio.DigitalInOut(board.GP25)
led.direction = digitalio.Direction.OUTPUT
led.value = False

## INDICATING THAT THE DEVICE HAS BOOTED UP AN IS ABOUT TO START INITIALISE BUTTONS AND ANALOG IN, LEDS RED
dots[0] = (33,0,0)
dots[1] = (33,0,0)
time.sleep(2)


### A button setup
pogaPinA = board.GP1
pogaA = digitalio.DigitalInOut(pogaPinA)
pogaA.direction = digitalio.Direction.INPUT
pogaA.pull = digitalio.Pull.UP

## B button setup
pogaPinB = board.GP2
pogaB = digitalio.DigitalInOut(pogaPinB)
pogaB.direction = digitalio.Direction.INPUT
pogaB.pull = digitalio.Pull.UP

## C button setup
pogaPinC = board.GP4
pogaC = digitalio.DigitalInOut(pogaPinC)
pogaC.direction = digitalio.Direction.INPUT
pogaC.pull = digitalio.Pull.UP

## D button setup
pogaPinD = board.GP3
pogaD = digitalio.DigitalInOut(pogaPinD)
pogaD.direction = digitalio.Direction.INPUT
pogaD.pull = digitalio.Pull.UP

## X button setup
pogaPinX = board.GP5
pogaX = digitalio.DigitalInOut(pogaPinX)
pogaX.direction = digitalio.Direction.INPUT
pogaX.pull = digitalio.Pull.UP

## Y button setup
pogaPinY = board.GP6
pogaY = digitalio.DigitalInOut(pogaPinY)
pogaY.direction = digitalio.Direction.INPUT
pogaY.pull = digitalio.Pull.UP

## Z button setup
pogaPinZ = board.GP8
pogaZ = digitalio.DigitalInOut(pogaPinZ)
pogaZ.direction = digitalio.Direction.INPUT
pogaZ.pull = digitalio.Pull.UP

## W button setup
pogaPinW = board.GP7
pogaW = digitalio.DigitalInOut(pogaPinW)
pogaW.direction = digitalio.Direction.INPUT
pogaW.pull = digitalio.Pull.UP

## R button from analog stick setup
pogaPinR = board.GP10
pogaR = digitalio.DigitalInOut(pogaPinR)
pogaR.direction = digitalio.Direction.INPUT
pogaR.pull = digitalio.Pull.UP

## L button from analog stick setup
pogaPinL = board.GP9
pogaL = digitalio.DigitalInOut(pogaPinL)
pogaL.direction = digitalio.Direction.INPUT
pogaL.pull = digitalio.Pull.UP


## Analog stick L Vertical Pin reference
analogLV = AnalogIn(board.A0)

## Analog stick L Horisontal Pin reference
analogLH = AnalogIn(board.A1)

## Analog stick R Horisontal Pin reference
analogRH = AnalogIn(board.A2)

##Reducing noise on ADC by pulling GP23 high
noisePin = digitalio.DigitalInOut(board.GP23)
noisePin.direction = digitalio.Direction.OUTPUT
noisePin.value = True

# Takes  12 bit analog input signal and smooths it out, gives out a value between 0 and 650
def analogInput(analogPin):
    signalValue = analogPin.value
    signalRanged = signalValue //100  #This does the magic dddsn
    return signalRanged

# Create two lists that are used to range the joistick position output
invL = []
strL = []
for creator in range(300,-1,-30):
    #print(creator)
    invL.append(creator)
for creator in range(340,651,30):
    #print(creator)
    strL.append(creator)

# Joystick class that reads the analog input and gives out certain driving parameters.
class Joystick:
    # direction, speed, angle
    def moving(self):
        drivingVal = analogInput(analogLV)
        return drivingVal

    def turning(self):
        turningVal = analogInput(analogRH)
        return turningVal

    def driving_dir(self):
        drivingVal = analogInput(analogLV)
        if drivingVal < 300:
            return "forward"
        elif drivingVal in range(300, 341):
            return "zero"
        elif drivingVal > 340:
            return "backward"

    def driving_speed(self):
        speed = analogInput(analogLV)
        if speed in range(strL[0],strL[1]):
            return 1
        elif speed in range(strL[1],strL[2]):
            return 2
        elif speed in range(strL[2],strL[3]):
            return 3
        elif speed in range(strL[3],strL[4]):
            return 4
        elif speed in range(strL[4],strL[5]):
            return 5
        elif speed in range(strL[5],strL[6]):
            return 6
        elif speed in range(strL[6],strL[7]):
            return 7
        elif speed in range(strL[7],strL[8]):
            return 8
        elif speed in range(strL[8],strL[9]+50):
            return 9
        if speed in range(invL[1],invL[0]):
            return 1
        elif speed in range(invL[2],invL[1]):
            return 2
        elif speed in range(invL[3],invL[2]):
            return 3
        elif speed in range(invL[4],invL[3]):
            return 4
        elif speed in range(invL[5],invL[4]):
            return 5
        elif speed in range(invL[6],invL[5]):
            return 6
        elif speed in range(invL[7],invL[6]):
            return 7
        elif speed in range(invL[8],invL[7]):
            return 8
        elif speed in range(invL[9]-50,invL[8]):
            return 9
        elif speed in range(300,340):
            return 0

    def turning_dir(self):
        turning = analogInput(analogRH)
        if turning < 300:
            return "Right"
        elif turning in range(300, 341+20):
            return "zero"
        elif turning > 340+20:
            return "Left"

    def turning_speed(self):
        angle = analogInput(analogRH)
        #print(angle)
        if angle in range(strL[0]+20,strL[1]):
            return 1
        elif angle in range(strL[1],strL[2]):
            return 2
        elif angle in range(strL[2],strL[3]):
            return 3
        elif angle in range(strL[3],strL[4]):
            return 4
        elif angle in range(strL[4],strL[5]):
            return 5
        elif angle in range(strL[5],strL[6]):
            return 6
        elif angle in range(strL[6],strL[7]):
            return 7
        elif angle in range(strL[7],strL[8]):
            return 8
        elif angle in range(strL[8],strL[9]+50):
            return 9
        if angle in range(invL[1],invL[0]):
            return 1
        elif angle in range(invL[2],invL[1]):
            return 2
        elif angle in range(invL[3],invL[2]):
            return 3
        elif angle in range(invL[4],invL[3]):
            return 4
        elif angle in range(invL[5],invL[4]):
            return 5
        elif angle in range(invL[6],invL[5]):
            return 6
        elif angle in range(invL[7],invL[6]):
            return 7
        elif angle in range(invL[8],invL[7]):
            return 8
        elif angle in range(invL[9]-50,invL[8]):
            return 9
        elif angle in range(300,340+20):
            return 0

# FUNCTION THAT TAKES IN CERTAIN DRIVING PARAMETERS AND ACTS AS A USB KEYBOARD AND PRESSES SOME BUTTONS
def keyboardDriving(forwBackw,speed):
    if forwBackw is "forward":
        if speed is 1:
            key.press(Keycode.P,Keycode.ONE)#
        elif speed is 2:
            key.press(Keycode.P,Keycode.TWO)#
        elif speed is 3:
            key.press(Keycode.P,Keycode.THREE)#
        elif speed is 4:
            key.press(Keycode.P,Keycode.FOUR)#
        elif speed is 5:
            key.press(Keycode.P,Keycode.FIVE)#
        elif speed is 6:
            key.press(Keycode.P,Keycode.SIX)#
        elif speed is 7:
            key.press(Keycode.P,Keycode.SEVEN)#
        elif speed is 8:
            key.press(Keycode.P,Keycode.EIGHT)#
        elif speed is 9:
            key.press(Keycode.P,Keycode.NINE)#
    elif forwBackw is "backward":
        if speed is 1:
            key.press(Keycode.M,Keycode.ONE)#
        elif speed is 2:
            key.press(Keycode.M,Keycode.TWO)#
        elif speed is 3:
            key.press(Keycode.M,Keycode.THREE)#
        elif speed is 4:
            key.press(Keycode.M,Keycode.FOUR)#
        elif speed is 5:
            key.press(Keycode.M,Keycode.FIVE)#
        elif speed is 6:
            key.press(Keycode.M,Keycode.SIX)#
        elif speed is 7:
            key.press(Keycode.M,Keycode.SEVEN)#
        elif speed is 8:
            key.press(Keycode.M,Keycode.EIGHT)#
        elif speed is 9:
            key.press(Keycode.M,Keycode.NINE)#
    elif forwBackw is "zero":
        key.press(Keycode.S)
def keyboardTurning(leftRight,angle):
    if leftRight is "Left":
        if angle is 1:
            key.press(Keycode.K, Keycode.ONE)
        elif angle is 2:
            key.press(Keycode.K, Keycode.TWO)
        elif angle is 3:
            key.press(Keycode.K, Keycode.THREE)
        elif angle is 4:
            key.press(Keycode.K, Keycode.FOUR)
        elif angle is 5:
            key.press(Keycode.K, Keycode.FIVE)
        elif angle is 6:
            key.press(Keycode.K, Keycode.SIX)
        elif angle is 7:
            key.press(Keycode.K, Keycode.SEVEN)
        elif angle is 8:
            key.press(Keycode.K, Keycode.EIGHT)
        elif angle is 9:
            key.press(Keycode.K, Keycode.NINE)
    elif leftRight is "Right":
        if angle is 1:
            key.press(Keycode.L, Keycode.ONE)
        elif angle is 2:
            key.press(Keycode.L, Keycode.TWO)
        elif angle is 3:
            key.press(Keycode.L, Keycode.THREE)#k
        elif angle is 4:
            key.press(Keycode.L, Keycode.FOUR)
        elif angle is 5:
            key.press(Keycode.L, Keycode.FIVE)
        elif angle is 6:
            key.press(Keycode.L, Keycode.SIX)
        elif angle is 7:
            key.press(Keycode.L, Keycode.SEVEN)
        elif angle is 8:
            key.press(Keycode.L, Keycode.EIGHT)
        elif angle is 9:
            key.press(Keycode.L, Keycode.NINE)
    elif leftRight is "zero":
        key.press(Keycode.N)


while True:
    ## INDICATING THAT THE DEVICE HAS ENTERED MAIN WHILE LOOP, LEDS AMBER
    dots[0] = (33,22,0)
    dots[1] = (33,22,0)

    ## Testing ADC noise
    #noiseSIG = analogInput(analogRH)
    #noiseSIG2 = analogRH.value
    #print(noiseSIG)
    #time.sleep(0.15)
    if pogaX.value is False and pogaW.value is False and pogaB.value is False and pogaD.value is False:
        device_on = True
    else:
        device_on = False

    ## DEFINING STRINGS TO USE LATER
    prewSpeed = ''
    prewSpeedVal = ''
    prewTurn = ''
    prewTurnVal = ''
    stopstateA = True
    stopstateB = True

    while device_on:
        ## INDICATING THAT THE DEVICE HAS ENTERED MAIN WHILE LOOP, LEDS GREEN
        dots[0] = (0,22,0)
        dots[1] = (0,22,0)

        ## USING JOYSTICK CLASS ANALOG DATA READINGS ARE GATHERED AND GIVEN OUT IN CERTAIN FORMAT
        joystick = Joystick()

        forwBackw = joystick.driving_dir()
        speed = joystick.driving_speed()
        leftRight = joystick.turning_dir()
        angle = joystick.turning_speed()
        #print(forwBackw,speed, leftRight, angle)

        ## JOYSTICK AND BUTTON SIGNALS ARE DETECTED AND SENT AS A USB KEYBOARD OUTPUTS
        ## IF THE ANALOG SIGNAL IS ZERO IT WILL BE POSTED ONCE, OTHERWISE ALL OTHER SINALS ARE POSTED REPEATEDLY
        if forwBackw == 'zero':
            if stopstateA == True:
                keyboardDriving(forwBackw,speed)
                time.sleep(0.07)
                key.release_all()
                stopstateA = False
            else:
                pass
        else:
            keyboardDriving(forwBackw,speed)
            time.sleep(0.07)
            key.release_all()
            stopstateA = True

        if leftRight == 'zero':
            if stopstateB == True:
                keyboardTurning(leftRight,angle)
                time.sleep(0.07)
                key.release_all()
                stopstateB = False
            else:
                pass
        else:
            keyboardTurning(leftRight,angle)
            time.sleep(0.07)
            key.release_all()
            stopstateB = True

        ## PUSHBUTTON DETECTION AND SIGNAL OUTPUT
        if pogaW.value is False:
            led.value = True
            key.press(Keycode.W)
            time.sleep(0.07)
        else:
            pass  #

        if pogaA.value is False:
            led.value = True
            key.press(Keycode.A)
            dots[0] = (33,33,33)
            time.sleep(0.07)
        else:
            pass
        if pogaB.value is False:
            led.value = True
            key.press(Keycode.B)
            time.sleep(0.07)
        else:
            pass
        if pogaC.value is False:
            led.value = True
            key.press(Keycode.C)
            time.sleep(0.07)
        else:
            pass
        if pogaD.value is False:
            led.value = True
            key.press(Keycode.D)
            time.sleep(0.07)
        else:
            pass
        if pogaX.value is False:
            led.value = True
            key.press(Keycode.X)
            time.sleep(0.07)
        else:
            pass
        if pogaY.value is False:
            led.value = True
            key.press(Keycode.Y)
            time.sleep(0.07)
        else:
            pass
        if pogaZ.value is False:
            led.value = True
            key.press(Keycode.Z)
            time.sleep(0.07) # ddcccaa
        else:
            pass

        ##EXITING THE LOOP
        if pogaB.value is False and pogaD.value is False and pogaX.value is False:
            device_on = False
        else:
            device_on = True

        # Release all keys
        key.release_all()


