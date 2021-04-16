# from pyspark import SparkContext
# import json
import pandas as pd

# sc = SparkContext('local', 'LORTracker')


data = {'metadata': {
    'data_version': '2',
    'match_id': 'ac6026e7-e7f1-46f9-b086-3793133b5c85',
                'participants': [
                    'swd0yx9Seb-X_DmAyl3GFuj2Do4tAdEkMrOOOXF6x_CmwZZyqMTKA2P8GXV7AKqs1rXkALhTGFDEYw',
                    'N3zoEngefZXpQVfcfawTs2-4H_V2gy1bVenVrilKyT-HPtrUlPenzpnjdTgQjN_sQm2aNkFjhkCUOg'
                ]
},
    'info': {
    'game_mode': 'Constructed',
    'game_type': 'Ranked',
    'game_start_time_utc': '2021-04-15T02:05:16.4471247+00:00',
    'game_version': 'live_2_6_11',
    'players': [
                    {
                        'puuid': 'swd0yx9Seb-X_DmAyl3GFuj2Do4tAdEkMrOOOXF6x_CmwZZyqMTKA2P8GXV7AKqs1rXkALhTGFDEYw',
                        'deck_id': '237708cf-83ca-4d07-a4a4-55fc4c93a9da',
                        'deck_code': 'CMBQCBAFBMCAGBIDAQCQMCADBERTQSKYLFOF5VQBAAAQCAYJF4',
                        'factions': [
                            'faction_MtTargon_Name',
                            'faction_ShadowIsles_Name'
                        ],
                        'game_outcome': 'loss',
                        'order_of_play': 0
                    },
        {
                        'puuid': 'N3zoEngefZXpQVfcfawTs2-4H_V2gy1bVenVrilKyT-HPtrUlPenzpnjdTgQjN_sQm2aNkFjhkCUOg',
                        'deck_id': 'e673f3d2-b77a-47ad-94a8-9eb48f630e92',
                        'deck_code': 'CMCACAIADIAQEAABAMBQABQIBYCQGCIJKZOGAZABAQBQSVCVK7OQCAQBAEAAOAIDBE4Q',
                        'factions': [
                            'faction_Demacia_Name',
                            'faction_MtTargon_Name'
                        ],
                        'game_outcome': 'win',
                        'order_of_play': 1
                    }
    ],
    'total_turn_count': 48}
}

MatchObject = {**data['metadata'], **data['info']}

df_MatchPlayer = pd.DataFrame(MatchObject['players'])    
del MatchObject['players']
df_MatchInfoPlayer = pd.DataFrame([{'match_id': MatchObject['match_id'], 'puuid': participant} for participant in MatchObject['participants']])
del MatchObject['participants']
df_MatchInfo = pd.DataFrame([MatchObject])


print(df_MatchPlayer.name)
# print(df_MatchInfoPlayer)
# print(df_MatchInfo)
