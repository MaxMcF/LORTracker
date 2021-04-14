# -*- coding: utf-8 -*-
"""
Dev: AHockemeyer
Date: 4/11/2021
Desc: Inserts data into LoRMatchData Dimension tables
ChangeLog: (Who, When, What) 
"""

import pymysql
import os
import json
from pathlib import Path
from dotenv import load_dotenv


load_dotenv()
DB_HOST = os.environ.get('DB_HOST')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
DB_PORT = os.environ.get('DB_PORT')
DB_SCHEMA = os.environ.get('DB_SCHEMA')
lstSetFileNames = ['set1', 'set2', 'set3', 'set4']

def importCardData(setFileName):
    f = Path(f"SetMetadata/{setFileName}/en_us/data/{setFileName}-en_us.json") 
    with open(f, 'r', encoding='utf8') as fileObj:
        data = json.load(fileObj)
        cardList = []
        for item in data:
            cardDict = {  'CardName':''
                    	, 'AssociatedCards':''
                    	, 'AssociatedCardRefs':''
                    	, 'GameAbsolutePath':''
                    	, 'FullAbsolutePath':''
                    	, 'Region':''
                    	, 'RegionRef':''
                    	, 'Attack':''
                    	, 'Cost':''
                    	, 'Health':''
                    	, 'Description':''
                    	, 'DescriptionRaw':''
                    	, 'LevelUpDescription':''
                    	, 'LevelUpDescriptionRaw':''
                    	, 'FlavorText':''
                    	, 'ArtistName':''
                    	, 'CardCode':''
                    	, 'KeywordList':''
                    	, 'KeywordRefList':''
                    	, 'SpellSpeed':''
                    	, 'SpellSpeedRef':''
                    	, 'Rarity':''
                    	, 'RarityRef':''
                    	, 'Subtype':''
                    	, 'SubtypeList':''
                    	, 'Supertype':''
                    	, 'CardType':''
                    	, 'Collectible':''
                    	, 'CardSet':''
                        }
            cardDict.update({'CardName':item['name']})
            cardDict.update({'Region':item['region']})
            cardDict.update({'RegionRef':item['regionRef']})
            cardDict.update({'Attack':item['attack']})
            cardDict.update({'Cost':item['cost']})
            cardDict.update({'Health':item['health']})
            cardDict.update({'Description':item['description']})
            cardDict.update({'DescriptionRaw':item['descriptionRaw']})
            cardDict.update({'LevelUpDescription':item['levelupDescription']})
            cardDict.update({'LevelUpDescriptionRaw':item['levelupDescriptionRaw']})
            cardDict.update({'FlavorText':item['flavorText']})
            cardDict.update({'ArtistName':item['artistName']})
            cardDict.update({'CardCode':item['cardCode']})
            cardDict.update({'SpellSpeed':item['spellSpeed']})
            cardDict.update({'SpellSpeedRef':item['spellSpeedRef']})
            cardDict.update({'Rarity':item['rarity']})
            cardDict.update({'RarityRef':item['rarityRef']})
            cardDict.update({'Subtype':item['subtype']})
            cardDict.update({'SubtypeList':item['subtypes']})
            cardDict.update({'Supertype':item['supertype']})
            cardDict.update({'CardType':item['type']})
            cardDict.update({'Collectible':item['collectible']})
            cardDict.update({'CardSet':item['set']})
            
            lstAssociatedCards = []
            for card in item['associatedCards']:
                lstAssociatedCards.append(card)
            cardDict.update({'AssociatedCards':lstAssociatedCards})
                
            lstAssociatedCardsRefs = []
            for card in item['associatedCardRefs']:
                lstAssociatedCardsRefs.append(card)
            cardDict.update({'AssociatedCardRefs':lstAssociatedCardsRefs})
                
            lstKeywords = []
            for keyword in item['keywords']:
                lstKeywords.append(keyword)
            cardDict.update({'Keywords':lstKeywords})
                
            lstKeywordRefs = []
            for keyword in item['keywordRefs']:
                lstKeywordRefs.append(keyword)
            cardDict.update({'KeywordRefs':lstKeywordRefs})
            
            for asset in item['assets']:    
                cardDict.update({'GameAbsolutePath':asset['gameAbsolutePath']})
                cardDict.update({'FullAbsolutePath':asset['fullAbsolutePath']})


            cardList.append(cardDict)
    return cardList

