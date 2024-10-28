from discord_webhook import DiscordWebhook, DiscordEmbed
import pyautogui
import os
import pytesseract
import getserverinfo
#tribe_log = []
ping_log = ['']*30
ping_tracker = 0
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
webhook_url = "https://discord.com/api/webhooks/1272103382563291198/oD0t_pcVjUh8Sdvk2fGSDJ0iwCyvOWpvOYrVnZrQVAz18RGI6Y4uaAwQHWdccDgYG5H0"

#webhook_url = "https://discord.com/api/webhooks/1300158203316797490/SINK6iJS5GSfYoUouV-2MEd7Ln34Uf9xKpaHnh6qvvftiYK5HzFJERmBV-yLIlg-82ep"

def screenshot() -> None:
    #
    #   Screenshots tribe log area on screen and saves it to "screenshot.png"
    #
    region = (750, 180, 430, 650)
    screenshot = pyautogui.screenshot(region=region)
    screenshot.save('screenshot.png')
    
def send_logs_image():
    #
    #   Takes screenshot
    #   Queries server information and sends basic information with raw screenshot to discord
    #   
    #   Calls function to compute if there is anything notable in logs, then removes the saved screenshot from the machine
    #
    screenshot()
    server_info = getserverinfo.get_server_info('9295')
    embed = DiscordEmbed(title="**Server Info**",description=str(server_info[0]))
    embed.add_embed_field(name='Players Online', value=(str(server_info[1]) + '/'+str(server_info[3])))
    embed.add_embed_field(name='Ingame Day', value=str(server_info[2]))
    webhook = DiscordWebhook(url= webhook_url)
    webhook.add_embed(embed)
    with open("screenshot.png", "rb") as f:
        webhook.add_file(file=f.read(), filename="example.jpg")
    webhook.execute()
    compute_logs('screenshot.png')
    os.remove('screenshot.png')
    
    
def send_logs_alert(alert_queue):
    #
    #   Checks whether there is duplicate alerts, if the recent alerts have not been sent in discord then send them
    #
    for x in range(len(alert_queue)):
        print(len(alert_queue))
        for y in range(len(ping_log)):
            if  str(ping_log[y]).find(str(alert_queue[x])) != -1:
                print('Found a duplicate entry... Removing...')
                remove_me = alert_queue[x]
                alert_queue.remove(remove_me)
                break
    if len(alert_queue)!= 0:
        for x in range(len(alert_queue)):
            print('x: '+ str(x))
            print('length: '+ str(len(alert_queue)))
            webhook = DiscordWebhook(url= webhook_url)
            embed = DiscordEmbed(title="**!!ALERT!!**", color='ff0000',description=alert_queue[0])
            embed.add_embed_field('**__**','<@&1156655341946294325>')
            webhook.add_embed(embed)
            webhook.execute()
            add_alert_ping(alert_queue[0])
            remove_me = alert_queue[0]
            alert_queue.remove(remove_me)
        
def compute_logs(raw_screenshot):
    #
    #   Base function to gather the logs strings from the screenshot and call functions to:
    #   Check if there is any alert-worthy messages 
    #
    raw_tribe_logs = pytesseract.image_to_string(raw_screenshot)
    tribe_log = []
    make_logs_list(raw_tribe_logs, tribe_log)  
    alert_queue = check_for_alert(tribe_log)
    if len(alert_queue) > 0:
        print('Alert Found...')
        send_logs_alert(alert_queue)
        
def make_logs_list(remaining_logs,tribe_log):
    #
    #   Search through the strings created from the log image and extract each log instance as a list of strings
    #
    try:
        if remaining_logs.find('!\n') != -1:
            start_log = remaining_logs.index('Day ')
            next_log = remaining_logs.index('!\n')
            tribe_log.append(remaining_logs[start_log:next_log+1].replace('\n',' '))
            remaining_logs = remaining_logs[next_log+1:]
            make_logs_list(remaining_logs, tribe_log)
    except:
        print('log not found...')     
def check_for_alert(tribe_log):
    #
    #   Logic to check the list of log strings for anything worthy of mentioning in discord
    #
    alert_queue = []
    for _ in range(len(tribe_log)):
        if tribe_log[_].find('killed') != -1:
            print('Something was killed...')
            if tribe_log[_-1].find('starved') != -1:
                print('Something Starved... Ignoring...')
                break
            if tribe_log[_].find('Your Tribe killed') != -1:
                print('Our tribe killed something...')
                if tribe_log[_].find('Baby') != -1:
                    print('Killed a baby... Ignoring...')
                    break
                print('We killed something imortant... alerting...')
                alert_queue.append(tribe_log[_])
            if tribe_log[_].find('Tribemember') != -1 and tribe_log[_].find('by') != -1:
                print('Tribemember was killed by something... Alerting...')
                alert_queue.append(tribe_log[_])
        if tribe_log[_].find('was destroyed') != -1:
            print('Something was destroyed...')
            if tribe_log[_].find('c4') != -1:
                print('Our own c4 was destroyed... Ignoring...')
                break
            print('Something important was destroyed... Alerting...')
            alert_queue.append(tribe_log[_])
    return alert_queue  

def add_alert_ping(alert):
    #
    #   If an alert is sent in discord, it is added to a list that holds the most recent 30 alerts
    #   This **attempts** to make sure alerts are not duplicated
    #
    global ping_log
    global ping_tracker
    ping_log[ping_tracker] = alert
    ping_tracker += 1
    if ping_tracker > 29:
        ping_tracker = 0
