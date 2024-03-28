## Anybody here play Pokémon?

Pokemon.py is a text-based Python game that simulates Pokémon and Pokémon battles. Players start the game with a random party of Pokémon, each with a random moveset made from almost 200 moves. As a trainer, you're encouraged to try out a Trainer Battle against an opponent with a random team of their own. Don't care for your random party? You can create new Pokémon using a Pokédex of 920+ different Pokémon species and forms. Or, you can create your own Pokémon from scratch. Determine its base stats, typing, nature, and, most importantly, name, and it'll do battle right alongside Bulbasaur and Arceus. Don't forget to train them! Once you've conquered your rival, you might have what it takes to defeat the Elite 4 and their champion, five (5) trainers with specifically tailored teams and movesets. Beat them, and each of your Pokémon will be bestowed a title, recognizing their champion status. And when you're done, you can save your team(s) to simple text files or less-simple numpy.ndarrays, so they can be loaded into the game again in later play sessions.

### Breaking the rules!
The level-100 cap is dead and gone! Your Pikachu can be Level 999,999 if you want, the only limit is when your computer/Python decides the numbers are literally too big for it to compute. Any Pokémon can have any move and any number of moves! There's no limit on the size of your party! By abusing the save/load function, you can even ignore EV-limitation rules!

### Your turn!
Did I leave out your favorite 'mon or a move essential to your E4 strategy? Do it yourself! As a github repository, the whole program is public. If you can play it, you can also edit 'moves.py' or 'somemons.dat' to include your additions. (Adding moves with 'new functionality' (i.e. there is not already a move that has this particular effect) is a little more involved than editing 'moves.py,' but I think I'll explain all that in some other context.)

### Rapid-fire features I haven't mentioned yet:
 - The CPU opponent is kinda smart!! I programmed an algorithm that takes into account type advantages, phys/spec spectrum considerations, status effects, etc. You will get hit with STABS and super-effective moves a LOT!
 -  Pokémon keep track of how they were created: starters vs. nursery vs. randomized by Boxes. E4 + Champion Pokémon are marked as such. The game detects when a Pokemon.py save file has been 'tampered' with and marks this on affected Pokémon. And more!
 -  Teams made and saved by Pokémon Showdown! are mostly supported and loadable. (Pokémon with spaces in their names (Mr. Mime, Type: Null) will break this I think. Otherwise this was one of my masterstroke moves, ngl.)
 -  Make a team and then set it to be the rival trainer's team.
 -  Set the starting weather and terrain of the rival trainer battle.
 -  Special main menu banner after you beat the E4 + Champion.
 -  E4 + Champion teams are pre-saved and can be loaded into the game as your own.
 -  Multi-party support through "Boxes" on the main menu.
 -  Perfect all IVs of individual Pokémon or your whole party at once. Fully EV train individual Pokémon or your whole party at once (EVs are distributed randomly, but in multiples of 4 so none are wasted.)
