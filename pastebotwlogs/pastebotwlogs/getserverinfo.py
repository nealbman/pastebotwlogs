import urllib.request
import json

def get_server_info(serv_num: str):
    #
    #   Gathers server information from wildcard's website and returns useful information
    #
    with urllib.request.urlopen('https://cdn2.arkdedicated.com/servers/asa/officialserverlist.json') as url:
        server_data = json.load(url)
        for _ in server_data:
            if _['SessionName'].find(serv_num) != -1:
                serv_name = _['Name']
                serv_players = _['NumPlayers']
                serv_day = _['DayTime']
                serv_max_players = _['MaxPlayers']
        return serv_name,serv_players,serv_day,serv_max_players