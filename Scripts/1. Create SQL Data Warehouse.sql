/****************************************************************************************
Dev: AHockemeyer
Date: 4/8/2021
Desc: Creates data warehouse for LoR Match History
ChangeLog: (Who, When, What) 
*****************************************************************************************/
USE LORTracker;

DROP TABLE DataStagingTable;
Create Table DataStagingTable (
	  GameKey int  NOT NULL AUTO_INCREMENT 
	, MatchID char(255) null
	, GameMode char(100) null
	, GameType char(100) null
	, Player1 char(255) null
	, P1DeckCode char(255) null
	, P1Faction1 char(100) null
	, P1Faction2 char(100) null
	, Player2 char(255) null
	, P2DeckCode char(255) null
	, P2Faction1 char(100) null
	, P2Faction2 char(100) null
	, Winner char(255) null
	, PlayedFirst char(255) null
	, NumOfTurns int
    , PRIMARY KEY(GameKey)
	);
go

Create Table DimVocab (
	  VocabKey int NOT NULL AUTO_INCREMENT
	, VocabDescription char(255) null
	, VocabName char(50) Not Null
	, VocabNameRef char(255) Not Null
    , PRIMARY KEY(VocabKey)
	);
go

Create Table DimKeywords (
	  KeywordKey int NOT NULL AUTO_INCREMENT
	, KeywordDescription char(255) null
	, KeywordName char(50) Not Null
	, KeywordNameRef char(255) Not Null
    , Primary Key(KeywordKey)
	);
go

Create Table DimRegions (
	  RegionKey int NOT NULL AUTO_INCREMENT
	, RegionName char(50) null
	, RegionNameRef char(255) Not Null
	, RegionAbbreviation char(5) Not Null
	, RegionIconAbsolutePath char(255) Not Null
    , primary key(RegionKey)
	);
go

Create Table DimSets (
	  SetKey int NOT NULL AUTO_INCREMENT
	, SetName char(50) Not Null
	, SetNameRef char(255) Not Null
	, SetIconAbsolutePath char(255) Not Null
    , Primary Key(SetKey)
	);
go

Create Table DimCards (
	  CardKey int NOT NULL AUTO_INCREMENT
	, CardName char(255) Not Null
	, AssociatedCards char(255) null
	, AssociatedCardRefs char(255) null
	, GameAbsolutePath char(255) null
	, FullAbsolutePath char(255) null
	, Region char(255) null
	, RegionRef char(255) null
	, Attack char(255) null
	, Cost char(255) null
	, Health char(255) null
	, `Description` char(255) null
	, DescriptionRaw char(255) null
	, LevelUpDescription char(255) null
	, LevelUpDescriptionRaw char(255) null
	, FlavorText char(255) null
	, ArtistName char(255) null
	, CardCode char(255) null
	, KeywordList char(255) null
	, KeywordRefList char(255) null
	, SpellSpeed char(255) null
	, SpellSpeedRef char(255) null
	, Rarity char(255) null
	, RarityRef char(255) null
	, Subtype char(255) null
	, SubtypeList char(255) null
	, Supertype char(255) null
	, CardType char(255) null
	, Collectible char(255) null
	, CardSet char(255) null
    , Primary Key(CardKey)
	)


Create Table DimPlayers (
	  PlayerKey int NOT NULL AUTO_INCREMENT
	, PlayerName char(50) null
	, PlayerID char(50) Not Null
    , Primary Key(PlayerKey)
	);
go


CREATE or ALTER PROCEDURE pInsTestData AS
	insert into DataStagingTable 
	( MatchID,
	  GameMode
	, GameType
	, Player1
	, P1DeckCode
	, P1Faction1
	, P1Faction2
	, Player2
	, P2DeckCode
	, P2Faction1
	, P2Faction2
	, Winner
	, PlayedFirst
	, NumOfTurns
	) values 
	('TestID1'
	,'Constructed'
	,'Ranked'
	,'JMAlVNY1hdxNWkn71q3QtBqzFGFQ9RtIqXmOqoXIJmR9yuOCY-maybE2wAvWkvoE4_O8QBflsNVzKg'
	,'CMCACAYABYBAIAACAMBQCAQJBQYQIAIABEISALIDAEAQEEQBAIAACAQBAAGRKAQBAEABUAICAIEQ'
	,'Demacia' 
	,'Ionia'
	,'srAFr4v22RM2P0Cu4OEbj_U19wF0iFC3yUfW6Motz1nzZPsgtk4XGdwd7nopD5sh3ATfm3BvzpEP0w'
	,'CMBQEAQAAIEQGAIABELDGBQEA4BRUHBTHFOQGAIBAANACAQAA4AQIAADAEAQIB2M'
	,'Demacia'
	, 'Ionia'
	,'Player1'
	,'Player1'
	,12
	)
go



CREATE or ALTER PROCEDURE pViewAll AS
	select * from DataStagingTable
	select * from DimVocab
	select * from DimKeywords
	select * from DimRegions
	select * from DimSets
	select * from DimPlayers
	select * from DimCards
go



pViewAll
go


