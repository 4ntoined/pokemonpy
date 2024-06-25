# Anybody here play Pokémon?
Just me? That's fine.

This program is a text-based game that simulates Pokémon and Pokémon battles and runs right in the terminal.
For a more detailed description of the game, check out [game_blurb.md](https://github.com/4ntoined/pokemonpy/blob/master/documentation/game_blurb.md).
For a demonstration of how to play the game, check out [this YouTube video](https://youtu.be/0SFg-sSOZBY) (and like and comment and subscribe).

## Installing the game
There are 3 methods to install and play the game. All methods require (1) access to the command line and (2) Python 3.

#### Access to the command line/terminal:
   - Search your computer for 'terminal' or 'command line'.
   - Mac and Linux are pretty straightforward about the terminal. For Windows, you'll probably want to use PowerShell and NOT the command prompt.
#### Python:
   - Python 3.7(ish) or later
   - https://www.python.org
   - For Windows players check out: https://learn.microsoft.com/en-us/windows/python/beginners

All of the code snippets in this doc presume you are using a terminal on a Linux machine. Things might be slightly different if you are on Mac or Windows.
For example, `python3` might be `py` or `Python` on Windows. You know your machine better than I do. Do what works.

### Method 1. pip (recommended)
The game is available on the Python Package Index [(package here)](https://pypi.org/project/pokemonpy/) and can be installed via [pip](https://packaging.python.org/en/latest/tutorials/installing-packages/):

`pip install pokemonpy`

Once installed, the game can be started by:
1. starting a live session of Python: `python3`
2. importing the package, initializing the game object, and starting the game:
```
import pokemonpy.pokemon as pk
game1 = pk.game()
game1.startgame()
```

### Method 2. conda (recommended if you prefer conda)
Similarly to Method 1, the game is available as a package through the [Anaconda distribution](https://www.anaconda.com/data-science-platform) of Python [(package here)](https://anaconda.org/antoi/pokemonpy) and can be installed with [conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html):

`conda install antoi::pokemonpy`

Game start instructions are the same as for pip:
```
python3
import pokemonpy.pokemon as pk
game1 = pk.game()
game1.startgame()
```

There are optional inputs for the startgame() function:
```
pokemonpy.pokemon.game.startgame(
    configname='config.txt', mutegame=(True or False), username="Your Name", opponentname="Op Name", nparty=1, nstart=6, gw=64)

configname - str, to have the game use a particular configuration file
mutegame - bool, set to True to skip the pre-game text
username - str, your name
opponentname - str, the name of the rival trainer
nparty - int, number of Pokémon parties you start with
nstart - int, number of Pokémon in each party
gw - int, sets the length of banners and headers
```

### Method 3. This github repository (not recommended, should work fine though)
This is the classic way to play the game, but it is a little more cumbersome than the other methods.

This method requires you to install [numpy](https://numpy.org/doc/stable/index.html). Using Methods 1 and 2, pip/conda will install numpy for you.

1. Clone/download this Github repository (https://www.github.com/4ntoined/pokemonpy) to your computer.
	- A few ways to do this:
	- Bright green 'Code' button near the top of the repo page -> Download ZIP -> Unzip the .zip you just downloaded.
	- 'Releases' panel on the right-hand side of the repo page -> Choose a release -> Download the source code -> Unzip the file you just downloaded.
	- If you have [git](https://github.com/git-guides/install-git) installed on your computer, use `git clone https://github.com/4ntoined/pokemonpy.git` in terminal.
2. Navigate to the 'pokemonpy' folder from your terminal: `cd /your/path/to/the/folder/here/pokemonpy/`
3. Enter `python3 pokemon.py`

Starting with optional inputs:

`python3 pokemon.py -m -c config_file_path -n "your name" -o "rivals name" -w how_big_to_display_the_game -p number_of_starter_parties -s number_of_pokémon_per_party`

- '-m' to mute the game start-up
- '-c' to tell the game to use a particular configuration file
- '-n' to set your name, used to display in battles
- '-o' to set the name of the rival trainer in the Battle! mode.
- '-w' to set the length of banners and headers throughout the game, defaults to 64 I think
- '-p' to set the number of parties you start with
- '-s' to set the number of Pokémon in each of those parties
- '-h' to have all of this told to you again but by python

## Editing the game:
Idk fam, follow your heart.

#### Adding moves, moves.py
You can add moves by adding them to moves.py. You'll find the construction of a list of tuples (it's hard to miss). Each of these tuples is a move. To add new moves, add your own tuples to this list.
You'll need to specify the move's name, its base power, accuracy, max PP, priority, type, category, whether it makes contact, a description, and "notes."
(Refer to the commenting within the script itself to get the order of the things right I definitely just butchered it.) The "notes" is where a move's mechanics are detailed. E.g. "burn 10" indicates a 10% chance to burn the target. "2turn" indicates a 2-turn move, like Dive or Fly, "mustRest" for Hyper Beams and Giga Impacts. "highCrit" for moves with increased critical hit ratios. Etc, etc.

Stats are raised and lowered using `stat A,B,C,D` where A=(self or targ) whose stats to change, B=(at,de,sa,sd,sp,ev,ac) what stat to change, C=(-6 to +6) how many stages to change and in what direction, D=(0 to 100) what percent chance is there for the stat change to occur.
Multiple stats can be changed at once using colons. E.g. Agility looks like `stat self,sp,+2,100`, Leer = `stat targ,de,-1,100`, Dragon Dance = `stat self,at:sp,+1:+1,100:100`

#### Adding Pokémon, somemons.dat
Add Pokémon to the Pokédex by appending them to somemons.dat. You'll need to specify their name, typing, and base stats, and I think that's it. And the index. I don't know what happens if you don't follow the sequence of indeces. Do it and let me know how it works out. I'll get around to adding Gen IX at some point. Or you can do it!

#### pokemon.py
This script runs the game. It kind of actually _is_ the game where everything else in this repo is a means to that end. I built it in pieces, so some pieces are a lot older and messier than others.
Like the rough edges are still there, in the timing of certain printouts in the consistency with which newlines are placed in the battling simulation itself. I figured I would at some point get around to ironing out all the wrinkles and honestly I got a lot of them, but there a lot still left.
But _I_ think my game is cool.

You can add your own 'mode' accessible from the main menu by creating a `if userChoice=='whatever you want someone to press to access your mode':` block and go ham.

#### base_pokemon.py
Everything that pokemon.py does, it can do because it's in this script. (From terminal) I like to start a live session of python and then:
```
from pokemonpy.base_pokemon import *
parties, fields = maker(2,6,2)
bb = battle(parties[0],parties[1],fields[0],usr_name='Your Name',cpu_name='The Ops')
bb.startbattle()
```

That's a Pokémon battle in 4 lines. I'm a legend.

Try:
```
from pokemonpy.base_pokemon import *
parties, fields = maker(2,6,2)
print_party(parties[0])
parties[0][0].summary()
parties[0][0].appraisal()
parties[0][0].save('poke.sav')
```

#### victoryroad.py
This script constructs the Elite 4 + Champion.

#### trainerai.py
This script contains the logic for the cpu opponent in the RIVAL battle and the e4+champion. Unfinished. It has no means of evaluating status moves, and uses them at random.
But it is brutal with damaging moves, favoring super-effective and STAB moves. Maybe I need to tone this down? Don't know. Let me know.

#### texter.py
Contains a bunch of functions that deal solely with text. I wanted to definitely separate them from the web of interdependent codes between base_pokemon.py and pokemon.py.
So they are here. Fun stuff, can easily be repurposed for other purposes.

#### dexpoke.py
This script turns somemons.dat into a numpy structured array that pokemon.py uses.

The game is an incomplete, imperfect imitation of Pokémon by GameFreak, and it is not completely bug-proof. Also, it is ripe for optimization.
There's a lot of repeated code (checking to see if a Pokémon needs to take poison damage is functionally the same as checking if a Pokémon needs to take burn damage, yet these things happen separately), and I'm sure a lot of what I've done here can be condensed using for loops and modularizing stuff with functions.
But, as is, it works really well if you don't try to break it.

Otherwise, yeah if any of this interested you at all please take it and run with it. I had a lot of fun writing and testing all this code and ultimately just playing a worse version of a game I already love.
But also the more I add to this, the closer I get to the Sun, the more I realize how much more there is to do and fix and reconsider.
Items! Abilities! PvP! Double battles! The Sun is so far away. But if _you_ can do that, any of that, any serious improvements on this stuff, I would actually literally love to see it.
