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
import os
from dotenv import load_dotenv
from ImportDimensionData import DBConnection
load_dotenv()



class APICaller(DBConnection):
    def __init__(self):
        super().__init__()
        self.base_url = 'https://americas.api.riotgames.com'
        self.headers = {'X-Riot-Token': os.environ.get('API_KEY')}


    def callAccountLookup(self, gameName, tagLine):
        url = self.base_url + f'/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}'
        status = requests.get(url, headers=self.headers)
        response = status.json()
        return response['puuid']


    def callMatchList(self, puuid):
        url = self.base_url + f'/lor/match/v1/matches/by-puuid/{puuid}/ids'
        status = requests.get(url, headers=self.headers)
        response = status.json()
        return response


    def callMatchLookup(self, matches):
        data = []
        for matchId in matches:
            url = self.base_url + f'/lor/match/v1/matches/{matchId}'
            status = requests.get(url, headers=self.headers)
            response = status.json()
            data.append(response)
        return data


    def convertJSONtoDF(self, matches):

        # Define target dataframe lists
        MatchInfoList = []
        MatchPlayerList = []

        # Unpack/restructure object into 3 models: MatchInfo, MatchPlayer
        for match in matches:
            MatchObject = {**match['metadata'], **match['info']}
            for player in MatchObject['players']:
                MatchPlayer = {'match_id': MatchObject['match_id'], **player}
                MatchPlayer['factions'] = ', '.join(MatchPlayer['factions'])
                MatchPlayerList.append(MatchPlayer)
            del MatchObject['players']
            del MatchObject['participants']
            MatchInfoList.append(MatchObject)

        # Define Dataframes based on lists
        df_MatchInfo = pd.DataFrame(MatchInfoList)
        df_MatchPlayer = pd.DataFrame(MatchPlayerList)

        return (df_MatchInfo, 'matchInfo'), (df_MatchPlayer, 'matchPlayer')

    
    def uploadDataFrametoSQL(self, df, tableName):
        df.to_sql(tableName, self.engine, if_exists='append', index=False)
    

if __name__ == '__main__':
    Hugh = ['Hugh', 'iswhtw', 'NA1']
    # Jake = ['Jake', 'DoctorBeeves', '0229']
    # Adam = ['Adam', 'Heliotropite', 'NA1']
    # Steven = ['Steven', 'iPhone 4', 'NA1']
    # Alex = ['Alex', 'mmmmmBAAAACOOON', 'NA1']
    # Noble = ['Noble', 'Noblescute', 'moc']
    # Nico = ['Nico', 'ClosingThyme', 'NA1']
    # Max = ['Max', '', '']

    apicall = APICaller()
    # players = [Hugh, Jake, Adam, Steven, Alex, Noble, Nico]
    players = [Hugh]
    for player in players:
        puuid = apicall.callAccountLookup(*player[1:])
        matchList = apicall.callMatchList(puuid)
        data = apicall.callMatchLookup(matchList)
        for dfOutput in apicall.convertJSONtoDF(data):
            apicall.uploadDataFrametoSQL(*dfOutput)


    
    