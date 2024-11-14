import discordlogswebhook as ds
import pyautogui as pg
from pynput import keyboard
import time
from tkinter import *

run_bot = False
quit_all = True
depo_tracker = 0
logs_timer = 0
num_food = 0
feed_tracker = 0


def run(feed_tracker, depo_tracker, logs_timer):
    #
    #   This is the main function for the program, only called in the main runtime loop
    #
    grab_paste()
    depo_tracker += 1
    feed_tracker += 1
    if depo_tracker >= 100:
        dump_paste()
        depo_tracker = 0
    if feed_tracker >= 200:
        feed_player()
        feed_tracker = 0
    ulogs_timer = check_logs(logs_timer)
    return feed_tracker,depo_tracker,ulogs_timer


def grab_paste():
    #
    #   Grabs paste from the ground in front of the player's camera
    #
    print('Grabbing Paste...')
    time.sleep(.5)
    pg.press('f')
    time.sleep(.5)  
     
def dump_paste():
    #
    #   Dumps paste in the dedis directly infront of the player's camera
    #
    print('Dumping Paste...')
    time.sleep(.5)
    pg.press('c')
    time.sleep(.5)
    pg.press('e')
    time.sleep(.5)
    pg.press('c')
    time.sleep(.5)
    pg.press('e')
    time.sleep(.5)
    pg.press('x')
      
def check_logs(logs_timer):
    #
    #   Checks tribe logs and determines if it should send them to discord.
    #   ATM it sends logs every ~3 minutes to not spam the discord channel.
    #
    print('Checking Logs...')
    pg.press('l')
    time.sleep(2)
    if logs_timer >= 10:
        print('Sending Logs to Discord...')
        ds.send_logs_image()
        logs_timer = 0
    time.sleep(15)
    pg.press('esc')
    logs_timer += 1
    return logs_timer
    
def feed_player():
    #
    #   Feeds player using slots 8 and 9 (if there is food left in player's inventory)
    #
    global num_food
    print('Feeding Player...')
    pg.press('8')
    pg.press('9')
    num_food += 1
    if num_food >= 19:
        ds.send_need_food_alert()
        num_food = 0
    
def on_press(key):
    #
    #   Listener for keyboard presses
    #   Utilized to pause and start the bot
    #
    global run_bot
    if key == keyboard.Key.f8 and key == keyboard.Key.f22:
        return False
    try:
        k = key.char
    except:
        k = key.name
    if k in ['f8']:
        global quit_all
        global run_bot
        print('Quitting...')
        quit_all = False
        run_bot = False
    if k in ['f7']:
        print('Pausing...') 
        run_bot = False
    if k in ['f5']:
        print('Starting/Resuming...')
        run_bot = True
    
listener = keyboard.Listener(on_press=on_press)
listener.start()

while quit_all == True:
    while run_bot == True:
        passed_values = run(feed_tracker,depo_tracker,logs_timer)
        depo_tracker = passed_values[1]
        logs_timer = passed_values[2]
