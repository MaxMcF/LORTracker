# -*- coding: utf-8 -*-
"""
Dev: AHockemeyer
Date: 4/8/2021
Desc: Processes data for and into LoRMatchData table.
ChangeLog: (Who, When, What) 
"""

import requests
import csv
import pandas as pd
import pyodbc
import os
from dotenv import load_dotenv


load_dotenv()

URL = 'https://americas.api.riotgames.com'
APIKEY = os.environ.get('API_KEY')


Hugh = ['Hugh', 'iswhtw', 'NA1']
Jake = ['Jake', 'DoctorBeeves', '0229']
Adam = ['Adam', 'Heliotropite', 'NA1']
Steven = ['Steven', 'iPhone 4', 'NA1']
Alex = ['Alex', 'mmmmmBAAAACOOON', 'NA1']
Noble = ['Noble', 'Noblescute', 'moc']
Nico = ['Nico', 'ClosingThyme', 'NA1']
Max = ['Max', '', '']


# def callAPI():
#     url = URL + '/lor/ranked/v1/leaderboards'
#     headers = {'X-Riot-Token': APIKEY}
#     status = requests.get(url, headers=headers)
#     data = status.json()
#     print(min(data['players'], key=lambda x: x['lp']))


def callAccountLookup(gameName, tagLine):
    url = URL + f'/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}'
    headers = {'X-Riot-Token': APIKEY}
    status = requests.get(url, headers=headers)
    response = status.json()
    return response['puuid']


def callMatchList(puuid):
    url = URL + f'/lor/match/v1/matches/by-puuid/{puuid}/ids'
    headers = {'X-Riot-Token': APIKEY}
    status = requests.get(url, headers=headers)
    response = status.json()
    return response


def callMatchLookup(matches):
    data = []
    for matchId in matches:
        url = URL + f'/lor/match/v1/matches/{matchId}'
        headers = {'X-Riot-Token': APIKEY}
        status = requests.get(url, headers=headers)
        response = status.json()
        data.append(response)
#    print(len(data))
    return data


def analyzeDataP(data):
    df = pd.DataFrame(columns = ['MatchID','GameMode', 'GameType', 'Player1', 'DeckListCode-P1', 'Factions-P1', 'Player2', 'DeckListCode-P2', 'Factions-P2', 'Winner', 'PlayedFirst','NumOfTurns'])
    for match in data:
        if len(match['info']['players']) > 1:
            player2 = match['info']['players'][1]['puuid']
            deck2 = match['info']['players'][1]['deck_code']
            if match['info']['players'][0]['game_outcome'] == 'win':
                winner = 'Player1'
            else:
                winner = 'Player2'
            if match['info']['players'][0]['order_of_play'] == 1:
                playedFirst = 'Player1'
            else:
                playedFirst = 'Player2'
            factionp2 = match['info']['players'][0]['factions']
            lstP2Factions = []
            for faction in factionp2:
                lstP2Factions.append(faction[8:-5])

        player1 = match['info']['players'][0]['puuid']
        deck1 = match['info']['players'][0]['deck_code']
        factionp1 = match['info']['players'][0]['factions']
        lstP1Factions = []
        for faction in factionp1:
            lstP1Factions.append(faction[8:-5])

        row = { 'MatchID': match['metadata']['match_id'] ,
                'GameMode': match['info']['game_mode'], 
                'GameType': match['info']['game_type'], 
                'Player1': player1,
                'DeckListCode-P1': deck1,
                'Factions-P1': lstP1Factions,
                'Player2': player2,
                'DeckListCode-P2': deck2,
                'Factions-P2': lstP2Factions,
                'Winner': winner,
                'PlayedFirst': playedFirst,
                'NumOfTurns': match['info']['total_turn_count']}
        print(row)
        df.append(row, ignore_index=True)
    print(df)
    return df


