# CS238_Final_Bridge

## Language: Python

### Structure:
* Card
    value: 0-51
    * Spades: 39-51   	(i/13 == 3)
    * Heart: 26- 38 	(i/13 == 2)
    * Diamond: 13-25 	(i/13 == 1)
    * Clubs: 0-12 		(i/13 == 0) 


### Usage:
* `-v` / `--verbose`: Change the verbosity, an integer must be added behind the command. (Default: 1)
```
python3 main.py [-v int]
```

* `-i` / `--init`: Initial 4 players for the bridge game.
```
python3 main.py [-i]
```

* `-d` / `--dealing`: Start dealing the card to 4 players.
```
python3 main.py [-d]
```

* `-r` / `--redealing`: Check if the dealing process makes all the players get at least 4 points. If not, dealing again until all players get at least 4 points for their cards.
```
python3 main.py [-d]
```

# Test
```
python3 main.py -v 3 -i -d -r
```
