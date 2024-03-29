# Anybody here play Pokémon?
Just me? That's fine.

This Python program simulates Pokémon and Pokémon battles.
For a more detailed description of the game, check out [game_blurb.md](https://github.com/4ntoined/pokemonpy/blob/lead_dev/documentation/game_blurb.md)
For a demonstration of how to play the game, check out [this guy's YouTube video](https://youtu.be/0SFg-sSOZBY) (and like and comment and subscribe, he told me to tell you that).
The rest of the readme will be geared toward codestuff: prerequisites, launching the game, and modifying the code to your tastes, etc.

### Prerequisites:
 - Python
 - Numpy

### Starting the game:
```python3 pokemon.py [-m] [-n your_name_here] [-w how_big_to_display_the_game] [-p number_of_starter_parties] [-s number_of_pokémon_per_party]```

all of these are optional inputs
- use '-m' to skip the game start-up
- use '-n' to set your name, you can set your name in-game, used to display in battles
- use '-w' to set the length of banners and headers throughout the game, defaults to 64 I think
- use '-p' to set the number of parties you start with
- use '-s' to set the number of Pokémon in each of those parties

### Editing the game:
Idk fam, follow your heart.

#### Adding moves
You can add moves by adding them to moves.py. You'll find the construction of a list of tuples (it's hard to miss). Each of these tuples is a move. To add new moves, add your own tuples to this list.
You'll need to specify the move's name, its base power, accuracy, max PP, priority, type, category, whether it makes contact, a description, and "notes."
(Refer to the commenting within the script itself to get the order of the things right I definitely just butchered it.) The "notes" is where a move's mechanics are detailed. E.g. "burn 10" indicates a 10% chance to burn the target.
Stats are raised and lowered using ```stat A,B,C,D``` where A=(self or targ) whose stats to change, B=(at,de,sa,sd,sp) what stat to change, C=(-6 to +6) how many stages to change and in what direction, D=(0 to 100) what percent chance is there for the stat change to occur
Multiple stats can be changed at once using colons. E.g. Agility looks like ```stat self,sp,+2,100```, Leer = ```stat targ,de,-1,100```, Dragon Dance = ```stat self,at:sp,+1:+1,100:100```
And there are very many more move effects.

#### Adding Pokémon
Add Pokémon to the Pokédex by appending them to somemons.dat. You'll need to specify their name, typing, and base stats, and I think that's it. And the index. I don't know what happens if you don't follow the sequence of indeces. Do it and let me know how it works out. I'll get around to adding Gen IX at some point. Or you can do it!

#### What else 

The game is incomplete, an imperfect imitation of Pokemon by GameFreak, and is not completely bug-proof. But it works really well if you don't try to break it.