def analyzeData(data):
    table = []
    for match in data:
        try:
            player1 = match['info']['players'][0]['puuid']
            deck1 = match['info']['players'][0]['deck_code']
            gametype = match['info']['game_type']
            
            lstP1Factions = []
            for faction in match['info']['players'][0]['factions']:
                lstP1Factions.append(faction[8:-5])
            
            
            
            if len(match['info']['players']) > 1:
                player2 = match['info']['players'][1]['puuid']
                deck2 = match['info']['players'][1]['deck_code']
                
                if match['info']['players'][0]['game_outcome'] == 'win':
                    winner = 'Player1'
                else:
                    winner = 'Player2'
                    
                if match['info']['players'][0]['order_of_play'] == 1:
                    playedFirst = 'Player1'
                else:
                    playedFirst = 'Player2'
    
                lstP2Factions = []
                for faction in match['info']['players'][0]['factions']:
                    lstP2Factions.append(faction[8:-5])
            else:
                player2 = 'Lab_Opponent'
                deck2 = 'Lab_Deck'
                lstP2Factions = []
                winner = ''
                playedFirst = 'Player1'
                gametype = 'Lab_of_Legends'
    
    
            row = { 'MatchID': match['metadata']['match_id'] ,
                    'GameMode': match['info']['game_mode'], 
                    'GameType': gametype, 
                    'Player1': player1,
                    'P1DeckCode': deck1,
                    'P1Factions': lstP1Factions,
                    'Player2': player2,
                    'P2DeckCode': deck2,
                    'P2Factions': lstP2Factions,
                    'Winner': winner,
                    'PlayedFirst': playedFirst,
                    'NumOfTurns': match['info']['total_turn_count']}
            table.append(row)
        except:
            print('Match analyze unsuccessful.')
    return table


def saveCSV(data, name):
    filename = str(name) + 'MatchData.csv'
    with open(filename, 'a', newline='') as file:         
        writer = csv.writer(file)
        writer.writerow(['MatchID','GameMode', 'GameType', 'Player1', 'P1DeckCode', 'P1Factions', 'Player2', 'P2DeckCode', 'P2Factions', 'Winner', 'PlayedFirst','NumOfTurns'])
        for line in data:
            row = line['MatchID'], line['GameMode'], line['GameType'], line['Player1'], line['P1DeckCode'], line['P1Factions'], line['Player2'], line['P2DeckCode'], line['P2Factions'], line['Winner'], line['PlayedFirst'], line['NumOfTurns'], '\n'
            writer.writerow(row)
            

def updateDataWarehouse(data):
    driver = 'Driver={SQL Server};'
    server = 'SPARROW'
    database = 'LoRMatchData'
    table = 'DataStagingTable'
    connection = 'UID=BICert;PWD=BICert'
    conn = pyodbc.connect(driver + 'Server=' + server + ";" + 'Database=' + database + ";" + connection)
    cursor = conn.cursor()
  
    for row in data:
        try:
            P1Faction1 = row['P1Factions'][0]
        except:
            P1Faction1 = "NoFaction"

        try:
            P1Faction2 = row['P1Factions'][1]
        except:
            P1Faction2 = "NoFaction"

        try:
            P2Faction1 = row['P2Factions'][0]
        except:
            P2Faction1 = "NoFaction"

        try:
            P2Faction2 = row['P2Factions'][1]
        except:
            P2Faction2 = "NoFaction"

        code = 'insert into ' + table + " (MatchID, GameMode, GameType, Player1, P1DeckCode, P1Faction1, P1Faction2, Player2, P2DeckCode, P2Faction1, P2Faction2, Winner, PlayedFirst, NumOfTurns) VALUES ('" + row['MatchID'] + '\',\'' + row['GameMode'] + '\',\'' + row['GameType'] + '\',\'' + row['Player1'] + '\',\'' + row['P1DeckCode'] + '\',\'' + P1Faction1 + '\',\'' + P1Faction2 + '\',\'' + row['Player2'] + '\',\'' + row['P2DeckCode'] + '\',\'' + P2Faction1 + '\',\'' + P2Faction2 + '\',\'' + row['Winner'] + '\',\'' + row['PlayedFirst'] + '\',\'' + str(row['NumOfTurns']) + '\')'
        cursor.execute(code)
    conn.commit()

    
def dataFromCSV(data, name):
    pass



if __name__ == '__main__':
# if Live:
    for player in [Hugh, Jake, Adam, Steven, Alex, Noble, Nico]:
        puuid = callAccountLookup(player[1], player[2])
        print(player[0] + ' puuid - success.')
        
        matches = callMatchList(puuid)
        print(player[0] + ' matches - success.')
        
        rawData = callMatchLookup(matches)
        print(player[0] + ' raw data pull - success.')
        
        print(rawData)
        
        matchData = analyzeData(rawData)
        print(player[0] + ' analyze data - success.')
        
        updateDataWarehouse(matchData)
        print(player[0] + ' Update SQL - success.')
        
    #            saveCSV(matchData, player[0])
        print(player[0] + ' - Success')
        # except:
        #     print('Error loading ' + player[0])

            
# if Testing:
    # matchData = analyzeData(testData)
    # updateDataWarehouse(matchData)
    # saveCSV(matchData, 'Adam')
    

    
    
    