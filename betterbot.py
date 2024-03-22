import board
import time
from gpiozero import Button
import os
import sys
import spidev as SPI
sys.path.append("/home/schoolpi/LCD_Module_code/RaspberryPi/python")
from lib import LCD_1inch69
from PIL import Image, ImageDraw, ImageFont

#Colours
BLACK = 0,0,0
WHITE = 255,255,255
BLUE = 0,0,255
YELLOW = 255,255,0
LIME = 0,255,0
RED = 255,0,0
PINK = 255,0,255
LIGHTBLUE = 0,255,255
GREEN = 0,255,0
ORANGE = 255,128,0
BROWN = 156,73,0
PURPLE = 76,0,153
DARKGREEN = 0,51,0
KELVINTEAL = 0,178,169

#Buttons
left_button = Button(21)
right_button = Button(17)
select_button = Button(16)
cancel_button = Button(12)

#Screen Pin setup
RST = 27
DC = 25
BL = 18
bus = 0
device = 0

disp = LCD_1inch69.LCD_1inch69()
disp.Init()
disp.clear()

body_font = ImageFont.truetype("/home/schoolpi/LCD_Module_code/RaspberryPi/python/Font/Font02.ttf", 32)
title_font = ImageFont.truetype("/home/schoolpi/LCD_Module_code/RaspberryPi/python/Font/Font02.ttf", 48)
sub_title_font = ImageFont.truetype("/home/schoolpi/LCD_Module_code/RaspberryPi/python/Font/Font02.ttf", 32)
timer_font = ImageFont.truetype("/home/schoolpi/LCD_Module_code/RaspberryPi/python/Font/Font02.ttf", 80)
bg_colour = WHITE
menu_level = "Main Menu"

def show_on_screen(bg_colour, text, text_pos, text_col, menu_level, sub_title_text):
    image1 = Image.new("RGB", (disp.width, disp.height), bg_colour)
    draw = ImageDraw.Draw(image1)
    
    draw.text((10,5), menu_level, fill = BLACK, font = title_font)
    draw.text((10,55), sub_title_text, fill = BLUE, font = title_font)
    draw.text((text_pos), text, fill = text_col, font = body_font)
    disp.ShowImage(image1)

def show_img_on_screen(img_path):
    image = Image.open(img_path)
    disp.ShowImage(image)
    
def show_timer_on_screen(bg_colour, text):
    image1 = Image.new("RGB", (disp.width, disp.height), bg_colour)
    draw = ImageDraw.Draw(image1)
    
    draw.text((50,80), text, fill = PURPLE, font = timer_font)
    disp.ShowImage(image1)

#Timer
minute = [1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]
b = 0

#actions
actions = ["Drink", "Stand up", "Stretch", "Time out", "Early Pass"]
action_img_names = ["Drink", "Stand_up", "Stretch", "Time_out", "Early_pass"]
a = 0

#Menu Options
menu_options = ["Set Reminders", "Change Background"]
m = 0

#Background Colours
bg_colours = [WHITE, YELLOW, RED, GREEN, LIGHTBLUE]
bg_colours_names = ["White", "Yellow", "Red", "Green", "Light Blue"]
g = 0

def select_reminder():
    global a
    show_on_screen(bg_colour, str(actions[a]), (5, 100), DARKGREEN, menu_level, "Actions")
    cancel = False
    while cancel == False:
        if left_button.is_pressed:
            a -= 1
            if a == -1:
                a = len(actions) - 1
            show_on_screen(bg_colour, str(actions[a]), (5, 100), DARKGREEN, menu_level, "Actions")
            time.sleep(0.2)
        
        elif right_button.is_pressed:
            a += 1
            if a == len(actions):
                a = 0
            show_on_screen(bg_colour, str(actions[a]), (5, 100), DARKGREEN, menu_level, "Actions")
            time.sleep(0.2)

        elif select_button.is_pressed:
            show_on_screen(bg_colour, "SELECT", (5, 100), LIME, menu_level, "")
            time.sleep(0.2)
            msg = "Wait for " + str(minute[b]) + " mins?"
            show_on_screen(bg_colour, str(msg), (5, 100), KELVINTEAL, menu_level, "TIMER")
            select_time()
        
        elif cancel_button.is_pressed:
            show_on_screen(bg_colour, "Cancel", (5, 100), BLACK, menu_level, "Actions")
            time.sleep(0.2)
            cancel = True
    show_on_screen(bg_colour, str(menu_options[m]), (5, 60), BROWN, menu_level, "")

