# LORTracker


## Purpose

We are exploring the Legends of Runeterra API for use in a data project. We intend on performing exploratory data analysis using the Player, Rank, and Match API endpoints, hopefully with the outcome of meta-game analysis.

## Endpoints

[Account](https://developer.riotgames.com/apis#account-v1/GET_getByRiotId):
	```f'/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}'```

[MatchList](https://developer.riotgames.com/apis#lor-match-v1/GET_getMatchIdsByPUUID):
	```f'/lor/match/v1/matches/by-puuid/{puuid}/ids'```

[MatchLookup](https://developer.riotgames.com/apis#lor-match-v1/GET_getMatch):
	```f'/lor/match/v1/matches/{matchId}'```


## Structure

We have set up a hosted DB to house the data we've gathered from the LOR API. This DB contains all the static assets available from the [LOR developer website](https://developer.riotgames.com/docs/lor).


## Future

We will likely develop a 3rd parth tool for in-game tracking in the future, but that is far away. 
