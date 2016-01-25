#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach


def connect(database_name="tournament"):
    """Connect to the PostgreSQL database.  Returns a database connection
    and a cursor."""
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except:
        print("<error message>")


def deleteMatches():
    """Remove all the match records from the database."""
    try:
        # Connect to the tournament database and remove all
        # matches from match table
        tournamentDB, cursor = connect()
        cursor.execute("DELETE FROM match")

        # Make the changes to the database persistent
        tournamentDB.commit()
    finally:
        # Close communication with the database
        cursor.close()
        tournamentDB.close()


def deletePlayers():
    """Remove all the player records from the database."""
    try:
        # Connect to the tournament database and remove all players
        # from player table
        tournamentDB, cursor = connect()
        cursor.execute("DELETE FROM player")

        # Make the changes to the database persistent
        tournamentDB.commit()
    finally:
        # Close communication with the database
        cursor.close()
        tournamentDB.close()


def countPlayers():
    """Returns the number of players currently registered."""
    try:
        # Connect to the tournament database and retrieve the number
        # of players in the player table
        playerCount = 0
        tournamentDB, cursor = connect()
        cursor.execute("SELECT count(*) FROM player")
        result = cursor.fetchone()

        if result is not None:
            playerCount = int(result[0])

        return playerCount

    finally:
        # Close communication with the database
        cursor.close()
        tournamentDB.close()


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    try:
        # Connect to the tournament database and insert players
        # into the player table
        tournamentDB, cursor = connect()
        cursor.execute("INSERT INTO player (name) VALUES (%s)",
                       (bleach.clean(name),))

        # Make the changes to the database persistent
        tournamentDB.commit()
    finally:
        # Close communication with the database
        cursor.close()
        tournamentDB.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a
    player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    try:
        # Connect to the tournament database and retrieve the players
        # standings sorted by wins
        tournamentDB, cursor = connect()
        cursor.execute("SELECT * FROM standings ORDER BY wins")
        standings = cursor.fetchall()

        return standings
    finally:
        # Close communication with the database
        cursor.close()
        tournamentDB.close()


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    try:
        # Connect to the tournament database and insert into the match
        # table the matches that have been played including the winners
        # and the losers
        tournamentDB, cursor = connect()
        cursor.execute("INSERT INTO match (winnerId, loserId) VALUES (%s, %s)",
                       (winner, loser))

        # Make the changes to the database persistent
        tournamentDB.commit()

    finally:
        # Close communication with the database
        cursor.close()
        tournamentDB.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    # Connect to the tournament database and retrieve the standings
    # sorted by wins
    pairings = []
    standings = playerStandings()

    # Check that standings list has values and that there are an even
    # number of players then loop through the standings row by row
    # to determine which players have won the same amount of matches.
    # Once identified, add the player to the pairing list
    print(len(standings))
    if standings is not None and len(standings) % 2 == 0:
        while standings:
            player1 = standings.pop()
            player1Wins = player1[2]
            for row in standings:
                player2 = row
                player2Wins = player2[2]
                if player1Wins == player2Wins:
                    pairings.append((player1[0], player1[1],
                                    player2[0], player2[1]))
                    standings.pop()

    return pairings
