# Mount Control script to control the ALT/AZ action of a custom EW head wedge.
# Python script is controlling a XY-160D Board, a L298N Dual H Bridge motor driver.
# Written by Ben Drewery

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
#pwm_frequency = 1000
#alt_duty_cycle = 100 # 0-100%
#az_duty_cycle = 100 # 0-100%

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
    button(screen, "Up", 200, 50, 100, 100, red)
    button(screen, "Left", 90, 160, 100, 100, red)
    button(screen, "Right", 310, 160, 100, 100, red)
    button(screen, "Down", 200, 270, 100, 100, red)
    # to spam the pygame.KEYDOWN event every 100ms while key being pressed
    # pygame.key.set_repeat(100, 100)
  
    #alt_pwm = GPIO.PWM(ENA, pwm_frequency)
    #az_pwm = GPIO.PWM(ENB, pwm_frequency)
    #alt_pwm.start(alt_duty_cycle)
    #az_pwm.start(az_duty_cycle)
    return screen
 
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
    button(screen, "Up", 200, 50, 100, 100, bright_red)

def alt_down():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(ENA, GPIO.HIGH)
    button(screen, "Down", 200, 270, 100, 100, bright_red)
   
def az_left(): 
    GPIO.output(IN4, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(ENB, GPIO.HIGH)
    button(screen, "Left", 90, 160, 100, 100, bright_red)

def az_right():
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    GPIO.output(ENB, GPIO.HIGH)
    button(screen, "Right", 310, 160, 100, 100, bright_red)
  
def stop_alt_up():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(ENA, GPIO.LOW)
    button(screen, "Up", 200, 50, 100, 100, red)

def stop_alt_dowm():
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(ENA, GPIO.LOW)
    button(screen, "Down", 200, 270, 100, 100, red)

def stop_az_left():
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(ENB, GPIO.LOW)
    button(screen, "Left", 90, 160, 100, 100, red)

def stop_az_right():
    GPIO.output(IN4, GPIO.LOW)
    GPIO.output(ENB, GPIO.LOW)
    button(screen, "Right", 310, 160, 100, 100, red)

# text object
def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()


# button
def button(screen, msg, x, y, w, h, c):
    global e
    # mouse = pygame.mouse.get_pos()
    pygame.draw.rect(screen, c, (x, y, w, h))

    smallText = pygame.font.Font("freesansbold.ttf", 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    screen.blit(textSurf, textRect)

init()
reset()
x = True
try:
    while x:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("except")
                    reset()
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
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    print('stop alt UP')
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    print('stop alt DOWN')
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    print('stop az LEFT')
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    print('stop az RIGHT')
    # update display
    pygame.display.update()
except KeyboardInterrupt:
    print("except")
finally:
    x = False
    reset()
    GPIO.cleanup()
    exit()

