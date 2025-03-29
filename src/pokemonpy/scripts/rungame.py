import sys, argparse
import pokemonpy.pokemon as pk

if __name__ == "__main__":
    g4 = pk.game()
    n_args = len(sys.argv)-1
    if n_args: #there are arguments
        parser = argparse.ArgumentParser(description='Play Pokémon!')
        parser.add_argument('-c','--config',action='store',type=str,\
                required=False, dest='configfile', \
                help='provide the path to a pokemon.py config file')
        parser.add_argument('-o','--opponentname',action='store',type=str,\
                required=False, dest='opponame', \
                help='set the name of the rival trainer')
        parser.add_argument('-w','--width',action='store',type=int,\
                required=False, dest='gamewidth', \
                help='set the width of banners and headings, defaults to 64')
        parser.add_argument( '-n','--name',action='store',type=str,\
                required=False,help='write your name',dest='name'\
                )
        parser.add_argument('-s','--psize',action='store',type=int,
                required=False,help='number of starter Pokémon'\
                )
        parser.add_argument('-p','--nparty',action='store',type=int,
                required=False,help='number of starter parties'\
                )
        parser.add_argument('-m','--mute',action='count',default=0,
                required=False,help='skip the pre-game text'\
                )
        argos = parser.parse_args( sys.argv[1:] )
        if argos.mute == 0:
            argos.mute=None
        if argos.configfile is None:
            argos.configfile = 'configurations/config.txt'
        g4.startgame(configname=argos.configfile, mutegame=argos.mute,\
                     username=argos.name, opponentname=argos.opponame,\
                     nparty=argos.nparty,nstart=argos.psize, gw=argos.gamewidth)
    else:
        g4.startgame()
    pass
else:
    pass
