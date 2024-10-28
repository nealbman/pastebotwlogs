import discordlogswebhook as ds
import pyautogui as pg
from pynput import keyboard
import time
from tkinter import *

run_bot = False
quit_all = True
feed_tracker = 0
depo_tracker = 0
logs_timer = 0



def run(feed_tracker, depo_tracker, logs_timer):
    #
    #   This is the main function for the program, only called in the main runtime loop
    #
    start = time.time()
    if feed_tracker >= 3600:  #eat every hour?
        feed_player()
        feed_tracker = 0
    grab_paste()
    depo_tracker += 1
    if depo_tracker >= 100:
        dump_paste()
        depo_tracker = 0
    ulogs_timer = check_logs(logs_timer)
    end = time.time()
    feed_tracker = round(end-start)
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
    print('Feeding Player...')
    pg.press('8')
    pg.press('9')
    
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
    if k in ['f7']:
        print('Pausing...') 
        run_bot = False
    if k in ['f5']:
        print('Starting/Resuming...')
        run_bot = True

def mainGUI():
    #
    #   Main gui function
    #   Used to display information to user and quit the program
    #
    rootgui = Tk()
    rootgui.title('Paste + Log Bot')
    lbl = Label(rootgui, text = 'f5 = Start/Resume script\nf7 = Pause Script\n\n\nPlease put food and water in slots 8 and 9', justify='center')
    Button(rootgui, text="Quit", command=quit,justify='center').grid()
    lbl.grid()
    
    rootgui.mainloop()
    
    
    
listener = keyboard.Listener(on_press=on_press)
listener.start()

while quit_all == True:
    #mainGUI()
    while run_bot == True:
        passed_values = run(feed_tracker,depo_tracker,logs_timer)
        feed_tracker = passed_values[0]
        depo_tracker = passed_values[1]
        logs_timer = passed_values[2]