def change_background():
    global g
    global bg_colour
    cancel = False
    while cancel == False:
        if right_button.is_pressed:
            g += 1
            if g == len(bg_colours_names):
                g = 0
            show_on_screen(bg_colour, str(bg_colours_names[g]), (5, 100), DARKGREEN, menu_level, "BG Colour")
            time.sleep(0.2)
        elif left_button.is_pressed:
            g -= 1
            if g == -1:
                g = len(bg_colours_names) - 1
            show_on_screen(bg_colour, str(bg_colours_names[g]), (5, 100), DARKGREEN, menu_level, "BG Colour")
            time.sleep(0.2)
        elif select_button.is_pressed:
            show_on_screen(bg_colour, "SELECT", (5, 100), LIME, menu_level, "")
            time.sleep(0.2)
            bg_colour = bg_colours[g]
            msg = "Bg colour changed."
            show_on_screen(bg_colour, str(msg), (5, 100), KELVINTEAL, menu_level, "BG Colour")
        elif cancel_button.is_pressed:
            show_on_screen(bg_colour, "Cancel", (5, 100), BLACK, menu_level, "Actions")
            time.sleep(0.2)
            cancel = True
    show_on_screen(bg_colour, str(menu_options[m]), (5, 60), BROWN, menu_level, "")

def select_time():
    global b
    cancel = False
    while cancel == False:
        if right_button.is_pressed:
            b += 1
            if b == len(minute):
                b = 0
            msg = "Wait for " + str(minute[b]) + " mins?"
            show_on_screen(bg_colour, str(msg), (5, 100), KELVINTEAL, menu_level, "TIMER")
            time.sleep(0.2)

        elif left_button.is_pressed:
            b -= 1
            if b == -1:
                b = len(minute) - 1
            msg = "Wait for " + str(minute[b]) + " mins?"
            show_on_screen(bg_colour, str(msg), (5, 100), KELVINTEAL, menu_level, "TIMER")
            time.sleep(0.2)

        elif select_button.is_pressed:
            seconds = minute[b] * 60
            while seconds > 0:
                seconds -= 1
                secs = seconds % 60
                mins = seconds // 60
                if secs < 10:
                    secs = "0" + str(secs)
                msg = str(mins) + ":" + str(secs)
                show_timer_on_screen(bg_colour, str(msg))
                time.sleep(1)
            for n in range(5):
                show_img_on_screen("/home/schoolpi/images/" + action_img_names[a] + "1.png")
                time.sleep(0.5)
                show_img_on_screen("/home/schoolpi/images/" + action_img_names[a] + "2.png")
                time.sleep(0.5)
            msg = actions[a] + " again?"
            show_on_screen(bg_colour, str(msg), (5, 100), KELVINTEAL, menu_level, "TIMER")

        elif cancel_button.is_pressed:
            show_on_screen(bg_colour, "Cancel", (5, 100), BLACK, menu_level, "")
            time.sleep(0.2)
            cancel = True
    show_on_screen(bg_colour, str(actions[a]), (5, 100), DARKGREEN, menu_level, "Actions")

show_img_on_screen("/home/schoolpi/images/home_screen.png")
left_button.wait_for_press()
time.sleep(0.2)
show_on_screen(bg_colour, str(menu_options[m]), (5, 60), BROWN, menu_level, "")

while True:
    #Action buttons
    if left_button.is_pressed:
        m -= 1
        if m == -1:
            m = len(menu_options) - 1
        show_on_screen(bg_colour, str(menu_options[m]), (5, 60), BROWN, menu_level, "")
        time.sleep(0.2)

    elif right_button.is_pressed:
        m += 1
        if m == len(menu_options):
            m = 0
        show_on_screen(bg_colour, str(menu_options[m]), (5, 60), BROWN, menu_level, "")
        time.sleep(0.2)

    elif select_button.is_pressed:
        show_on_screen(bg_colour, "SELECT", (5, 100), LIME, menu_level, "")
        time.sleep(0.2)
        if m == 0:
            show_on_screen(bg_colour, str(actions[a]), (5, 100), DARKGREEN, menu_level, "Actions")
            select_reminder()
        elif m == 1:
            show_on_screen(bg_colour, str(bg_colours_names[g]), (5, 100), DARKGREEN, menu_level, "BG Colour")
            change_background()

    elif cancel_button.is_pressed:
        show_on_screen(bg_colour, "Cancel", (5, 100), BLACK, menu_level, "")
        time.sleep(0.2)
        show_on_screen(bg_colour, str(menu_options[m]), (5, 60), BROWN, menu_level, "")

