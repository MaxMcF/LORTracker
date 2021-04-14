/****************************************************************************************
Dev: AHockemeyer
Date: 4/8/2021
Desc: Creates data warehouse for LoR Match History
ChangeLog: (Who, When, What) 
*****************************************************************************************/
Use Master;
go

If Exists (Select * From Sys.databases where Name = 'LoRMatchData')
  Begin
   Alter Database LoRMatchData set single_user with rollback immediate;
   Drop Database LoRMatchData;
  End
go

Create Database LoRMatchData;
go

Use LoRMatchData;
go


Create Table DataStagingTable (
	  GameKey int Constraint pkGameKey Primary Key Identity 
	, MatchID nvarchar(255) null
	, GameMode nvarchar(100) null
	, GameType nvarchar(100) null
	, Player1 nvarchar(255) null
	, P1DeckCode nvarchar(255) null
	, P1Faction1 nvarchar(100) null
	, P1Faction2 nvarchar(100) null
	, Player2 nvarchar(255) null
	, P2DeckCode nvarchar(255) null
	, P2Faction1 nvarchar(100) null
	, P2Faction2 nvarchar(100) null
	, Winner nvarchar(255) null
	, PlayedFirst nvarchar(255) null
	, NumOfTurns int
	);
go



Create Table DimKeywords (
	  KeywordKey int Constraint pkKeywordKey Primary Key Identity 
	, KeywordDescription nvarchar(255) null
	, KeywordName nvarchar(50) Not Null
	, KeywordNameRef nvarchar(50) Not Null
	);
go


Create Table DimRegions (
	  RegionKey int Constraint pkRegionKey Primary Key Identity 
	, RegionName nvarchar(50) null
	, RegionNameRef nvarchar(50) Not Null
	, RegionAbbreviation nvarchar(5) Not Null
	, RegionIconAbsolutePath nvarchar(255) Not Null
	);
go


Create Table DimSets (
	  SetKey int Constraint pkSetKey Primary Key Identity 
	, SetName nvarchar(50) Not Null
	, SetNameRef nvarchar(50) Not Null
	, SetIconAbsolutePath nvarchar(255) Not Null
	);
go


Create Table DimCards (
	  CardKey int Constraint pkCardKey Primary Key Identity 
	, CardName nvarchar(50) Not Null
	, CardFaction nvarchar(50) Not Null
	);
go


Create Table DimPlayers (
	  PlayerKey int Constraint pkPlayerKey Primary Key Identity 
	, PlayerName nvarchar(50) null
	, PlayerID nvarchar(50) Not Null
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



-- delete from DataStagingTable where GameKey < 0
-- select * from DataStagingTable