-- This file provide the database definitions for tournament database


-- Kill active connections before making changes to tournament database.
SELECT pg_terminate_backend(pg_stat_activity.pid)
FROM pg_stat_activity
WHERE pg_stat_activity.datname = 'tournament'
  AND pid <> pg_backend_pid();

-- Create new Database.  If the database already exists, remove it before
-- creating a new one.
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament;

-- Create the player table that contains all players
CREATE TABLE player (
    id serial PRIMARY KEY,
    name varchar(50) NOT NULL
);

-- Create the match table that contains all data related to matches
-- including which player won and which player lost.
CREATE TABLE match(
    id serial PRIMARY KEY,
    winnerId integer references player(id) ON DELETE CASCADE,
    loserId integer references player(id) ON DELETE CASCADE
);

ALTER table match
    ADD CHECK(winnerId <> loserId);


-- Create a standings views that displays the player standings including
-- how many matches the players have played and how many of the mathes
-- they won.
CREATE VIEW standings AS
SELECT mainPlayer.id, mainPlayer.name,
    (SELECT  count(*) AS wins FROM match
        WHERE mainPlayer.id = match.winnerId),
    (SELECT count(*) AS matches FROM match
        WHERE mainPlayer.id = match.winnerId OR mainPlayer.id = loserId)
FROM player AS mainPlayer
ORDER BY wins;
\q