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
import time as t
import numpy as np
from base_pokemon import mon, battle, field, checkBlackout, loadMon, makeMon, makeRandom, moveInfo, typeStrings, Weathers, Terrains, shortpause, dramaticpause, micropause
from moves import getMoveInfo,mov,natures
from dexpoke import dex
from victoryroad import c1_name,c2_name,c3_name,c4_name,c5_name,c1_party,c2_party,c3_party,c4_party,c5_party
rng=np.random.default_rng()
#
# YOOOOOOOOOOOO
# it's all GONE.... the game is RIGHT there v
############   give the player a starter  ###############
#user
starter= makeRandom()
##### creating the trainer for classic mode #####
rival= makeRandom(starter.level-1, 6)
#makeMon( rng.integers( len(dex) ), starter.level-1 )
rival2= makeRandom(starter.level+5, 6)
#makeMon( rng.integers( len(dex) ), starter.level+5 )
#bugs=rng.choice(mo,size=6,replace=False)
#rival.knownMoves=list(bugs)
#rival.PP=[mov[i]["pp"] for i in bugs]
#boos=rng.choice(mo,size=6,replace=False)
#rival2.knownMoves=list(boos)
#rival2.PP=[mov[i]["pp"] for i in boos]
#stuff them into their parties
userParty=[starter]
trainerParty=[rival,rival2]
#
opponentName="OPPONENT"
#####################
#load up a battlefield for classic mode
emerald = field(rando=True)
######################
print("\n... A Python game by Antoine ...")
shortpause()
print("** Welcome to the Wonderful World of Pokemon Simulation! **")
dramaticpause()
#aa:mainmenu
while 1:
    mainmenu = "\n[P]okemon\n[B]attle!\n[N]ursery\n[D]ex Selection\n[T]raining\n[M]ove Tutor\nPokemon [C]enter\n[O]pponent Set\nBattle [S]etting\n[R]eset Party\n[L]oad\nMove D[E]leter\n:"
    userChoice=input(mainmenu)
    ########################################################################################################
    #user setting the weather and terrain
    if userChoice=="s" or userChoice=="S":
        print("\n------------ Set the Stage of Battle ------------\n-------------------------------------------------")
        micropause()
        while 1: #user input loop
            print("Current Battle conditions:")
            micropause()
            print(f"Weather: {emerald.weather}\nTerrain: {emerald.terrain}")
            print("\nOptions:\n[1] Randomize weather and terrain\n[2] Randomize just weather\n[3] Randomize just terrain\n[4] Set manually\n")
            setChoice=input("What [#] would you like to do?\nor [b]ack: ")
            #go back
            if setChoice=="b" or setChoice=="B":
                break
            #randomize both
            if setChoice=="1":
                emerald.shuffleweather()
                print("Conditions have been randomized!")
                micropause()
            #randomize weather
            if setChoice=="2":
                emerald.shuffleweather(True,False)
                print("Weather has been randomized!")
                micropause()
            #randomize terrain
            if setChoice=="3":
                emerald.shuffleweather(False,True)
                print("Terrain has been randomized!")
                micropause()
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
                                emerald.weather=Weathers[int(newWeath)]
                                print("New weather set!")
                                break
                            except IndexError:
                                print("*\n** Entry out of range **\n*")
                            except ValueError:
                                print("*\n** Not a valid entry **\n*")
                    #weather
                    if conChoice=="2":
                        while 1: #user input loop, whats the new terrain
                            print("")
                            for i in range(len(Terrains)):
                                print(f"{i}\t{Terrains[i]}")
                            newTerr=input("What should the new terrain be?\n[#] or [b]ack: ")
                            if newTerr=="b" or newTerr=="B":
                                break
                            try:
                                emerald.terrain=Terrains[int(newTerr)]
                                print("New terrain set!")
                                break
                            except IndexError:
                                print("*\n** Entry out of range **\n*")
                            except ValueError:
                                print("*\n** Not a valid entry **\n*")
            #more options to change battle conditions
                                
    ####Reseting the Opponent in Classic Battle function####
    if userChoice=='o' or userChoice=="O":
        print("\n________ Opponent Reset ________")
        shortpause()
        aceChoice=input("Would you like to set your current team as the battle opponent?\n[y] or [b] to go back:")
        if aceChoice=='y' or aceChoice=="Y":
            trainerParty=copy.deepcopy(userParty)
            print("The Battle Opponent has a new Party! Good Luck!")
            shortpause() #kills
        else:
            print("Leaving Opponent Reset...")
            shortpause() #kills
        #end of opponent set, back to main screen

    #############################################   E4?   ###########################################################
    if userChoice=='4':
        ##### uhhhhh #####
        #e4 order will be Silver, Zinnia, Cynthia, N, largely because I said so
        #silver's battlefield will be...? rain
        gold = field(weath='rain') #Silvers battlefield
        gold.shuffleweather(False, True)
        silversParty=c1_party #gotta create somehow someway
        battle1 = battle(userParty, silversParty, gold, cpu_name = c1_name)
        resu1 = battle1.startbattle()
        #did the player win? gotta check for that lol
        #ask to heal the players pokemon
        #zinnia's battle
        zinniasP = c2_party
        sapphire = field(weath='sandstorm',terra='electric')
        #sapphire.shuffleweather(False,True)
        battle2 = battle(userParty,zinniasP,sapphire,cpu_name = c2_name)
        resu2 = battle2.startbattle()
        #win check
        #cynthias battle
        cynthsP=c3_party
        diamond = field(weath='hail',terra='psychic')
        battle3 = battle(userParty,cynthsP,diamond,cpu_name = c3_name)
        resu3 = battle3.startbattle()
        #N's battle
        nsP=c4_party
        black = field(weath='sunny',terra='misty')
        battle4 = battle(userParty, nsP, black,cpu_name = c4_name)
        resu4 = battle4.startbattle()
        #win
        #champ
        chP=c5_party
        indigo = field(terra='grassy') #clear weather, why not
        battle5 = battle(userParty, chP, indigo,cpu_name = c5_name)
        resu5 = battle5.startbattle()
        #if you won, you won, like it's over
        print("You defeated the Elite Four and their Champion!")
        shortpause()
        print("Congratulations! Cheers to the new Champion!")
        shortpause()
        #hall of fame where we highlight the party that just won
        pass
    #### end of e4? mode ###
    #### Classic Battle #### aa:battlemode
    if userChoice=="b" or userChoice=="B":
        ni, ny = checkBlackout(userParty)
        if ni==0:
            print("\nYou can't battle without a healthy Pokemon!")
            shortpause()
            continue #go back to main without starting the battle
        classicbattle = battle(userParty, trainerParty, emerald)
        classicbattle.startbattle()
        #then it should loop back to the main menu?
    ###end of battle block###
        
    #### check party pokemon? aa:pokemonparty ####
    if userChoice=="p" or userChoice=="P":
        while 1:
            print("\n******** Party Pokemon ********\n*******************************\n")
            for i in range(len(userParty)):
                if userParty[i].dualType:
                    thipe=typeStrings[userParty[i].tipe[0]]
                    thipe+=" // "
                    thipe+=typeStrings[userParty[i].tipe[1]]
                else:
                    thipe=typeStrings[userParty[i].tipe[0]]
                print(f"[{i+1}] {userParty[i].name} \tLv. {userParty[i].level} \tHP: {format(userParty[i].currenthpp,'.2f')}% \t{thipe}")
            print("\n*******************************\n")
            partyChoice=input("Enter a number to see a Pokemon's summary...\n[#] or [b]ack: ")
            #go back to main screen
            if partyChoice=='b' or partyChoice=="B":
                print("Leaving Party screen...")
                shortpause() #kills
                break
            try:
                pokeInd=int(partyChoice)-1
                selMon=userParty[pokeInd]
            except ValueError:
                print("\nEnter the number corresponding to a Pokemon!\nor [b] to go back")
            except IndexError:
                print("\nEnter the number corresponding to a Pokemon!\nor [b] to go back")
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
                                pause=input("\nEnter anything to continue back to Pokemon summary...")
                                break
                    #judge
                    if sumChoice=="j" or sumChoice=="J":
                        selMon.appraise()
            #end of while block
        print("Going back to main screen...")
        t.sleep(1)
        #end of party pokemon
    ###end of party display block###

    ####pokemon aa:nursery####
    if userChoice=='n' or userChoice=='N':
        print("\n____ Welcome to the Pokemon Nursery! ____")
        t.sleep(1)
        print("Here, you can create Pokemon from scratch!")
        t.sleep(1)
        ####nursery loop####
        while 1:
            nurseChoice=input("What do you want to do?\nNew [P]okemon!!\n[B]ack\n:")
            if nurseChoice=='b' or nurseChoice=='B':
                break #exits nursery loop
            ####new pokemon####
            if nurseChoice=='p':
                newName=input("Would you like to give your Pokemon a name?: ")
                print(f"Let's get {newName} some STATS")
                while 1: #stat input loop
                    statS=input("Enter 6 stats [1-255]\n[HP] [ATK] [DEF] [SPA] [SPD] [SPE]\n")
                    try:
                        stat=[int(float(i)) for i in statS.split(" ")]
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
                print("****************\nPokemon Types:\n0 Normal\n1 Fire\n2 Water\n3 Grass\n4 Electric\n5 Ice\n6 Fighting\n7 Poison\n8 Ground\n9 Flying\n10 Psychic\n11 Bug\n12 Rock\n13 Ghost\n14 Dragon\n15 Dark\n16 Steel\n17 Fairy\n****************")
                while 1: #type input loop
                    newTipe=input(f"Use the legend above to give {newName} a type or two: ")
                    try:
                        newTipe=[int(i) for i in newTipe.split()]
                        if max(newTipe)<=18: #no types above 18
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
                    lvlS=input(f"What level should {newName} be? 1-100: ")
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
                    print("Attack : 0\nDefense: 1\nSp. Atk: 2\nSp. Def: 3\nSpeed  : 4\n~~~~~~~~~~")
                    nachup = input(f"What should be {newName}'s boosted stat: ")
                    try:
                        nachup = int(nachup)
                        if (nachup <= 4) and (nachup >= 0):
                            break #stat good
                        else:
                            print("\n!! Enter a number between 0 and 4 !!")
                            t.sleep(.3)
                    except ValueError:
                        print("\n!! Enter a number !!")
                        t.sleep(.3)
                    ##okay if all goes well the code should progress here and we need to ask for hindered nature
                while 1:
                    print("\n~~~~~~~~~~\nAttack : 0\nDefense: 1\nSp. Atk: 2\nSp. Def: 3\nSpeed  : 4\n~~~~~~~~~~")
                    nachdo = input(f"What should be {newName}'s nerfed stat: ")
                    try:
                        nachdo = int(nachdo)
                        if (nachdo <= 4) and (nachdo >= 0):
                            break #stat is good, break input loop
                        else:
                            print("\n!! Enter a number between 0 and 4 !!")
                            t.sleep(.3)
                    except ValueError:
                        print("\n!! Enter a number !!")
                        t.sleep(.3)
                nacher = (nachup, nachdo)
                ##make the pokemon!##
                if len(newTipe)==1:
                    newMon=mon(lvlS,newName,nature=nacher,hpbase=stat[0],atbase=stat[1],debase=stat[2],sabase=stat[3],sdbase=stat[4],spbase=stat[5],tipe=np.array(newTipe))
                if len(newTipe)>1:
                    newMon=mon(lvlS,newName,nature=nacher,hpbase=stat[0],atbase=stat[1],debase=stat[2],sabase=stat[3],sdbase=stat[4],spbase=stat[5],tipe=np.array([newTipe[0],newTipe[1]]))
                print(f"\n{newName} is born!")
                t.sleep(1)
                userParty.append(newMon)
                print("Take good care of them!")
            pass #loops back to start of nursery
        pass #loops back to start of game
    ###end of nursery block
    
    ####training####
    if userChoice=='t':
        print("\n********SuperHyper Training********\nYou can add EVs and IVs to your Pokemon!")
        while 1:
            #choose a pokemon
            print("\n")
            for i in range(len(userParty)):
                print(f"[{i+1}] {userParty[i].name} \tLv. {userParty[i].level}")
            trainChoice=input("Which Pokemon will we train?:\n[#] or [b]ack: ")
            
            #option to go back, from pokemon selection to main screen
            if trainChoice=='b':
                break
            #user input loop, making sure input is poke#
            while 1:
                try:
                    pokeIndex=int(trainChoice)-1
                    pokeTrain=userParty[pokeIndex]
                    break #confirmed numbers are good, exit user loop
                except:
                    print("\n**Must enter a number of a Pokemon**")
                    trainChoice=input("\nWhich Pokemon will we train?:\n[#]")
                    #ends error catch for pokemon selection
            print(f"\n**** {pokeTrain.name} ****")
            superHyper=input("Manage [E]Vs or [I]Vs or [L]evels\n:") #anything other than options below will skip to the next loop of choose a pokemon
            
            #EVs
            if superHyper=='e':
                while 1:
                    evs=input("Enter 6 numbers (0-252) all at once.\nEVs cannot sum >510.:\n")
                    #option to go back
                    if evs=='b':
                        break #throws us back to choose a pokemon
                    else:
                        evs=evs.split()
                        try:
                            eves=np.array([int(evs[0]),int(evs[1]),int(evs[2]),int(evs[3]),int(evs[4]),int(evs[5])])
                            #make sure values are legal
                            if np.max(eves)<=252.:
                                if np.sum(eves)<=510.:
                                    pokeTrain.hpev=int(evs[0])
                                    pokeTrain.atev=int(evs[1])
                                    pokeTrain.deev=int(evs[2])
                                    pokeTrain.saev=int(evs[3])
                                    pokeTrain.sdev=int(evs[4])
                                    pokeTrain.spev=int(evs[5])
                                    pokeTrain.reStat()
                                    t.sleep(1)
                                    print("\nTraining...")
                                    t.sleep(1)
                                    print(f"\n{pokeTrain.name} finished Super Training and has new stats!")
                                    break #ends ev training, sends back to choose a pokemon
                                else:
                                    print("\n**No more than 510 EVs**")
                                    pass
                                pass
                            else:
                                print("\n**No more than 252 EVs in any stat.**")
                                pass
                            pass
                        except: #catch non-numbers, incomplete sets
                            print("\n**Max EV is 252.**\n**Total EVs cannot sum more than 510.**\n**Input 6 numbers separated by spaces.**")    
                        #if code is here, EV training while loop continues
                    pass
                #end of ev training loop
            
            #IVs        
            if superHyper=='i':
                while 1:
                    ivs=input("Enter 6 numbers (0-31) all at once.:\n")
                    #option to go back, from iv input to choose a pokemon
                    if ivs=='b':
                        break
                    else:
                        ivs=ivs.split() #6 numbers into list of strings
                        try:
                            #make sure we have 6 numbers
                            ives=np.array([int(ivs[0]),int(ivs[1]),int(ivs[2]),int(ivs[3]),int(ivs[4]),int(ivs[5])])
                            if np.max(ives)<=31:
                                pokeTrain.hpiv=int(ivs[0])
                                pokeTrain.ativ=int(ivs[1])
                                pokeTrain.deiv=int(ivs[2])
                                pokeTrain.saiv=int(ivs[3])
                                pokeTrain.sdiv=int(ivs[4])
                                pokeTrain.spiv=int(ivs[5])
                                pokeTrain.reStat()
                                t.sleep(1)
                                print("\nTraining...")
                                t.sleep(1)
                                print(f"{pokeTrain.name} finished Hyper Training and has new stats!")
                                t.sleep(1)
                                break #ends IV training, goes back to choose a pokemon
                            else:
                                print("\n**Maximum IV is 31**")
                        except IndexError: #input couldn't fill 6-item array
                            print("\n**Enter !6! numbers separated by spaces**")
                        except ValueError: #we tried to make an int() out of something non-number
                            print("\n**Enter 6 !numbers! separated by spaces**")
                        #if we get here, an IV was more than 31, loops back to IV input
                    #end of iv input loop
                #end of IV training loop
            
            #level
            if superHyper=='l':
                while 1:
                    try:
                        levl=int(input(f"What level should {pokeTrain.name} be?: "))
                        if levl>0.: #if input was a positive number
                            pokeTrain.level=levl #set pokemon's new level
                            pokeTrain.reStat() #recalcs stats
                            print("\nTraining...")
                            t.sleep(1)
                            print(f"\n{pokeTrain.name} finished training and has new stats!")
                            t.sleep(1)
                            break #exits user input loop
                        else:
                            print("\n**Level must be at least 1**")
                    except:
                        print("\n**Enter a number greater than 0.**")
                    #end of level input while block
                #end of level training block
                
            pass #loops back to training screen
        print("\nLeaving SuperHyper Training...")
        t.sleep(1) #exiting training
    ###end of training block###
    #zz:training
    #aa:movetutor
    ####move learner####
    if userChoice=='m':
        print("\n****************************\n******** Move Tutor ********\n****************************\n\nYou can teach your Pokemon new moves!\n")
        while 1: #choose a pokemon
            print("\n******** Party Pokemon ********\n*******************************\n")
            for i in range(len(userParty)):
                if userParty[i].dualType:
                    thipe=typeStrings[userParty[i].tipe[0]]
                    thipe+=" // "
                    thipe+=typeStrings[userParty[i].tipe[1]]
                else:
                    thipe=typeStrings[userParty[i].tipe[0]]
                print(f"[{i+1}] {userParty[i].name} \tLv. {userParty[i].level} \tHP: {format(userParty[i].currenthpp,'.2f')}% \t{thipe}")
            print("*******************************\n")
            learnChoice=input("Enter the number of a Pokemon\n[#], [m]ove info, or [b]ack: ")
            #go back
            if learnChoice=='b' or learnChoice=='B':
                print("Leaving Move Tutor...")
                shortpause() #kills
                break #go back to main screen
            if learnChoice=="m" or learnChoice=="M":
                #print all the moves
                print("\n------------ Pokemon Moves ------------")
                for i in range(len(mov)):
                    print(f"{mov[i]['index']}\t| {mov[i]['name']}\t| {typeStrings[mov[i]['type']]}")
                print("------------------------")
                while 1:
                    mpChoice=input("Which moves do you want to see?\n[#] or [b]ack: ")
                    if mpChoice=="b" or mpChoice=="B":
                        shortpause()
                        break
                    try:
                        movez=mpChoice.split() #pokemon movelist index (string)
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
                        pause=input("\nEnter anything to continue back to Pokemon summary...")
                        continue
            else:
                try:
                    learnChoice=int(learnChoice)
                    studentMon=userParty[learnChoice-1]
                    print(f"{studentMon.name} is ready to learn...") #confirmation readout, user choice intiated a pokemon
                except ValueError:
                    print("** Enter a [#] corresponding to a Pokemon !!**\n")
                except IndexError:
                    print("** Enter a [#] corresponding to a Pokemon !!**\n")
                else:
                    #otherwise, print the moves, godspeed
                    print("\n------------ Pokemon Moves ------------")
                    for i in range(len(mov)):
                        print(f"{mov[i]['index']}\t| {mov[i]['name']}\t| {typeStrings[mov[i]['type']]}")
                    print("------------------------")
                    while 1: #input loop
                        chooseMove=input(f"Which moves should {studentMon.name} learn?\n[#] separated by spaces: ")
                        #go back to choose a pokemon
                        if chooseMove=='b' or chooseMove=='B':
                            break
                        if chooseMove.split()[0]=='random':
                            try:
                                n_moves = int(chooseMove.split()[1])
                            except ValueError:
                                print('\n**Bad Value**')
                            except IndexError:
                                print('\n**Bad Index**')
                            else:
                                studentMon.randomizeMoveset(n_moves)
                                break #randomized moves, go back to pokemon selecting loop
                        #extract and apply moves
                        try:
                            chooseMoves=chooseMove.split() #separate move indices into own strings
                            moveInts=[int(i) for i in chooseMoves] #(try to) convert strings to ints
                            incomplete=False
                            if max(moveInts)<len(mov): #make sure all indices have an entry in the movedex
                                if min(moveInts)>=0: #ward off negative numbers
                                    for i in moveInts:
                                        if i in studentMon.knownMoves:
                                            print(f"! {studentMon.name} already knows {getMoveInfo(i)['name']} !\n")
                                            incomplete=True
                                        else:
                                            studentMon.knownMoves.append(i)
                                            studentMon.PP.append(getMoveInfo(i)['pp'])
                                            print(f"{studentMon.name} learned {getMoveInfo(i)['name']}!")
                                    if incomplete==False: #if there are no conflicts
                                        break #all moves added, breaks loop and goes back to choose a pokemon
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

    ####make pokemon from pokedex (use preset stats)####
    if userChoice=='d':
        print("\n*****************************\n******** The Pokedex ********\n*****************************\n\n")
        t.sleep(1)
        while 1: #choose new pokemon loop
            print(dex)
            pokeChoice=input("Which pokemon would you like to add to your team?\n[#] or [b]ack: ")
            if pokeChoice=='b':
                print("Leaving Pokedex...")
                shortpause() #kills
                break
            if pokeChoice=='B':
                print("Leaving Pokedex...")
                shortpause() #kills
                break
            try:
                pokeChoices=pokeChoice.split()
                pokInts=[int(i) for i in pokeChoices]
                if max(pokInts)<len(dex):
                    if min(pokInts)>=0:
                        for i in pokInts:
                            newbie=makeMon(i,userParty[0].level)
                            print(f"{newbie.name} is born!")
                            t.sleep(1)
                            userParty.append(newbie)
                            print(f"{newbie.name} has been added to your party!")
                            t.sleep(1)
                            print("Take good care of them!")
                    else: #failing brings you back to new pokemon loop
                        print("** That's out of bounds... **\n")
                else: #new pokemon loop
                    print("** That's out of bounds... **\n")
            except ValueError:
                print("** Try again **\n")
            except IndexError:
                print("** That's out of bounds... **\n")
    ###end of making preset pokemon
    
    ####Loading pokemon
    if userChoice=='l':
        print("******** Load Pokemon ********\n\nYou can load previously saved pokemon!\n")
        while 1: #savefile input loop
            saveChoice=input("What save file to load?\n[blank] entry to use default or [b]ack\n: ")
            #go back
            if saveChoice=='b' or saveChoice=='b':
                print("Leaving Load Pokemon..")
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
                    t.sleep(1)
                print("Finished loading Pokemon!\n")
                t.sleep(1)
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
                        t.sleep(1)
                    print("Finished loading Pokemon!\n")
                    t.sleep(1)
                    #loop back to load a save
                #
            #loop back to load a save
        #done loading save
    ###end of load save block###
    
    ####pokemon center#### let's heal em up
    if userChoice=="c":
        print("\n******** Welcome to the Pokemon Center ********\n")
        shortpause()
        print("We can heal your Pokemon to full health!")
        t.sleep(1)
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
    if userChoice=='r':
        print("\n******** Party Reset ********")
        shortpause()
        print("\nYou can remove individual Pokemon from your party...")
        micropause()
        print("Or you can reset your team to just the starter (Bulbasaur for now)")
        shortpause()
        while 1: #input loop only to catch players leaving individual pokemon removal
            resChoice=input("What would you like to do?\n[C]hoose Pokemon, [R]eset team, or [b]ack: ")
            
            if resChoice==("b" or "B"):
                print("Leaving Party Reset...")
                shortpause() #kills
                break
                
            if resChoice==("r" or "R"):
                userParty.clear()
                starter=makeMon(0)
                userParty.append(starter)
                print("Your party has been reset!")
                shortpause()
                print("Leaving Party Reset...")
                shortpause() #kills
                break
            
            if resChoice==("c" or "C"):
                #user input loop
                while 1:
                    #display current party
                    print("\n******** Party Pokemon ********\n*******************************\n")
                    for i in range(len(userParty)):
                        if userParty[i].dualType:
                            thipe=typeStrings[userParty[i].tipe[0]]
                            thipe+=" // "
                            thipe+=typeStrings[userParty[i].tipe[1]]
                        else:
                            thipe=typeStrings[userParty[i].tipe[0]]
                        print(f"[{i+1}] {userParty[i].name} \tLv. {userParty[i].level} \tHP: {format(userParty[i].currenthpp,'.2f')}% \t{thipe}")
                    print("\n*******************************\n")
                    remChoice=input("Which Pokemon to remove?\n[#] or [b]ack: ")
                    
                    if remChoice==("b" or "B"):
                        print("Going back...")
                        #shortpause()
                        break
                    try:
                        choices=np.array([int(i)-1 for i in remChoice.split()])
                        for i in range(len(choices)):
                            if len(userParty)==1: #catch players trying to dump whole party
                                print("!! Cannot remove last Pokemon from Party !!")
                                break
                            if i==0: #keeps us from checking empty arrays i.e. choices[0:0]
                                byeMon=userParty.pop(choices[i])
                                print(f"{byeMon.name} has been released to the wild...")
                            else:
                                removedIndices=np.count_nonzero(choices[0:i]<choices[i]) #how many selected indices that are *lower* than current one have already been removed
                                choices[i]-=removedIndices
                                byeMon=userParty.pop(choices[i])
                                print(f"{byeMon.name} has been released to the wild...")
                        print("Selected Pokemon have been released!")
                        shortpause() #kills
                        break
                    except ValueError:
                        print("\n!! Entry must be number or list of numbers separated by spaces !!")
                    except IndexError:
                        print("\n!! Entry must correspond to Party Pokemon !!")
    
    #move deleting
    if userChoice=="e" or userChoice=="E":
        print("\n******** Move Deleter ********")
        shortpause()
        print("\nHere you can get rid of unwanted moves.")
        shortpause()
        while 1: #user input loop
            print("\n******** Party Pokemon ********\n*******************************\n")
            for i in range(len(userParty)):
                if userParty[i].dualType:
                    thipe=typeStrings[userParty[i].tipe[0]]
                    thipe+=" // "
                    thipe+=typeStrings[userParty[i].tipe[1]]
                else:
                    thipe=typeStrings[userParty[i].tipe[0]]
                print(f"[{i+1}] {userParty[i].name} \tLv. {userParty[i].level} \tHP: {format(userParty[i].currenthpp,'.2f')}% \t{thipe}")
            print("\n*******************************\n")
            leteChoice=input("Select a Pokemon [#] to look at\nor [b]ack: ")
            #go back
            if leteChoice=="b" or leteChoice=="B":
                print("Leaving Move Deleter...")
                shortpause()
                break
            try:
                select=userParty[int(leteChoice)-1]
            except ValueError:
                print("\n** Enter [#] of a pokemon above! **")
            except IndexError:
                print("\n** Use the legend to enter [#] of a Pokemon! **")
            else:
                while 1: #user input loop
                    select.summary()
                    mvChoice=input("Which moves should be deleted?\n[#] or [b]ack: ")
                    if mvChoice=="b" or mvChoice=="B":
                        shortpause()
                        break
                    try:
                        chooz=np.array([int(i)-1 for i in mvChoice.split()])
                        for i in range(len(chooz)):
                            if len(select.knownMoves)==1: #catch players trying to dump whole moveset
                                micropause()
                                print("** Pokemon cannot forget its last move **")
                                break
                            if i==0: #keeps us from checking empty arrays i.e. choices[0:0]
                                byeMove=select.knownMoves.pop(chooz[i])
                                byePP = select.PP.pop(chooz[i])
                                micropause()
                                print(f"{select.name} forgets {mov[byeMove]['name']}...")
                            else:
                                removedIndices=np.count_nonzero(chooz[0:i]<chooz[i]) #how many selected indices that are *lower* than current one have already been removed
                                chooz[i]-=removedIndices
                                byeMove=select.knownMoves.pop(chooz[i])
                                byePP = select.PP.pop(chooz[i])
                                micropause()
                                print(f"{select.name} forgets {mov[byeMove]['name']}...")
                        print("Selected moves have been forgetten!")
                        shortpause() #kills
                        break
                    except ValueError:
                        print("\n** Entry must be [#] or list of [#]s separated by spaces! **")
                    except IndexError:
                        print("\n** Entry must correspond to Pokemon move! **")
            #
    ####what's the next spot?####

    #end of game, loops back to main screen
#runs after intial while loop
