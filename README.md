# Swiss Pairing Tournament
This program keeps track of players and matches in a game tournament using the Swiss Pairing process. 
It includes a database component and a code code components.  The details of the database are located
in the tournament.sql file.  This file contains instructions for setting up the database.  The
tournament.py file contains the logic written in python that manages the players and the matches.
It also contains a unit test suite in the tournament_test.py which is used to test the program


To run the program, the first setup the database by executing tournament.sql 
(can use \i tournament.sql in psql command line.
the execute the media_enter file.  
The next step is executing the test suite by running 'python tournament_test.py'
at the command line.

