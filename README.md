# Anybody here play Pokémon?
Just me? That's fine.

This program is a text-based game that simulates Pokémon and Pokémon battles and runs right in the terminal.
For a more detailed description of the game, check out [game_blurb.md](https://github.com/4ntoined/pokemonpy/blob/master/documentation/game_blurb.md).
For a demonstration of how to play the game, check out [this YouTube video](https://youtu.be/0SFg-sSOZBY).
The game is maintained here: https://github.com/4ntoined/pokemonpy-package.

## Installing the game
Installing and playing the game requires (1) access to the command line and (2) Python 3.

#### Access to the command line/terminal:
   - Search your computer for 'terminal' or 'command line'.
   - On Windows, you'll probably want to use PowerShell and NOT the Command Prompt (cmd.exe).
   - Alternatively, there is [Windows Subsystem for Linux](https://learn.microsoft.com/en-us/windows/wsl/install), which gives you a Linux-like command line environment, if you're willing to jump through a few hoops. This is my preferred way to play in Windows as I have no idea how to use PowerShell.
#### Python:
   - Python 3.9 or later
   - https://www.python.org
   - For Windows players check out: https://learn.microsoft.com/en-us/windows/python/beginners

### pip
The game is available on the Python Package Index [(package here)](https://pypi.org/project/pokemonpy/) and can be installed via [pip](https://packaging.python.org/en/latest/tutorials/installing-packages/):

```
pip install pokemonpy
```

### conda
The game is also available as a package through the [Anaconda distribution](https://www.anaconda.com/data-science-platform) of Python [(package here)](https://anaconda.org/antoi/pokemonpy) and can be installed with [conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html):

```
conda install antoi::pokemonpy
```

## Starting the game
With the package installed, you can start the game using the `rungame.py` script [found here](https://github.com/4ntoined/pokemonpy-package/blob/d02cc526a1b903d4ffbf25067d265481353a8274/src/pokemonpy/scripts/rungame.py).
(Technically, it is already downloaded with all the other source files for the package, but that might be less accessible to you than the previous link.)
However you find the script on your computer, run it with:

```
python3 your/path/here/rungame.py
```

You can give the script some optional arguments when you call it:

```
python3 ./rungame.py -m -c config_file_path -n "your name" -o "rival's name" -w how_wide_to_display_the_game -p number_of_starter_parties -s number_of_pokémon_per_party

-m to skip the game start-up
-c to have the game use a particular configuration file
-n to set your name
-o to set the name of your opponent in the Battle! mode
-w to set the length of banners and headers
-p to set the number of Pokémon parties you start with
-s to set the number of Pokémon in each party
-h to have all of this told to you again but by Python
```

Alternatively, you can:

1. start a live session of Python:

```
python3
```

2. import the package, initialize the game object, and start the game:

```
import pokemonpy.pokemon as pk
game1 = pk.game()
game1.startgame()
```

The options for the startgame() function:

```
pokemonpy.pokemon.game.startgame(
    configname='config.txt', mutegame=(True or False), username="Your Name", opponentname="Rival's Name", nparty=1, nstart=6, gw=64)

configname - str, to have the game use a particular configuration file
mutegame - bool, set to True to skip the game start-up text
username - str, your name
opponentname - str, the name of your opponent in the Battle! mode
nparty - int, number of Pokémon parties you start with
nstart - int, number of Pokémon in each party
gw - int, sets the length of banners and headers
```

## Some fun things to try with the package

Start a battle:
```
from pokemonpy.base_pokemon import *
parties, fields = maker(2, 6, 2)
bb = battle(parties[0], parties[1], fields[0], usr_name = 'Your Name', cpu_name = 'The Opps')
bb.start_withai( cpu_logic = 'random' )
```

Make a party and save the first Pokémon: 
```
from pokemonpy.base_pokemon import *
parties, fields = maker( 2, 6, 2)
print_party(parties[0])
parties[0][0].summary()
parties[0][0].appraisal()
parties[0][0].save('poke.sav')
```

Make and save an Elite 4:
```
## this script will create a new elite 4 (or elite n, where n is some positive integer) and save them to pokemonpy save files

import numpy as np
import pokemonpy
import pokemonpy.base_pokemon as bp

rng = np.random.default_rng()

bp.game_width = 64      # sets the length of banners and headers and textwrap
n = 4                   # number of trainers
p = 6                   # number of Pokémon for each trainer
l = 200                 # Pokémon level
m = 4                   # number of moves to add onto the default; default is 6
savename = 'save.sav'   # savefile where the trainers are saved

parties, fields = bp.maker(n, p, n, level=l, how_created='elite')   # create n random 'elite' parties and n randomized battlefields
trainer_names = rng.choice(bp.easter_strings,n,replace=True)        # select 'names' from a list of strings in the game's code

# these for loops train all the Pokémon and saves each party
for i in range(n):
    # iterating over each party
    for a in parties[i]:
        # iterating over each Pokémon in the party
        # a is a pokémon
        a.perfect_ivs()
        a.full_evs()
        a.add_random_moves(number = m)
        #a.summary()   #uncomment to see all the elite Pokémon summaries
        #a.appraise()  #uncomment for base stat breakdown
        pass
    bp.saveParty(savename, parties[i], overwrite=True)                        # save the party to a joint save
    bp.saveParty(trainer_names[i]+'.sav', parties[i], overwrite = True)       # save the party to its own save, might get appended with another party if they happen to have the same random name
    pass
```

Make and battle an Elite 4!
```
## this script will create an elite n and a party for the user and set the user against the elite n in succession

import numpy as np
import pokemonpy
import pokemonpy.base_pokemon as bp

rng = np.random.default_rng()

bp.game_width = 64      # sets the length of banners and headers and textwrap
n = 4                   # number of trainers
p = 6                   # number of Pokémon for each trainer
l = 200                 # Pokémon level
m = 4                   # number of moves to add onto the default; default is 6
myname = 'RED'          # your name

parties, fields = bp.maker(n, p, n, level=l, how_created='elite')   # create n random 'elite' parties and n randomized battlefields
trainer_names = rng.choice(bp.easter_strings,n,replace=True)        # select 'names' from a list of strings in the game's code

# a party for the player
mine = bp.makeParty(numb=int(p*2), level = int(l+50), how_created = 'starter')

# these for loops train each party and then initiates a battle against them
for i in range(n):
    # iterating over each party
    for a in parties[i]:
        # iterating over each Pokémon in the party
        # a is a pokémon
        a.perfect_ivs()
        a.full_evs()
        a.add_random_moves(number = m)
        #a.summary()   #uncomment to see all the elite Pokémon summaries
        #a.appraise()  #uncomment for base stat breakdown
        pass
    # heal before battle
    for b in mine:
        b.withdraw()
        b.restore()
    # battle the party
    bb = bp.battle(mine,parties[i],fields[i],usr_name=myname,cpu_name=trainer_names[i])
    bb.start_withai(e4=True)
    pass
```

Move Catalog:
```
import pokemonpy
import pokemonpy.base_pokemon as bp
from pokemonpy.texter import magic_text

bp.game_width = 64      # sets the length of banners and headers and textwrap

for i in range(len(bp.mov)):
    bp.moveInfo(i, index=True) # displaying move info
    print("\n\n",end="")
```
What else...?
