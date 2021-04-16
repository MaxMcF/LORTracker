# -*- coding: utf-8 -*-
"""
Dev: AHockemeyer
Date: 4/11/2021
Desc: Inserts data into LoRMatchData Dimension tables
ChangeLog: (Who, When, What) 
"""

import os
import json
from pathlib import Path
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine
load_dotenv()



class DBConnection():
    def __init__(self):
        host = os.environ.get('DB_HOST')
        user = os.environ.get('DB_USER')
        password = os.environ.get('DB_PASS')
        port = os.environ.get('DB_PORT')
        db_data = f'mysql+mysqlconnector://{user}:{password}@{host}:{port}/LORTracker?charset=utf8mb4'
        self.engine = create_engine(db_data)


class StaticImporter(DBConnection):
    def __init__(self):
        super().__init__()


    def importCardData(self, setFileName):
        f = Path(f"../SetMetadata/{setFileName}/en_us/data/{setFileName}-en_us.json") 
        df = pd.read_json(f)
        for column in ['associatedCards', 'associatedCardRefs', 'keywords', 'keywordRefs', 'subtypes']:
            df[column] = df[column].apply(', '.join)
        df = df.drop('assets', axis=1)
        df.to_sql('cards', self.engine, if_exists='append', index=False)


    def importDimensionData(self):
        f = Path(f"../StaticMetadata/en_us/data/globals-en_us.json") 
        with open(f, 'r') as fileObj:
            data = json.load(fileObj)
            for dimension in ['vocabTerms', 'keywords', 'regions', 'spellSpeeds', 'rarities', 'sets']:
                df = pd.DataFrame(data[dimension])
                df.to_sql(dimension, self.engine, if_exists='append', index=False)



if __name__ == '__main__':
    ConnObj = StaticImporter()
    for cardSet in ['set1', 'set2', 'set3', 'set4']:
        ConnObj.importCardData(cardSet)
    ConnObj.importDimensionData()
    
    
    