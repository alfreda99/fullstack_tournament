-- This file provide the database definitions for tournament database


-- Create new Datebase.  If the datbase already exists, remove it before
-- creating a new one.
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament;

-- Create the player table that contains all players
CREATE TABLE player (
    id serial PRIMARY KEY,
    name varchar(50) NOT NULL
);

-- Create the match table that contains all dats related to matches
-- including which player won and which player lost.
CREATE TABLE match(
    id serial PRIMARY KEY,
    winnerId integer references player(id),
    loserId integer references player(id)
);

-- Create a standings views that displays the player standings including
-- how many matches the players have played and how many of the mathes
-- they won.
CREATE VIEW standings AS
SELECT mainPlayer.id, mainPlayer.name,
    (SELECT  count(*) AS wins FROM match
        WHERE mainPlayer.id = match.winnerId),
    (SELECT count(*) AS matches FROM match
        WHERE mainPlayer.id = match.winnerId OR mainPlayer.id = loserId)
FROM player AS mainPlayer;
\q