def insertCardData(data):
    conn = pymysql.connect(host=DB_HOST,
                             user=DB_USER,
                             password=DB_PASS,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

    cursor = conn.cursor()
    
    table = 'DimCards'
    code = 'insert into ' + table + " (CardName, AssociatedCards, AssociatedCardRefs, GameAbsolutePath, FullAbsolutePath, Region, RegionRef, Attack, Cost, Health, Description, DescriptionRaw, LevelUpDescription, LevelUpDescriptionRaw, FlavorText, ArtistName, CardCode, KeywordList, KeywordRefList, SpellSpeed, SpellSpeedRef, Rarity, RarityRef, Subtype, SubtypeList, Supertype, CardType, Collectible, CardSet) VALUES ("
    for row in data:
        codeLine = '\'' + row[0].replace("'", "") + '\',\'' + row[1].replace("'", "") + '\',\'' + row[2].replace("'", "") + '\'),('
        code = code + codeLine
    cursor.execute(code[:-2])
    conn.commit()
    print(table + ' Table Populated.')


def importDimensionData():
    f = Path(f"StaticMetadata/en_us/data/globals-en_us.json") 
    with open(f, 'r') as fileObj:
        data = json.load(fileObj)
        vocabList = []
        keywordList = []
        regionList = []
        setList = []
        for item in data["vocabTerms"]:
            row = [item["name"], item["nameRef"], item["description"]]
            vocabList.append(row)
            
        for item in data["keywords"]:
            row = [item["name"], item["nameRef"], item["description"]]
            keywordList.append(row)
            
        for item in data["regions"]:
            row = [item["name"], item["nameRef"], item["iconAbsolutePath"], item["abbreviation"]]
            regionList.append(row)

        for item in data["sets"]:
            row = [item["name"], item["nameRef"], item["iconAbsolutePath"]]
            setList.append(row)
            
    return vocabList, keywordList, regionList, setList

def insertVocabData(data):
    conn = pymysql.connect(host=DB_HOST,
                             user=DB_USER,
                             password=DB_PASS,
                             database=None,

                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

    cursor = conn.cursor()

    table = 'DimVocab'
    code = 'insert into ' + table + " (VocabDescription, VocabName, VocabNameRef) VALUES ("
    for row in data:
        codeLine = '\'' + row[0].replace("'", "") + '\',\'' + row[1].replace("'", "") + '\',\'' + row[2].replace("'", "") + '\'),('
        code = code + codeLine
    cursor.execute(code[:-2])
    conn.commit()            
    print(table + ' Table Populated.')

def insertKeywordData(data):
    conn = pymysql.connect(host=DB_HOST,
                             user=DB_USER,
                             password=DB_PASS,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

    cursor = conn.cursor()
    
    table = 'DimKeywords'
    code = 'insert into ' + table + " (KeywordDescription, KeywordName, KeywordNameRef) VALUES ("
    for row in data:
        codeLine = '\'' + row[0].replace("'", "") + '\',\'' + row[1].replace("'", "") + '\',\'' + row[2].replace("'", "") + '\'),('
        code = code + codeLine
    cursor.execute(code[:-2])
    conn.commit()            
    print(table + ' Table Populated.')

def insertRegionData(data):
    conn = pymysql.connect(host=DB_HOST,
                             user=DB_USER,
                             password=DB_PASS,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

    cursor = conn.cursor()
    table = 'DimRegions'
    code = 'insert into ' + table + " (RegionName, RegionNameRef, RegionIconAbsolutePath, RegionAbbreviation) VALUES ("
    for row in data:
        codeLine = '\'' + row[0].replace("'", "") + '\',\'' + row[1].replace("'", "") + '\',\''  + row[2].replace("'", "") + '\',\'' + row[3].replace("'", "") + '\'),('
        code = code + codeLine
    cursor.execute(code[:-2])
    conn.commit()            
    print(table + ' Table Populated.')

def insertSetData(data):
    conn = pymysql.connect(host=DB_HOST,
                             user=DB_USER,
                             password=DB_PASS,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

    cursor = conn.cursor()
    table = 'DimSets'
    code = 'insert into ' + table + " (SetName, SetNameRef, SetIconAbsolutePath) VALUES ("
    for row in data:
        codeLine = '\'' + row[0].replace("'", "") + '\',\'' + row[1].replace("'", "") + '\',\'' + row[2].replace("'", "") + '\'),('
        code = code + codeLine
    cursor.execute(code[:-2])
    conn.commit()            
    print(table + ' Table Populated.')


if __name__ == '__main__':

    dimData = importDimensionData()

    insertVocabData(dimData[0])
    insertKeywordData(dimData[1])
    insertRegionData(dimData[2])
    insertSetData(dimData[3])

    # print(importCardData('set1'))
    
    # cardDictList = []
    # for fileName in lstSetFileNames:
    #     cardDictList = cardDictList + importCardData(fileName)
    
    # insertCardData(cardDictList)
    
    
    
    
    