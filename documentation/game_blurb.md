# Pokemon.py, Pokémon in Python

Pokemon.py is a text-based Python game that simulates Pokémon and Pokémon battles. Players start the game with a random party of Pokémon, each with a random moveset made from almost 200 moves. As a trainer, you're encouraged to try out a Trainer Battle against an opponent with a random team of their own. Don't care for your random party? You can create new Pokémon using a Pokédex of 920+ different Pokémon species and forms. Or, you can create your own Pokémon from scratch. Determine its base stats, typing, nature, and, most importantly, name, and it'll do battle right alongside Bulbasaur and Arceus. Don't forget to train them! Once you've conquered your rival, you might have what it takes to defeat the Elite 4 and their champion, five (5) trainers with specifically tailored teams and movesets. Beat them, and each of your Pokémon will be bestowed a title, recognizing their champion status. And when you're done, you can save your team(s) to simple text files or less-simple numpy.ndarrays, so they can be loaded into the game again in later play sessions.

### Breaking the rules!
The level-100 cap is dead and gone! Your Pikachu can be Level 999,999 if you want, the only limit is when your computer/Python decides the numbers are literally too big for it to compute. Any Pokémon can have any move and any number of moves! There's no limit on the size of your party! By abusing the save/load function, you can even ignore EV-limitation rules!

### Your turn!
Did I leave out your favorite 'mon or a move essential to your E4 strategy? Do it yourself! As a github repository, the whole program is public. If you can play it, you can also edit 'moves.py' or 'somemons.dat' to include your additions. (Adding moves with 'new functionality' (i.e. there is not already a move that has this particular effect) is a little more involved than editing 'moves.py,' but I think I'll explain all that in some other context.)

### Rapid-fire features I haven't mentioned yet:
 - The CPU opponent is kinda smart! I programmed an algorithm that takes into account type matchups, phys/spec damage considerations, status effects, etc. You will get hit with STABs and super-effective moves a LOT!
 -  Pokémon keep track of when, where, and how they were created: starters vs. nursery vs. randomized by Boxes. E4 + Champion Pokémon are marked as such. The game detects when a Pokemon.py save file has been 'tampered' with and marks this on affected Pokémon. And more!
 -  Teams made and saved by Pokémon Showdown! are mostly supported and loadable. (Pokémon with spaces in their names (Mr. Mime, Type: Null) will break this I think. Otherwise this was one of my masterstroke moves, ngl.)
 -  Make a team and then set it to be the rival trainer's team.
 -  Set the starting weather and terrain of the rival trainer battle.
 -  Special main menu banner after you beat the E4 + Champion.
 -  E4 + Champion teams are pre-saved and can be loaded into the game as your own.
 -  Multi-party support through "Boxes" on the main menu.
 -  Perfect all IVs of individual Pokémon or your whole party at once. Fully EV train individual Pokémon or your whole party at once (EVs are distributed randomly, but in multiples of 4 so none are wasted.)

### HOW TO PLAY:
1. Clone (download) this Github repository (https://www.github.com/4ntoined/pokemonpy) to your computer. (Congrats! You've installed the game!)
2. Navigate to the 'pokemonpy' folder from your terminal (command: 'cd /your/path/to/the/folder/here/pokemonpy/')
3. Enter 'python3 pokemon.py'

#### Prerequisites:
1. Access to the command line
   - Search your computer for 'terminal' or 'command prompt' or 'command line'
   - Windows, in my experience, is a little weird about the command line. Mac and Linux are pretty straightforward I think. To play on Windows, I search 'bash' on the start menu and run 'bash.exe' when it pops up. Alternatively, typing and entering 'bash' from the raw command line also works. Bash is a Unix shell. There are others like sh, csh, zsh, and your computer might have one of these installed instead of bash. For our purposes I think they all work just about the same. Your mileage may vary, I'm literally just having fun with it.

2. Python 3.7(ish) or later
   - https://www.python.org

3. Numpy package for Python
   - https://numpy.org/doc/stable/index.html

Tip: Numpy recommends the Anaconda distribution of Python (https://www.anaconda.com/data-science-platform) for users who do not already have Python. If you go this route you get Python and Numpy all at once (no need to install Python, Anaconda will take care of it), along with a lot of other packages you won't need for Pokemon.py. Anaconda's cool, she makes managing Python and its packages pretty easy, but she takes up a lot of storage space and you ONLY need Python + Numpy to play Pokemon.py. So do you.

