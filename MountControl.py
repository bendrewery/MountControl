#Test sync from tablet to github

#!/usr/bin/python2
#coding=utf-8
import os
import sys
import RPi.GPIO as GPIO
import time
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'Hide'
import pygame
 
# Pin Output
IN1 = 18
IN2 = 16
ENA = 22
IN3 = 13
IN4 = 11
ENB = 15

# Defaults
pwm_frequency = 1000
alt_duty_cycle = 100 # 0-100%
az_duty_cycle = 100 # 0-100%

# Colours
black = [255, 255, 255]
white = [0, 0, 0]
red = [200, 0, 0]
bright_red = [255, 0, 0]

def init():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(IN1, GPIO.OUT) # Alt UP
    GPIO.setup(IN2, GPIO.OUT) # Alt DOWN
    GPIO.setup(ENA, GPIO.OUT)
    GPIO.setup(IN3, GPIO.OUT) # AZ LEFT
    GPIO.setup(IN4, GPIO.OUT) # AZ RIGHT
    GPIO.setup(ENB, GPIO.OUT)
  
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption('Mount Controller')
    screen.fill(black)
    # to spam the pygame.KEYDOWN event every 100ms while key being pressed
    pygame.key.set_repeat(100, 100)
  
    #alt_pwm = GPIO.PWM(ENA, pwm_frequency)
    #az_pwm = GPIO.PWM(ENB, pwm_frequency)
    #alt_pwm.start(alt_duty_cycle)
    #az_pwm.start(az_duty_cycle)
 
# All pins are low level for reset and stop operation
def reset():
  GPIO.output(IN1, GPIO.LOW)
  GPIO.output(IN2, GPIO.LOW)
  GPIO.output(IN3, GPIO.LOW)
  GPIO.output(IN4, GPIO.LOW)
  GPIO.output(ENA, GPIO.LOW)
  GPIO.output(ENB, GPIO.LOW)
  
def alt_up(): 
  GPIO.output(IN2, GPIO.LOW)
  GPIO.output(IN1, GPIO.HIGH)
  GPIO.output(ENA, GPIO.HIGH)

def alt_down():
  GPIO.output(IN1, GPIO.LOW)
  GPIO.output(IN2, GPIO.HIGH)
  GPIO.output(ENA, GPIO.HIGH)
   
def az_left(): 
  GPIO.output(IN4, GPIO.LOW)
  GPIO.output(IN3, GPIO.HIGH)
  GPIO.output(ENB, GPIO.HIGH)

def az_right():
  GPIO.output(IN3, GPIO.LOW)
  GPIO.output(IN4, GPIO.HIGH)
  GPIO.output(ENB, GPIO.HIGH)
  
def stop():
  reset()

init()
reset()
x = True
try:
    while x:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("except")
                    stop()
                    GPIO.cleanup()
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    print('alt UP')
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    print('alt DOWN')
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    print('az LEFT')
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    print('az RIGHT')
            if event.type == pygame.KEYUP:
                print('stop')
except KeyboardInterrupt:
  print("except")
finally:
  x = False
  stop()
  GPIO.cleanup()
  exit()

