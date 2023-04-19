#Antoine
#Pokemon x Python
#normal 0,fire 1,water 2,grass 3,electric 4,ice 5,fighting 6,poison 7,
#ground 8,flying 9,psychic 10,bug 11, #rock 12,ghost 13,dragon 14,
#dark 15,steel 16,fairy 17
# *****************************   to do list   *****************************: 
# ABILITIES *cough* // genders ugh
# priority // fly/dig/dive/etc // baton pass // bide // trapping moves bind/whirlpool 
# multistrike moves // encore // endeavor // echoed voice/rollout // protect-feint
# entry hazards in battle status, grounded/ungrounded in battle status
# ***************************************************************************
import copy
#import time as t
import numpy as np
from base_pokemon import mon, battle, field, checkBlackout, loadMon, makeMon,\
    makeRandom, makeParty, moveInfo, typeStrings, Weathers, Terrains, \
    shortpause, dramaticpause, micropause, elite4_healquit, print_dex, \
    print_party
from moves import getMoveInfo,mov #,natures
from dexpoke import dex
from victoryroad import make_teams, random_evs
rng=np.random.default_rng()
#
############   give the player a starter  ###############
starterlevel = 150
starter= makeRandom(level=starterlevel)
starter.set_evs(tuple(random_evs()))
players_parties = []
##### creating the trainer for classic mode #####
rival= makeRandom(np.floor(starter.level*(0.96)), 6)
rival2= makeRandom(np.floor(starter.level*1.07), 6)
#stuff them into their parties
starterParty = [starter]
trainerParty=[rival,rival2]
#
opponentName="RIVAL"
#### setting up the player's parties ####
#this list will hold tuples of pokemon parties (lists of pokemon objs) and names and indeces
players_parties.append((starterParty, "starter", 0))
userParty=starterParty
equiped = 0
party_count = 1 #keeping track of parties as they are created for indexing purposes
hallfame_count = 0
#####################
#load up a battlefield for classic mode
scarlet = field(rando=True)
######################
print("\n... Created by Adarius ...")
shortpause()
print("** Welcome to the Wonderful World of Pokémon Simulation! **")
dramaticpause()
#aa:mainmenu
while 1:
    #going to consolidate nursery and dex selection
    #move tutor and move deleter and training
    #opponent set and battle setting set 
    #reseting the party can get swallowed into expanded multi-party functions
    mainmenu = "\n[P]okémon\n[B]attle!\nElite [4]\n[T]raining\n[N]ursery" + \
        "\nPokémon [C]enter\nBo[x]es\nBattle [S]etting"+ \
        "\n[L]oad\nWhat to do: "
    userChoice=input(mainmenu)
    ########################################################################################################
    #user setting the weather and terrain for classic mode #aa:classicsettings
    if userChoice=="s" or userChoice=="S":
        #hello
        while 1: #user input loop
            print("\n------------Classic Mode Settings------------")
            micropause()
            print("")
            micropause()
            #settings menu
            print("[1] Set the conditions of battle\n[2] Set your opponent's party")
            sat_choice = input("What [#] to do or [b]ack: ")
            if sat_choice == 'b' or sat_choice == 'B':
                break
            if sat_choice == '1': #battlefield conditions setting
                print("\n------------ Set the Stage ------------\n-------------------------------------------------")
                print("\nCurrent Battle conditions:")
                micropause()
                print(f"Weather: {scarlet.weather}\nTerrain: {scarlet.terrain}")
                print("\n[1] Randomize weather and terrain\n[2] Randomize just weather\n[3] Randomize just terrain\n[4] Set manually")
                setChoice=input("What [#] to do or [b]ack: ")
                #go back
                if setChoice=="b" or setChoice=="B":
                    break
                #randomize both
                if setChoice=="1":
                    scarlet.shuffleweather()
                    print("Conditions have been randomized!")
                    shortpause()
                #randomize weather
                if setChoice=="2":
                    scarlet.shuffleweather(True,False)
                    print("Weather has been randomized!")
                    shortpause()
                #randomize terrain
                if setChoice=="3":
                    scarlet.shuffleweather(False,True)
                    print("Terrain has been randomized!")
                    shortpause()
                #manual set
                if setChoice=="4":
                    while 1: #user input loop, weather or terrain
                        conChoice=input("Set\n[1] Weather \n[2] Terrain\nor [b]ack: ")
                        if conChoice=="b" or conChoice=="B":
                            break
                        #weather
                        if conChoice=="1":
                            while 1: #user input loop, whats the new terrain
                                print("")
                                for i in range(len(Weathers)):
                                    print(f"{i}\t{Weathers[i]}")
                                newWeath=input("What should the new weather be?\n[#] or [b]ack: ")
                                if newWeath=="b" or newWeath=="B":
                                    break
                                try:
                                    scarlet.weather=Weathers[int(newWeath)]
                                    print("New weather set!")
                                    break
                                except IndexError:
                                    print("*\n** Entry out of range **\n*")
                                except ValueError:
                                    print("*\n** Not a valid entry **\n*")
                        #weather
                        elif conChoice=="2":
                            while 1: #user input loop, whats the new terrain
                                print("")
                                for i in range(len(Terrains)):
                                    print(f"{i}\t{Terrains[i]}")
                                newTerr=input("What should the new terrain be?\n[#] or [b]ack: ")
                                if newTerr=="b" or newTerr=="B":
                                    break
                                try:
                                    scarlet.terrain=Terrains[int(newTerr)]
                                    print("New terrain set!")
                                    break
                                except IndexError:
                                    print("*\n** Entry out of range **\n*")
                                except ValueError:
                                    print("*\n** Not a valid entry **\n*")
                #more options to change battle conditions
            elif sat_choice == '2': ## another setting somewhere
                print("\n________ Opponent Reset ________")
                shortpause()
                aceChoice=input("Set your current team as the battle opponent?\n[y] or [b]ack: ")
                if aceChoice=='y' or aceChoice=="Y":
                    trainerParty=copy.deepcopy(userParty)
                    print("The Battle Opponent has a new Party! Good Luck!")
                    shortpause() #kills
                else:
                    print("Leaving Opponent Reset...")
                    shortpause() #kills
                #end of opponent set, back to main screen
            else:
                #print("*like I'm hearing a ghost*: What was that?")
                pass
            # should be the end of the classic setting block
        #zz:classicsettings
    ####  E4  #### aa:elite4mode
    if userChoice=='4':
        ## can't play if all your pokemon are fainted
        ni, ny = checkBlackout(userParty)
        if ni==0:
            print("\nYou can't battle without a healthy Pokémon!")
            shortpause()
            continue #go back to main without starting the battle
        ## going to recommend a party level 
        print("\nYou can challenge the best trainers in the world.")
        shortpause()
        bigstuff = make_teams()
        print(f"Recommended level: {bigstuff[4][1][5].level}")
        shortpause()
        aretheysure = input("Will you challenge the Elite 4?\n[y]es or [b]: ")
        if aretheysure=='b' or aretheysure == 'B':
            print("Leaving Indigo Plateau...")
            micropause()
            continue
        if aretheysure=='y' or aretheysure=='Y':
            #e4 order will be S - Z - C - N largely because I said so
            sils_stuff = bigstuff[0]
            zins_stuff = bigstuff[1]
            cyns_stuff = bigstuff[2]
            nnns_stuff = bigstuff[3]
            chps_stuff = bigstuff[4]
            #
            gold = field(weath='rain') #S
            gold.shuffleweather(False, True)
            sapphire = field(weath='sandstorm',terra='electric') #Z
            diamond = field(weath='hail',terra='psychic') #C
            black = field(weath='sunny',terra='misty') #N
            indigo = field(terra='grassy') #champ
            #
            silP= sils_stuff[1] 
            zinP= zins_stuff[1]
            cynP= cyns_stuff[1] 
            nnnP= nnns_stuff[1]
            chaP= chps_stuff[1]
            #
            battle1 = battle(userParty, silP, gold, cpu_name = sils_stuff[0])
            resu1 = battle1.startbattle(e4=True)
            resu1=True
            if (not resu1): #the user lost
                print("Leaving Indigo Plateau...")
                micropause()
                continue
            print(f"\n{zins_stuff[0]} awaits your challenge...")
            shortpause()
            hea_1 = elite4_healquit(userParty)
            if hea_1 =='quitted': continue
            #zinnia's battle
            battle2 = battle(userParty,zinP,sapphire,cpu_name = zins_stuff[0])
            resu2 = battle2.startbattle(e4=True)
            resu2=True
            #win check
            if (not resu2): #the user lost
                print("Leaving Indigo Plateau...")
                micropause()
                continue
            print(f"\n{cyns_stuff[0]} awaits your challenge...")
            shortpause()
            hea_2 = elite4_healquit(userParty)
            if hea_2 =='quitted': continue
            #cynthias battle
            battle3 = battle(userParty,cynP,diamond,cpu_name = cyns_stuff[0])
            resu3 = battle3.startbattle(e4=True)
            resu3 = True
            if (not resu3): #the user lost
                print("Leaving Indigo Plateau...")
                micropause()
                continue
            print(f"\n{nnns_stuff[0]} awaits your challenge...")
            shortpause()
            hea_3 = elite4_healquit(userParty)
            if hea_3 =='quitted': continue
            #N's battle
            battle4 = battle(userParty, nnnP, black,cpu_name = nnns_stuff[0])
            resu4 = battle4.startbattle(e4=True)
            resu4=True
            #win
            if (not resu4): #the user lost
                print("Leaving Indigo Plateau...")
                micropause()
                continue
            print("\nThe Grand Champion awaits your challenge...")
            shortpause()
            hea_4 = elite4_healquit(userParty)
            if hea_4 =='quitted': continue
            #champ
            battle5 = battle(userParty, chaP, indigo,cpu_name = chps_stuff[0])
            resu5 = battle5.startbattle(e4=True)
            resu5=True
            #if you won, you won, like it's over
            if not resu5:
                print("Leaving Indigo Plateau...")
                micropause()
                continue
            else:         
                hallfame_count += 1
                print("\nYou defeated the Elite Four and the Grand Champion!")
                dramaticpause()
                print("Congratulations! Cheers to the new Grand Champion! A true Pokémon Master!")
                dramaticpause()
                hallfame = input("Would you like to save your Hall of Fame record?\n[y]es or no: ")
                if hallfame == "y" or hallfame == "Y":
                    #save the party
                    savehere = f'halloffame_{hallfame_count:0>2}.sav'
                    for i in userParty: i.save(savehere)
                    print(f"Party saved at {savehere}.")
                    micropause()
                pass
            pass
        else:
            #print("Leaving Indigo Plateau...")
            #micropause()
            continue
    ### end of e4? mode ### zz:elite4mode
    #### Classic Battle #### aa:battlemode
    if userChoice=="b" or userChoice=="B":
        ni, ny = checkBlackout(userParty)
        if ni==0:
            print("\nYou can't battle without a healthy Pokémon!")
            shortpause()
            continue #go back to main without starting the battle
        classicbattle = battle(userParty, trainerParty, scarlet)
        classicbattle.startbattle()
        #then it should loop back to the main menu?
    ###end of battle block### zz:battlemode
    #### check party pokemon? aa:party ####
    if userChoice=="p" or userChoice=="P":
        while 1:
            """
            print("\n////////////////////////////////\n//////// Party Pokémon /////////\n////////////////////////////////")
            for i in range(len(userParty)):
                if userParty[i].dualType:
                    thipe=typeStrings[userParty[i].tipe[0]]
                    thipe+=" // "
                    thipe+=typeStrings[userParty[i].tipe[1]]
                else:
                    thipe=typeStrings[userParty[i].tipe[0]]
                print(f"[{i+1}] {userParty[i].name} \tLv. {userParty[i].level} \tHP: {format(userParty[i].currenthpp,'.2f')}% \t{thipe}")"""
            print_party(userParty)
            partyChoice=input("Enter a number to see a Pokémon's summary...\n[#] or [b]ack: ")
            #go back to main screen
            if partyChoice=='b' or partyChoice=="B":
                print("Leaving Party screen...")
                shortpause() #kills
                break
            try:
                pokeInd=int(partyChoice)-1
                selMon=userParty[pokeInd]
            except ValueError:
                print("\n! Enter the number corresponding to a Pokémon !\nor [b] to go back")
            except IndexError:
                print("\n! Enter the number corresponding to a Pokémon !\nor [b] to go back")
            else:
                while 1:
                    selMon.summary()
                    sumChoice=input(f"What to do with {selMon.name}?\nset [f]irst, see [m]oves, [s]ave, [j]udge or [b]ack: ")
                    #go back to pokemon selection
                    if sumChoice=='b' or sumChoice=="B":
                        shortpause()
                        break
                    #save
                    if sumChoice=='s':
                        while 1:
                            savename=input("Enter name of savefile...\n[blank] to use default savefile name\nor [b]ack\n: ")
                            if (savename=='b') or (savename=='B'):
                                shortpause()
                                break
                            if savename=='':
                                selMon.save()
                                print(f"{selMon.name} was saved to the file!\n")
                                shortpause() #kills
                                continue
                            else:
                                selMon.save(savename)
                                print(f"{selMon.name} was saved to the file!\n")
                                shortpause() #kills
                                continue
                        #
                    #set first
                    if sumChoice=='f':
                        if pokeInd==0:
                            print(f"{selMon.name} is already first!")
                            continue
                        moving=userParty.pop(pokeInd)
                        userParty.insert(0,moving)
                        print(f"{moving.name} was moved to the front!")
                        shortpause() #kills
                        continue
                    #
                    if sumChoice=="m" or sumChoice=="M":
                        while 1: #user input loop
                            selMon.showMoves()
                            movChoice=input("Which move to look at?\n[#] or [b]ack: ")
                            if movChoice=="b" or movChoice=="B":
                                #leave move info selection, back to what to do w pokemon
                                break
                            #try to get numbers from user input
                            try:
                                movez=movChoice.split() #pokemon movelist index (string)
                                movez=[int(i)-1 for i in movez] #pokemon movelist indices (int)
                                movez=[selMon.knownMoves[i] for i in movez] #pokemon move movedex index
                            except ValueError:
                                print("\n** Entry must be a [#] or list of [#]s, separated by spaces! **")
                            except IndexError:
                                print("\n** Use the indices to select moves to take a closer look at. **")
                            else:
                                for i in range(len(movez)):
                                    print("")
                                    moveInfo(movez[i])
                                    micropause() #drama
                                #we got all the move info out?, go back to pokemon?
                                pause=input("\nEnter anything to continue back to Pokémon summary...")
                                break
                    #judge
                    if sumChoice=="j" or sumChoice=="J":
                        selMon.appraise()
                        pause=input("Enter anything to continue...")
            #end of while block
        print("Going back to main screen...")
        shortpause()
        #end of party pokemon
    ###end of party display block###zz:pokemonparty
    ####pokemon aa:nursery####
    if userChoice=='n' or userChoice=='N':
        print("\n____ Welcome to the Pokémon Nursery! ____")
        shortpause()
        print("Here, you can create Pokémon from scratch!")
        shortpause()
        ####nursery loop####
        while 1:
            nurseChoice=input("What do you want to do?\n[1] Create a Pokémon!!\n[2] Choose from the Pokedex\n[#] or [b]ack: ")
            if nurseChoice=='b' or nurseChoice=='B':
                break #exits nursery loop
            ####new pokemon####
            if nurseChoice=='1':
                newName=input("Would you like to give your Pokémon a name?: ")
                print(f"Let's get {newName} some STATS")
                while 1: #stat input loop
                    statS=input("Enter 6 stats [1-255]\n[HP] [ATK] [DEF] [SPA] [SPD] [SPE]\n")
                    try:
                        stat=[int(float(i)) for i in statS.split()]
                        if len(stat)!=6:
                            print("\n!! Enter all 6 stats at once !!")
                            continue
                        if min(stat)>0:
                            break #stats acccepted, exits stat input loop
                        else:
                            print("\n**Base stats must be at least 1**")
                    except ValueError:
                        print("\n** Stats must be numbers **")
                ##type choice##
                print("****************\nPokémon Types:\n0 Normal\n1 Fire\n2 Water\n3 Grass\n4 Electric"+ \
                      "\n5 Ice\n6 Fighting\n7 Poison\n8 Ground\n9 Flying\n10 Psychic\n11 Bug\n12 Rock"+ \
                          "\n13 Ghost\n14 Dragon\n15 Dark\n16 Steel\n17 Fairy\n****************")
                while 1: #type input loop
                    newTipe=input(f"Use the legend above to give {newName} a type or two: ")
                    try:
                        newTipe=[int(i) for i in newTipe.split()]
                        if max(newTipe)<=18: #no types above 17
                            if min(newTipe)>=0: #no types below 0
                                break #input valid, exit type input loop
                            else:
                                print("\n** Highest type: 17, lowest type: 0 **")
                        else:
                            print("\n** Highest type: 17, lowest type: 0 **")
                    except ValueError:
                        print("\n** Use the legend above and enter a number (or 2 separated with a space) **")
                ##level input##
                while 1: #level input loop
                    lvlS=input(f"What level should {newName} be? (min. 1): ")
                    try:
                        lvlS=int(lvlS)
                        if lvlS>=1:
                            break #break level input
                        else:
                            print("\n** Level must be at least 1 **")
                    except ValueError:
                        print("\n** Enter a number! **")
                ##oh boy nature input###
                while 1:
                    print("\n~~~~~~~~~~\nAttack : 0\nDefense: 1\nSp. Atk: 2\nSp. Def: 3\nSpeed  : 4\n~~~~~~~~~~")
                    nachup = input(f"What should be {newName}'s boosted stat: ")
                    try:
                        nachup = int(nachup)
                        if (nachup <= 4) and (nachup >= 0):
                            break #stat good
                        else:
                            print("\n!! Enter a number between 0 and 4 !!")
                            micropause()
                    except ValueError:
                        print("\n!! Enter a number !!")
                        micropause()
                    ##okay if all goes well the code should progress here and we need to ask for hindered nature
                while 1:
                    #print("\n~~~~~~~~~~\nAttack : 0\nDefense: 1\nSp. Atk: 2\nSp. Def: 3\nSpeed  : 4\n~~~~~~~~~~")
                    nachdo = input(f"What should be {newName}'s nerfed stat: ")
                    try:
                        nachdo = int(nachdo)
                        if (nachdo <= 4) and (nachdo >= 0):
                            break #stat is good, break input loop
                        else:
                            print("\n!! Enter a number between 0 and 4 !!")
                            micropause()
                    except ValueError:
                        print("\n!! Enter a number !!")
                        micropause()
                nacher = (nachup, nachdo)
                ##make the pokemon!##
                if len(newTipe)==1:
                    newMon=mon(lvlS,newName,nature=nacher,hpbase=stat[0],atbase=stat[1],debase=stat[2],sabase=stat[3],sdbase=stat[4],spbase=stat[5],tipe=np.array(newTipe))
                if len(newTipe)>1:
                    newMon=mon(lvlS,newName,nature=nacher,hpbase=stat[0],atbase=stat[1],debase=stat[2],sabase=stat[3],sdbase=stat[4],spbase=stat[5],tipe=np.array([newTipe[0],newTipe[1]]))
                print(f"\n{newName} is born!")
                shortpause()
                userParty.append(newMon)
                print("Take good care of them!")
                #zz:customMons
            ##pokedex selection aa:pokedex
            elif nurseChoice == '2':
                #do the dex selection
                printdex= input("Would you like to see the Pokedex?\n[y]es, [n]o, or [b]ack: ")
                if printdex=='b' or printdex=='B':
                    continue
                elif printdex=='y' or printdex=='Y':
                    print("\n*****************************\n******** The Pokedex ********\n*****************************\n")
                    print_dex()
                    shortpause()
                while 1:
                    pokeChoice=input("Which Pokémon would you like to add to your team?\n[#]'s or [b]ack: ")
                    if pokeChoice=='b' or pokeChoice=='B':
                        print("Leaving Pokedex...")
                        shortpause() #kills
                        break
                    try:
                        pokeChoices=pokeChoice.split()
                        pokInts=[int(i) for i in pokeChoices]
                        if max(pokInts)<len(dex):
                            if min(pokInts)>=0:
                                print("")
                                for i in pokInts:
                                    newbie=makeMon(i,userParty[0].level)
                                    print(f"{newbie.name} is born and added to your party!")
                                    userParty.append(newbie)
                                    micropause()
                                    #print(f"{newbie.name} has been added to your party!")
                                    #shortpause()
                                shortpause()
                                break #when done adding mons, get out of here
                            else: #failing brings you back to new pokemon loop
                                print("\n** That's out of bounds... **")
                        else: #new pokemon loop
                            print("\n** That's out of bounds... **")
                    except ValueError:
                        print("\n** Try again **")
                    except IndexError:
                        print("\n** That's out of bounds... **")
                pass
            else: #other choices in the nursery main
                pass
            pass #loops back to start of nursery
        pass #loops back to start of game
    ###end of nursery block #zz:nursery
    ####training####
    ## gonna rework this to include move tutor and move deleter
    ## at the same time, gonna also rework the concept so that you choose a pokemon
    ## and then choose from there wha tto do with them
    if userChoice=='t' or userChoice=='T':
        while 1:
            print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&\n&&&&&&&&&&&  Training  &&&&&&&&&&&\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
            #choose a pokemon
            print("")
            for i in range(len(userParty)):
                print(f"[{i+1}] {userParty[i].name} \tLv. {userParty[i].level}")
            trainChoice=input("Which Pokémon will we train?:\n[#] or [b]ack: ")
            #option to go back, from pokemon selection to main screen
            if trainChoice=='b' or trainChoice=='B':
                break
            try:
                pokeIndex=int(trainChoice)-1
                pokeTrain=userParty[pokeIndex]
                #break #confirmed numbers are good, exit user loop                
            except ValueError:
                #we need a number
                print("\n** Enter a NUMBER **")
                micropause()
                pass
            except IndexError:
                print("\n** Must enter the number of a Pokémon **")
                micropause()
                #the pokemon does not exist
                pass
            else:
                while 1:
                    print(f"\n******** Training {pokeTrain.name} ********")
                    hypermoves = input("[1] Super-Hyper Training\n[2] Move Tutor\n[3] Move Deleter\n[#] or [b]ack\n: ")
                    if hypermoves == 'b' or hypermoves=='B': #superhyper
                        break
                    #### super-hyper training #### aa:training
                    if hypermoves == '1': 
                        while 1: #i want to loop back here unless specifically broken
                            superHyper=input("Manage [E]Vs or [I]Vs or [L]evels\nor [b]ack: ") #anything other than options below will skip to the next loop of choose a pokemon
                            if superHyper=='b' or superHyper=='B':
                                print("\nLeaving SuperHyper Training...")
                                micropause()
                                break
                            #EVs
                            if superHyper=='e':
                                while 1:
                                    evs=input("Enter 6 numbers (0-252) all at once.\nEVs cannot sum >508.:\n")
                                    #option to go back
                                    if evs=='b':
                                        break #throws us back to ev/iv/lvls
                                    else:
                                        evs=evs.split()
                                        try:
                                            eves=np.array([int(evs[0]),int(evs[1]),int(evs[2]),int(evs[3]),int(evs[4]),int(evs[5])])
                                            #make sure values are legal
                                            if np.max(eves)<=252. and np.min(eves)>=0:
                                                if np.sum(eves)<=508.:
                                                    pokeTrain.hpev=int(evs[0])
                                                    pokeTrain.atev=int(evs[1])
                                                    pokeTrain.deev=int(evs[2])
                                                    pokeTrain.saev=int(evs[3])
                                                    pokeTrain.sdev=int(evs[4])
                                                    pokeTrain.spev=int(evs[5])
                                                    pokeTrain.reStat()
                                                    print("\nTraining...")
                                                    shortpause()
                                                    print(f"\n{pokeTrain.name} is all Supertrained!!")
                                                    shortpause()
                                                    break #ends ev training, back to evs
                                                else:
                                                    print("\n** No more than 508 EVs total. **")
                                                    pass
                                                pass
                                            else:
                                                print("\n** No more than 252 EVs in any stat. **\n** No negative EVs. **")
                                                pass
                                            pass
                                        except: #catch non-numbers, incomplete sets
                                            print("\n** Max EV is 252. **\n** Total EVs cannot sum >508. **\n** Input 6 numbers separated by spaces. **")    
                                        #if code is here, EV training while loop continues
                                    pass
                                #end of ev training loop
                            #IVs        
                            elif superHyper=='i':
                                while 1:
                                    ivs=input("Enter 6 numbers (0-31) all at once.:\n")
                                    #option to go back, from iv input to ev/iv/lvl
                                    if ivs=='b':
                                        break
                                    else:
                                        ivs=ivs.split() #6 numbers into list of strings
                                        try:
                                            #make sure we have 6 numbers
                                            ives=np.array([int(ivs[0]),int(ivs[1]),int(ivs[2]),int(ivs[3]),int(ivs[4]),int(ivs[5])])
                                            if np.max(ives)<=31 and np.min(ives)>=0:
                                                pokeTrain.hpiv=int(ivs[0])
                                                pokeTrain.ativ=int(ivs[1])
                                                pokeTrain.deiv=int(ivs[2])
                                                pokeTrain.saiv=int(ivs[3])
                                                pokeTrain.sdiv=int(ivs[4])
                                                pokeTrain.spiv=int(ivs[5])
                                                pokeTrain.reStat()
                                                print("\nTraining...")
                                                shortpause()
                                                print(f"{pokeTrain.name} is all Hypertrained!")
                                                shortpause()
                                                break #ends IV training, goes back to choose a pokemon
                                            else:
                                                print("\n** Maximum IV is 31 **\n** Minimum is 0 **")
                                        except IndexError: #input couldn't fill 6-item array
                                            print("\n** Enter !6! numbers separated by spaces **")
                                        except ValueError: #we tried to make an int() out of something non-number
                                            print("\n** Enter 6 !numbers! separated by spaces **")
                                        #if we get here, an IV was more than 31, loops back to IV input
                                    #end of iv input loop
                                #end of IV training loop
                            #level
                            elif superHyper=='l':
                                while 1:
                                    levl=input(f"What level should {pokeTrain.name} be?\nor [b]ack: ")
                                    if levl=='b' or levl=='B':
                                        break
                                    try:
                                        levl = int(levl)
                                        if levl>=1: #if input was a positive number
                                            pokeTrain.level=levl #set pokemon's new level
                                            pokeTrain.reStat() #recalcs stats
                                            print("\nTraining...")
                                            shortpause()
                                            print(f"{pokeTrain.name} leveled up (or down)!")
                                            shortpause()
                                            break #back to levl/evs/ivs
                                        else:
                                            print("\n**Level must be at least 1**")
                                    except:
                                        print("\n**Enter a number greater than 0.**")
                                    #end of level input while block
                                #end of level training block
                    #### move tutor #### aa:movetutor
                    elif hypermoves == '2':
                        while 1:
                            print("\n****************************\n******** Move Tutor ********\n****************************\n\nYou can teach your Pokémon new moves!\n")
                            #print all the moves
                            print("\n------------ Pokémon Moves ------------")
                            for i in range(len(mov)):
                                print(f"{mov[i]['index']}\t| {mov[i]['name']}\t| " + \
                                      f"{typeStrings[mov[i]['type']]}")
                            print("---------------------------------------")
                            micropause()
                            #ask user what moves to learn
                            learnChoice=input(f"What moves should {pokeTrain.name} learn?\n" + \
                                "(Lead with 'i' to see move info.)\n(Use 'random n' to teach n random moves.)"+\
                                "\n[#]'s or [b]ack: ")
                            #go back
                            if learnChoice=='b' or learnChoice=='B':
                                print("Leaving Move Tutor...")
                                shortpause()
                                break #back to training-main
                            moveslearning = learnChoice.split()
                            mlcount = len(moveslearning)
                            # for non-blank entries
                            if mlcount > 0:
                                #user wants to learn about the moves
                                if moveslearning[0]=='i' or moveslearning[0]=='I':
                                #while 1:
                                    #mpChoice=input("Which moves do you want to see?\n[#] or [b]ack: ")
                                    #if mpChoice=="b" or mpChoice=="B":
                                    #    shortpause()
                                    #    break
                                    try:
                                        movez=moveslearning[1:] #pokemon movelist index (string)
                                        movez=[int(i) for i in movez] #pokemon movelist indices (int)
                                    except ValueError:
                                        print("\n** Entry must be a [#] or list of [#]s, separated by spaces! **")
                                    except IndexError:
                                        print("\n** Use the indices to select moves to take a closer look at. **")
                                    else:
                                        for i in range(len(movez)):
                                            print("")
                                            moveInfo(movez[i])
                                            micropause() #drama
                                        pause=input("\nEnter anything to continue... ")
                                        #no break, loop back to moves tutor, NOT training
                                #user wants random moves
                                elif moveslearning[0]=='random':
                                    try:
                                        n_moves = int(moveslearning[1])
                                    except ValueError:
                                        print('\n** Bad Value **')
                                    except IndexError: #what happens if user wants more 
                                        print('\n** Bad Index **')
                                    else:
                                        pokeTrain.randomizeMoveset(n_moves)
                                        break #randomized moves, go back to training menu
                                else:
                                    try:
                                        #chooseMoves=chooseMove.split() #separate move indices into own strings
                                        moveInts=[int(i) for i in moveslearning] #(try to) convert strings to ints
                                        incomplete=False
                                        if max(moveInts)<len(mov): #make sure all indices have an entry in the movedex
                                            if min(moveInts)>=0: #ward off negative numbers
                                                print("")
                                                for i in moveInts:
                                                    if i in pokeTrain.knownMoves:
                                                        print(f"! {pokeTrain.name} already knows {getMoveInfo(i)['name']} !")
                                                        #incomplete=True
                                                    else:
                                                        pokeTrain.knownMoves.append(i)
                                                        pokeTrain.PP.append(getMoveInfo(i)['pp'])
                                                        print(f"{pokeTrain.name} learned {getMoveInfo(i)['name']}!")
                                                        micropause()
                                                break #moves addressed, get out of here
                                                #if incomplete==False: #if there are no conflicts
                                                    #break #all moves added, breaks loop and goes back to choose a pokemon
                                                #otherwise, choose moves loop is restated
                                            else: #failing brings you back to move selection
                                                print("** That's out of bounds.. **\n")
                                        else: #failing brings you back to move selection
                                            print("** That's out of bounds.. **\n")
                                    except ValueError:
                                        print("** Enter [#] corresponding to desired moves **\n")
                                    except IndexError:
                                        print("** Use move legend to add moves **\n")
                                        #end of move selection while block, moves have been picked
                            #choose a new pokemon
                        #goes back to choose a pokemon
                    ###end of move learner block####
                    #### move deletion #### aa:movedelete
                    elif hypermoves == '3': #move deletions
                        while 1: #user input loop
                            print("\n******** Move Deleter ********")
                            shortpause()
                            pokeTrain.summary()
                            mvChoice=input("Which moves should be deleted?\n[#] or [b]ack: ")
                            mvC1 = len(mvChoice.split())
                            print(mvC1)
                            #go back
                            if mvChoice=="b" or mvChoice=="B":
                                break
                            #display move info if you lead with I
                            if mvC1 >= 1:
                                print(mvChoice.split()[0])
                                if mvChoice.split()[0]=='i' or mvChoice.split()[0]=='I':
                                    try:
                                        movez=mvChoice.split()[1:] #pokemon movelist index (string)
                                        movez=[int(i)-1 for i in movez] #pokemon movelist indices (int)
                                        movea=[ pokeTrain.knownMoves[i] for i in movez]
                                    except ValueError:
                                        print("\n** Entry must be a [#] or list of [#]s, separated by spaces! **")
                                    except IndexError:
                                        print("\n** Use the indices to select moves to take a closer look at. **")
                                    else:
                                        for i in range(len(movez)):
                                            print("")
                                            moveInfo(movea[i])
                                            micropause() #drama
                                        pause=input("\nEnter anything to continue... ")
                                        continue #after seeing move info loop back to deleter menu
                                #else, move on
                            #else, move on
                            #if not back or looking for info we assume we got a list of numbers
                            try:
                                chooz=np.array([int(i)-1 for i in mvChoice.split()])
                                print("")
                                for i in range(len(chooz)):
                                    if len(pokeTrain.knownMoves)==1: #catch players trying to dump whole moveset
                                        micropause()
                                        print("** Pokémon cannot forget its last move **")
                                        break
                                    if i==0: #keeps us from checking empty arrays i.e. choices[0:0]
                                        byeMove=pokeTrain.knownMoves.pop(chooz[i])
                                        byePP = pokeTrain.PP.pop(chooz[i])
                                        print(f"{pokeTrain.name} forgets {mov[byeMove]['name']}...")
                                        micropause()
                                    else:
                                        removedIndices=np.count_nonzero(chooz[0:i]<chooz[i]) #how many selected indices that are *lower* than current one have already been removed
                                        chooz[i]-=removedIndices
                                        byeMove=pokeTrain.knownMoves.pop(chooz[i])
                                        byePP = pokeTrain.PP.pop(chooz[i])
                                        print(f"{pokeTrain.name} forgets {mov[byeMove]['name']}...")
                                        micropause()
                                print("Selected moves have been forgetten!")
                                #shortpause() #kills
                                break #back to training menu
                            except ValueError:
                                print("\n** Entry must be [#] or list of [#]s separated by spaces! **")
                            except IndexError:
                                print("\n** Entry must correspond to a Pokémon move! **")
                        ###zz:movedelete
                    elif hypermoves == '4': #renaming pokemon
                        pass
                    elif hypermoves == '5': #re-naturing pokemon
                        pass
                    else:
                        pass
        #
    ###end of training block###
    #zz:training    
    ####Loading pokemon
    if userChoice=='l':
        print("******** Load Pokémon ********\n\nYou can load previously saved Pokémon!\n")
        while 1: #savefile input loop
            saveChoice=input("What save file to load?\n[blank] entry to use default or [b]ack\n: ")
            #go back
            if saveChoice=='b' or saveChoice=='b':
                print("Leaving Load Pokémon..")
                shortpause()
                break
            if saveChoice=="":
                newMons=loadMon("pypokemon.sav")
                if newMons[0]==0: #if error in loading data, ask for savefile again
                    print("\n!! Something is wrong with this savefile !!")
                    continue
                #add all the pokemon to the party
                for i in newMons:
                    userParty.append(i)
                    print(f"{i.name} has joined your party!")
                    shortpause()
                print("Finished loading Pokémon!\n")
                shortpause()
            else:
                try:
                    newMons=loadMon(saveChoice)
                except IndexError:
                    print("! That filename wasn't found !**\nno reason why this should run")
                else:
                    if newMons[0]==0: #error in loading data
                        continue
                    for i in newMons:
                        userParty.append(i)
                        print(f"{i.name} has joined your party!")
                        shortpause()
                    print("Finished loading Pokémon!\n")
                    shortpause()
                    #loop back to load a save
                #
            #loop back to load a save
        #done loading save
    ###end of load save block###
    ####pokemon center#### aa:center aa:healing let's heal em up
    if userChoice=="c" or userChoice=="C":
        print("\n******** Welcome to the Pokémon Center ********\n")
        shortpause()
        print("We can heal your Pokémon to full health!")
        shortpause()
        while 1:
            cenChoice=input("[y] to restore your party or [b]ack\n: ")

            if cenChoice=='b':
                print("See you soon!\n")
                shortpause()
                break
            
            if cenChoice=='y':
                print("\n")
                for i in userParty:
                    i.restore()
                    print(f"{i.name} is ready for more battles!")
                    micropause()
                print("\nYour party is looking better than ever!!")
                shortpause()
                print("\nHave a nice day! and have fun!")
                shortpause()
                break #back to main screen    
    ####resetting user Party to Bulbasaur
    ### multi-party support? #aa:multiparty
    if userChoice=='X' or userChoice=='x':
        while 1: #input loop only to catch players leaving individual pokemon removal
            #see party will select a party, from there #we can copy the party, equip it, add a pokemon (from the equipped party) to it, more?
            equii = np.squeeze( np.argwhere( np.array(players_parties,dtype=object)[:,2]==equiped ))
            print("\n[[[[[[[[[[[[ Your Parties ]]]]]]]]]]]]\n")
            for i in range(len(players_parties)):
                print(f"[{i+1}] {players_parties[i][1]} | size: {len(players_parties[i][0])}")
            print(f"Equipped: {players_parties[equii][1]}\n")
            #equipd = np.argwhere(players_parties[:,1]=="")
            partiesChoice = input("[S]tart a new party\n[#] see party\nor [b]ack: ") 
            if partiesChoice == "b" or partiesChoice == "B":
                break
            if partiesChoice == "s" or partiesChoice=="S":
                #make a new party, a list
                #ask player to name the party, for id purposes
                #ask them if they want to equip it?
                #that's it, no? do we allow empty parties? idw impose a pokemon onto
                #every new party, only for the player to have to get rid of it if they
                #don't want it around. like its creating unnecessary work
                #but i am worried that an empty active party will somewhere break the code
                #and I really dont wanna have to go through the exercise of fixing it in that case
                #maybe we'll add a safeguard that you can't equip an empty party
                partname = input("Name the party: ")
                equi="none"
                #input loop for number of pokemon to include in the party
                while 1:
                    partmons = input("Fill with how many random Pokémon: ")
                    levelz = input("Level: ")
                    try:
                        num = int(float(partmons)) #number of new pokemon
                        lv = int(float(levelz)) #level of the pokemon
                        if num>=0 and lv>=0: #if 0 or more
                            #run the else block
                            pass
                        else:
                            print("\n!! 0 or more !!")
                            micropause()
                            continue #don't run the else block, reloop to input
                    except ValueError:
                        print("\n** Bad Value **")
                        pass
                    else:
                         new_party = makeParty(num,level=lv) #making the party
                         print("\nYou started a new party!")
                         shortpause()
                         break #leave the input loop for num of pokes
                players_parties.append((new_party,partname,party_count))
                party_count += 1
                if len(new_party)>=1: equi = input("Would you like to equip this party?\n[y] or [n]: ")
                if equi=='y' or equi=="Y":
                    userParty = new_party
                    equiped = players_parties[-1][2]
                pass
            elif 1: #some condition? for looking at a party, should just be an integer
                #see the pokemon in the party, give and take options for that party
                #equipping, copying, adding a pokemon
                party_count += 1
                try: #parties choice is maybe a number
                    part_n = int(float(partiesChoice)-1)
                    party_i, party_name, party_dex = players_parties[part_n]
                    # we have the party in question and its name loaded up
                    #index and value are good, we move to print the pokemon and ask options
                    #sigh... need to make pokemon party display a function
                    #be right back
                    #hey                            
                    pass
                except ValueError:
                    pass
                except IndexError:
                    pass
                else:
                    while 1:
                        #show the party
                        equipp = equiped==party_dex #boolean carrying when selected party is equipped
                        sizep = len(party_i)
                        if sizep == 0:
                            print(f"\n--- {party_name} ---")
                            print("====================\nThis party is empty.\n====================")
                        else: print_party(party_i, party_name, True)
                        if equipp: print("~This is your equipped party.~") #this is the equipped party
                        #ask for options, 
                        megaChoice = input("[e]quip, [c]opy, [a]dd/[r]emove Pokémon, [d]elete, e[m]pty, [s]ave, [#], [b]ack\n: ")
                        if megaChoice=='b' or megaChoice=='B': break
                        if megaChoice=='e' or megaChoice=='E': #equipping the party
                            if equipp: #if this party is already equipped
                                print(f"\n!! {party_name} is already equipped !!")
                                micropause()
                                continue #back to party options
                            if sizep < 1: #if this party has zero or fewer Pokemon
                                print("\n!! You cannot equip an empty party !!")
                                micropause()
                                continue #back to party options
                            userParty=party_i
                            equiped=party_dex
                            print(f"\nYou equipped {party_name}.")
                            shortpause()
                            #loops back to party options
                        elif megaChoice=='s' or megaChoice=='S':
                            #ask for file save name or default
                            #save every pokemon in the party to the file
                            savewhere=input("Where to save the party: ")
                            if savewhere=='': savewhere='pypokemon.sav'
                            for i in party_i:
                                i.save(savewhere)
                                print(f"Saved {i.name} to {savewhere}")
                                #micropause()
                            pass
                            #back to party options
                        elif megaChoice=='a' or megaChoice=='A':
                            #list pokemon from userParty and copy them into
                            #this party, party_i
                            while 1: #input loop for choosing pokemon, break when pokemon are added
                                print_party(userParty)
                                gigChoice = input("Which Pokémon to add?\n[#]'s or [b]ack: ")
                                if gigChoice=='b' or gigChoice=='B': break
                                if gigChoice=='all' or gigChoice=='All' or gigChoice=='ALL':
                                    pokis = userParty
                                    break
                                else:
                                    try: #number of a pokemon in userParty, 1-indexed
                                        pokis_i = [int(float(i)-1) for i in gigChoice.split()] #the indeces chosen
                                        pokis = [userParty[i] for i in pokis_i] # the pokemon selected
                                    except ValueError:
                                        print("\n** Try Again **")
                                        micropause()
                                        pass
                                    except IndexError:
                                        print("\n** Try Again **")
                                        micropause()
                                        pass
                                    else: #if all goes well, break the add pokemon input
                                        break
                            #take the selection, make a copy of each and add to selected party
                            for i in pokis:
                                party_i.append(copy.deepcopy(i))
                                print(f"{i.name} joined {party_name}!")
                            shortpause()
                            pass
                        elif megaChoice=='c' or megaChoice=='C':
                            #ask for a name for the copied party
                            #copy the party with the new name
                            coppy = input("Name the copy: ")
                            part_copy = copy.deepcopy(party_i)
                            players_parties.append((part_copy,coppy,party_count))
                            party_count += 1
                            print("\nCopied!")
                            micropause()
                            #loop back mans
                        elif megaChoice=='d' or megaChoice=='D': #deleting this party
                            #make sure this isnt the equipped party    
                            #ask if user is sure
                            #if so, delete it
                            if equipp:
                                print("No!")
                                micropause()
                                continue
                            print("\nThis party will be deleted, and these Pokémon released.")
                            shortpause()
                            deleConfirm = input(f"Are you sure you want to delete Party {party_name}?\n[y]es or [n]o: ")
                            if deleConfirm=="y" or deleConfirm=="Y":
                                byeParty=players_parties.pop(part_n)
                                print("\nDeleted!")
                                micropause()
                                break #leave poke party options screen go back to listing all parties
                        elif megaChoice=='r' or megaChoice=='R': #removing a pokemon
                            #make sure at least 1,
                            #ask whom to remove
                            #remove the selection
                            #if this is the equipped party, do not remove the last remaining pokemon
                            #user input loop
                            if sizep < 1:
                                print("\nNo Pokémon to remove!")
                                micropause()
                                continue
                            while 1: #input loop for pokemon removal
                                """
                                #display current party
                                #print("\n******** Party Pokémon ********\n*******************************\n")
                                #for i in range(len(userParty)):
                                    if userParty[i].dualType:
                                        thipe=typeStrings[userParty[i].tipe[0]]
                                        thipe+=" // "
                                        thipe+=typeStrings[userParty[i].tipe[1]]
                                    else:
                                        thipe=typeStrings[userParty[i].tipe[0]]
                                    print(f"[{i+1}] {userParty[i].name} \tLv. {userParty[i].level} \tHP: {format(userParty[i].currenthpp,'.2f')}% \t{thipe}")
                                print("\n*******************************\n")"""
                                remChoice=input("Which Pokémon to remove?\n[#] or [b]ack: ")
                                if remChoice=="b" or remChoice=="B":
                                    #print("Going back...")
                                    #shortpause()
                                    break #loop back to poke party options
                                #the entry should be 1-indexed indeces of mons to ditch
                                try:
                                    choices=np.array([int(float(i)-1) for i in remChoice.split()],dtype=int)
                                    print("")
                                    for i in range(len(choices)):
                                        if sizep==1 and equipp: #catch players trying to dump whole party when it is currently equipped
                                            print("!! Cannot remove last Pokémon from Party while equipped !!")
                                            break #loop back to party,
                                        if i==0: #keeps us from checking empty arrays i.e. choices[0:0]
                                            byeMon=party_i.pop(choices[i])
                                            print(f"{byeMon.name} has been released to the wild...")
                                            sizep=len(party_i)
                                        else:
                                            removedIndices=np.count_nonzero(choices[0:i]<choices[i]) #how many selected indices that are *lower* than current one have already been removed
                                            choices[i]-=removedIndices
                                            byeMon=party_i.pop(choices[i])
                                            sizep=len(party_i)
                                            print(f"{byeMon.name} has been released to the wild...")
                                        micropause()
                                    print("Selected Pokémon have been released!")
                                    shortpause() #kills
                                    break
                                except ValueError:
                                    print("\n!! Entry must be number or list of numbers separated by spaces !!")
                                    micropause()
                                except IndexError:
                                    print("\n!! Entry must correspond to Party Pokémon !!")
                                    micropause()
                            pass
                        elif megaChoice=='m' or megaChoice=='M': #empty, reset, clear, dump, all first letters already used here...
                            #make sure this isnt the equipped party
                            #ask if the user is sure
                            #if so, remove all the pokemon from party_i
                            #if equipp:
                                #print("No!")
                                #shortpause()
                                #continue
                            if sizep==0:
                                print("Why?")
                                shortpause()
                                continue
                            print("\nThese Pokémon will be released.")
                            shortpause()
                            resetConfirm=input(f"Are you sure you want to empty Party {party_name}?\n[y]es or [n]o: ")
                            if resetConfirm=="y" or resetConfirm=='Y':
                                #do it
                                party_i.clear()
                                #starter=makeMon(0)
                                #userParty.append(starter)
                                print(f"\n{party_name} has been emptied!")
                                if equipp: #if this party is equipped, populate it automatically
                                    bayleef = makeMon(0,nacher=(int(rng.choice((0,1,2,3,4))),int(rng.choice((0,1,2,3,4)))))
                                    bayleef.set_evs(tuple(random_evs()))
                                    party_i.append(bayleef)
                                sizep=len(party_i)
                                #micropause()
                                #print("Leaving Party Reset...")
                                shortpause() #kills
                            pass
                        else: #trying some numbers
                            #sigh, this is show pokemon summary right? okay whatever
                            try:
                                poke_selec = int(float(megaChoice)-1)
                                poke_s = party_i[poke_selec]
                                pass
                            except ValueError:
                                print("\n** Try Again **")
                                pass
                            except IndexError:
                                print("\n** Try Again **")
                                pass
                            else:
                                poke_s.summary()
                                pause=input("Enter anything to contine... ")
                                pass
                            pass
                    pass
                pass
            else: #?
                pass
        #after parties menu while loop
    ####what's the next spot?####

    #end of game, loops back to main screen
#runs after intial while loop
