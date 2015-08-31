import os
import sys
import time
from random import random, randint, sample
import gamestate

from util import say, print_color

from carnival import game, talkToCarnie, talkToBeardedLadies
from rpg import detect_enemy, fight, prompt

# /////////////////////////////////////////////////////////////////////////////
# Bobo's room
# /////////////////////////////////////////////////////////////////////////////

def talkToBobo(gamestate,*args,**kwargs):
    boboStates = ['no', 'yes']
    boboResponses = ['Bobo says %s%s' % (x,x) for x in boboStates]
    boboActivities = {
        "n": 
            [
            "scratches his butt",
            "throws some poo at you",
            "gives you the hairy eyeball",
            "looks generally annoyed"
            ],
        "y":
            ["sings Ave Maria",
             "gives you a flower, but it disintegrates immediately",
             "recites a beautiful Shakespeare sonnet",
             "cures cancer"
            ]
    }


    print "What would you like to say to Bobo?"
    question = raw_input()
    print boboResponses[randint(0,len(boboResponses)-1)]

    youLikey = 'x'
    while youLikey not in 'yn' :
        print "Do you like Bobo's response? [y/n]"
        youLikey = raw_input().lower()

    print "Fine, Bobo %s"%sample(boboActivities[youLikey],1)[0]


def play(gamestate,*args,**kwargs) :
    print "Bobo looks at you with childlike excitement!"
    time.sleep(3)
    game_width = 25
    curr_pos = (0,0)
    win_pos = (randint(0,game_width),randint(0,game_width))
    while curr_pos != win_pos :
        board = [['.' for _ in range(game_width)] for __ in range(game_width)]
        board[curr_pos[1]][curr_pos[0]] = 'B'
        board[win_pos[1]][win_pos[0]] = 'X'
        os.system("clear")
        print '\n'.join(''.join(_) for _ in board)
        print 'Control Bobo! [jkhl]'
        move = raw_input()
        if move not in 'jkhl' :
            continue
        elif move == 'j' :
            curr_pos = (max(0,min(curr_pos[0],game_width)),
                        max(0,min(curr_pos[1]+1,game_width)))
        elif move == 'k' :
            curr_pos = (max(0,min(curr_pos[0],game_width)),
                        max(0,min(curr_pos[1]-1,game_width)))
        elif move == 'h' :
            curr_pos = (max(0,min(curr_pos[0]-1,game_width)),
                        max(0,min(curr_pos[1],game_width)))
        elif move == 'l' :
            curr_pos = (max(0,min(curr_pos[0]+1,game_width)),
                        max(0,min(curr_pos[1],game_width)))


# /////////////////////////////////////////////////////////////////////////////
# Cave
# /////////////////////////////////////////////////////////////////////////////

def caveDescription(room):
    if 'manDead' in room:
        print "You see the carcass of an old man.  It smells funny."
    else:
        print("You are in a cave, an old man stands in the center.  His beard is long and\n" 
          "wizardly: sophisticated yet non-intimidating.  To his left and right are two\n" 
          "fires.  He looks like a friendly chap")


def talkToMan(gamestate):
    room = gamestate.currentRoom()
    if not 'sword' in gamestate.inventory():
        say ("The man tells you that it is dangerous to go alone and to take this \n"
             "You acquire the wooden sword <uplifting, yet short, acquisation tune plays>.")
        gamestate.addToInventory('sword')
        gamestate.markAchieved('gotSword')
    else:
        say ("The man tells you to get going.  He's old and the world is made for the young. \n"
             "He tells you that you should go kill things, but watch out for exploding barrels and \n"
             "stray HP Lovecraft beasts.")

def killMan(gamestate):
    room = gamestate.currentRoom()
    print "You strike the man and steal his monies.  The world is cruel, but yet you are rewarded."
    gamestate.inventory()['monies'] += 200
    room['manDead'] = True
    del(room['uses'][('sword', 'man')])
    del(room['actions']['talk']['man'])

# /////////////////////////////////////////////////////////////////////////////
# Playpen
# /////////////////////////////////////////////////////////////////////////////

def playpenDescription(room):
    print "You are in a Bobo's playpen.",
    if('ball' not in gamestate.inventory()):
        print "It's sparse, but it does have a big bouncy ball.  There is a passage to the south."
    else:
        print "It's sparse and soulless. And now ball-less.  There is a passage to the south."
    if 'dongedDoor' in room and 'keyedDoor' in room:
        print "To the west is an opened door.  You smell a spicy odor eminating in that direction."
    else:
        print "To the west is a locked door.  It has both a regular keyhole and another oddly shapped hole."

def takeBall(gamestate):
    room = gamestate.currentRoom()
    gamestate.addToInventory('ball')
    del(gamestate.room('playpenRoom')['actions']['take'])
    del(gamestate.room('playpenRoom')['actions']['bounce'])
    print "You take the ball.  The room suddenly seems less joy filled."

def keyDoor(gamestate):
    room = gamestate.currentRoom()
    print "The key breaks as you turn it, but the door is partially unlocked!"
    if 'key' in gamestate.inventory():
        if 'key' in gamestate.inventory():
            gamestate.removeFromInventory('key')
            room['keyedDoor'] = True
    if 'dongedDoor' in room and 'keyedDoor' in room:
        openDoor(gamestate)

def dongDoor(gamestate):
    room = gamestate.currentRoom()
    print "The dong slips in all smooth and natural like."
    room['dongedDoor'] = True
    if 'dongedDoor' in room and 'keyedDoor' in room:
        openDoor(gamestate)

def openDoor(gamestate):
    room = gamestate.currentRoom()
    print "The door swings open."
    gamestate.markAchieved('spicyRoom')
    room['adjacent'].append((['west', 'door'], 'secretRoom'))
    
# /////////////////////////////////////////////////////////////////////////////
# KitchenDickTip
# /////////////////////////////////////////////////////////////////////////////

def kitchenDickDescrip(room):
    room = gamestate.currentRoom()
    print "You are at the end of a long, strong, and oddly well hung road."
    print 'There is a sign to your right reading "Kitchen-Dick Road."'
    if not 'noEdwardo' in room:
        print "To your left is a mustachioed man with greasy, slicked back hair, and a long trench coat."
        print "Needless to say this dude looks totally legit.  But then again who can tell.  On thing you're"
        print "sure of is that this dude has no balls."

def talkToEdwardo(gamestate):
    room = gamestate.currentRoom()
    say("Ehhhh, ehhhhh, right up the pooftah.")

    if 'key' in gamestate.inventory():
        return

    say("Would you like to buy a key, only $200?")
    if(prompt("Buy the creepy dude's key? ") == 'y'):
        moniesAmount = gamestate.inventory()['monies']
        if moniesAmount < 200:
            say("You trying to swindle me!")
            return
        print "The dude chuckles and hands you a key."
        gamestate.inventory()['monies'] -= 200
        gamestate.addToInventory('key')
        room['edwardoGaveKey'] = True
    else:
        say("Hehehehe, I have a feeling you'll need it.")

def noDeathToEdwardo(gamestate):
    say("Oh-ho-ho")
    print "Edwardo (the creepy dude) bobs and weaves his way out of your stubby, stabby, swords path."

def edwardoJustNeedsSomeBalls(gamestate):
    room = gamestate.currentRoom()
    print "Edwardo looks so happy playing with the balls.  Suddenly his trench-coat dissapears, his hair"
    print "unslickifies, his mustache dissappears.  He now takes on the appearance of an upstanding"
    print "gentlemen."
    print
    say("The kindness you have shown me has warmed my heart dear stranger.  Here have what I have.")
    print
    print "Then Edwardo dissapears."
    print
    print "Sheeeeeeeeeiiiit"
    gamestate.inventory()['monies'] += 200
    if not 'edwardoGaveKey' in room:
        gamestate.addToInventory('key')
    room['noEdwardo'] = True

    del(room['actions']['talk'])
    toRemove = []
    for use in room['uses']:
        if room['uses'][use] == noDeathToEdwardo or room['uses'][use] == edwardoJustNeedsSomeBalls:
            toRemove.append(use)
    for use in toRemove:
        del(room['uses'][use])

# /////////////////////////////////////////////////////////////////////////////
# Secret Spicy Room 
# /////////////////////////////////////////////////////////////////////////////

def talkToSkelly(gamestate):
    say("Ridde me these three and a reward will be yours he-he-he")
    riddles = [
          ("How does Juan-De-Fuca answer test questions?", "wrong")
        , ("What does Juan-De-Fuca like to eat with Indian Food?", "naan")
        , ("What does Juan-De-Fuca smoke his wacky-tobaccy out of?", "bong")
        , ("What do you call a group of Juan-De-Fucas?", "throng")
        , ("What kind of car does Juan-De-Fuca drive?", "honda")
        , ("What does Juan-De-Fuca use to kill civvies?", "bomb")
        , ("Who's Juan-De-Fuca's favorite Chinese dictator?", "mao zedong")
    ]
    choices = range(0, len(riddles))
    
    for i in xrange(0,3):
        choiceNum = randint(0,len(choices)-1)
        q = choices[choiceNum]
        choices.remove(q)

        question     = riddles[q][0]
        expectAnswer = riddles[q][1]

        say(question)
        say("The answer is: <blank> de-fuca")
        print "You answer> ",
        gaveAnswer = raw_input()
        gaveAnswer = gaveAnswer.lower()

        if gaveAnswer in expectAnswer:
            say("That's right %s de Fuca!" % expectAnswer)
        else:
            say("Wrong!  It's %s de Fuca!" % expectAnswer)
            say("Begone scummy scummersons!")
            return

    say("Alright, you are truly a worthy advesary!")
    gamestate.markAchieved('deFuca')

# /////////////////////////////////////////////////////////////////////////////
# Persistent actions
# /////////////////////////////////////////////////////////////////////////////


def go(room, direction):
    direction = direction[0]
    room = gamestate.currentRoom()
    adjacencies = room['adjacent']
    for (expectedDirs, exitsTo) in adjacencies:
        for expectedDir in expectedDirs:
            if(expectedDir == direction):
                gamestate.moveTo(exitsTo)
                return

    print "Can't go that way."


def look(room, noun):
    print "Upon deep inspection of the room you realize that. "

    adjacencies = room['adjacent']
    if len(adjacencies) == 0:
        print "There are no adjacent rooms"

    print "You may get to an adjacent location with one of the magic words:  %s" % ', '.join(dirs[0] for (dirs,room) in adjacencies)

def exit(room, noun):
    if(prompt("Really exit? ") == 'y'):
        sys.exit(1)

def inventory(room, noun):
    inventory = gamestate.inventory()
    if len(inventory) == 0:
        print "You have nothing in your inventory"
        return
    print "You have the following in your inventory:"
    for item,num in inventory.items():
        item_str = item if num is None else '%s (%d)'%(item,num)
        print "   * ", item_str

def use(room, nouns):
    nouns = set(nouns)

    subject = None
    objecto = None
    for noun in nouns:
        if noun in gamestate.inventory():
            subject = noun

    if subject is None:
        print "Use what?"
        return

    if not subject is None:
        nouns.remove(subject)
    if(len(nouns) > 0):
        objecto = list(nouns)[0]

    if objecto is None:
        print "Use %s on what?" % subject
        return

    didIt = False
    if 'uses' in room:
        if (subject, objecto) in room['uses']:
            didIt = True
            room['uses'][(subject, objecto)](gamestate)

    if not didIt:
        print "Don't know how to do that..."

def suckit(room, nouns):
    if gamestate.howManySuckedIt() < 3:
        print "Sucked it good, but bobo looks like it wants more."
        gamestate.youSuckedIt()
        if gamestate.howManySuckedIt() == 3:
            print "The legendary wolfdong has appeared in your inventory.\n(It looks like a normal dong shaft but its got a wolf head on the end with glowing eyes and its dripping acid saliva.)"
            gamestate.markAchieved('gotDong')
    else:
        print "You might have a problem."

def hint(room, nouns):
    print gamestate.nextHint()

PERSISTENT_VERBS = ["go","fight","look","exit","inventory","use","suckit","hint"]
PERSISTENT_NOUNS = ["north", "south", "west", "east"]
PERSISTENT_ACTIONS = {   "go": go
                       , "fight":fight
                       , "look":look
                       , "exit":exit
                       , "inventory":inventory
                       , "use":use
                       , "suckit":suckit
                       , "hint":hint
                     }

# /////////////////////////////////////////////////////////////////////////////
# Game logic
# /////////////////////////////////////////////////////////////////////////////
def title():
    print ""
    print ""
    print " ()()()     ()    ()()()      ()         __               "
    print " ()   ()  ()  ()  ()   ()   ()  ()      |      /\   \   / "
    print " ()()()   ()  ()  ()()()    ()  ()       \    /  \   \ /  "
    print " ()   ()  ()  ()  ()   ()   ()  ()        |  /----\   |   "
    print " ()()()     ()    ()()()      ()        --' /      \  |   "
    print "                                                          "
    print "  NNNN       NN     OOOOO                   !!!!    !!!!  "
    print "  NNNNNN     NN    OOOOOOO                  !!!!    !!!!  "
    print "  NN  NNNN   NN   OOO    OO                 !!!!    !!!!  "
    print "  NN    NNN  NN   OO     OO                 !!!!    !!!!  "
    print "  NN      NN NN   OO     OO                 !!!!    !!!!  "
    print "  NN       NNNN   OOO   OOO                 !!!!    !!!!  "
    print "  NN        NNN    OOOOOOO                  !!!!    !!!!  "
    print "  NN         NN     OOOOO                   !!!!    !!!!  "
    print "                                            !!!!    !!!!  "
    print "              NNNN       NN     OOOOO       !!!!    !!!!  "
    print "              NNNNNN     NN    OOOOOOO      !!!!    !!!!  "
    print "              NN  NNNN   NN   OOO    OO     !!!!    !!!!  "
    print "              NN    NNN  NN   OO     OO     !!!!    !!!!  "
    print "              NN      NN NN   OO     OO                   "
    print "              NN       NNNN   OOO   OOO     !!!!    !!!!  "
    print "              NN        NNN    OOOOOOO      !!!!    !!!!  "
    print "              NN         NN     OOOOO       !!!!    !!!!  "


def listOfAllVerbs(currentVerbs):
    res = currentVerbs
    res.extend(PERSISTENT_VERBS)
    return res

def parseCommand(command, room):
    actions = room['actions']
    legalVerbs = listOfAllVerbs(actions.keys())
    legalNouns = computeSetOfLegalNounsForRoom(room, legalVerbs)

    command = command.lower()
    verb = 'none'
    nouns = ['none']
    for word in command.split():
        if word in legalVerbs:
            verb = word
        elif word in legalNouns:
            nouns.append(word)

    if len(nouns) > 1:
        nouns.remove('none')
    return (verb, nouns)


def evaluateAction(cmd, room):
    actions  = room['actions']

    (verb, nouns) = cmd
    noun = nouns[0]
    if verb in actions:
        if noun in actions[verb]:
            actions[verb][noun](gamestate)
        else:
            print "Don't know how to do that..."
    elif verb in PERSISTENT_ACTIONS:
        PERSISTENT_ACTIONS[verb](room, nouns)
    else:
        print "Don't know how to do that..."


def i(s) :
    def _(*args,**kwargs) :
        print s
    return _

def computeSetOfLegalNounsForRoom(room, legalVerbs):
    """ Yeah this function sucks """
    actions = room['actions']

    legalNouns = set(PERSISTENT_NOUNS)
    for verb in legalVerbs:
        if verb in actions:
            for noun in actions[verb]:
                legalNouns.add(noun)

    # Add adjacencies
    for adjacency in room['adjacent']:
        for direction in adjacency[0]:
            legalNouns.add(direction)

    # Add any use targets
    if 'uses' in room:
        for (item, tgt) in room['uses']:
            legalNouns.add(tgt)

    # Add inventory items
    legalNouns |= set(gamestate.inventoryItems())

    return legalNouns


def gameLoop():
    boboRoom = {}
    boboRoom['description'] = i("You are in a room with Bobo. There is nothing else but Bobo.\n" 
                              "There's an open door behind you (south). There is a passage to the north.")
    boboRoom['adjacent'] = [  (['north', 'passage', 'playpen'], 'playpenRoom')
                            , (['south', 'door', 'behind', 'backwards', 'outside'], 'outside')]
    boboRoom['actions'] = \
        {  "smirk":     {   'none': i('Smirk at who?')
                          , 'bobo': i("Bobo smirks back at you")
                        }
         , "talk":      {   'none': i("Talk to who?")
                          , 'bobo': talkToBobo
                        }
         , "play":      {   'none': i("With yourself?!")
                          , 'bobo': play
                        }
        }
    boboRoom['uses'] = \
        {    ('ball', 'bobo'):  i("Bobo is extremly happy playing with the ball!")
           , ('monies', 'bobo'): i("Bobo is beyond the kind of material wealth that makes humans happy.")
           , ('sword', 'bobo'): i("Nooooo!!!!! You could never hurt Bobo.")
        }

    playpenRoom = {}
    playpenRoom['description'] = playpenDescription
    playpenRoom['adjacent'] = [(['south', 'passage'], 'boboRoom')]
    playpenRoom['actions'] = \
        {  "bounce":     {   'none': i('Bounce what?')
                           , 'ball': i("The ball bounces: what fun!")
                         }
         , "take":       {   'none': i("Take what?")
                           , 'ball': takeBall
                         }
        } 
    playpenRoom['uses'] = {
             ('key', 'door'):      keyDoor
           , ('wolfdong', 'door'): dongDoor
           , ('dong', 'door'):     dongDoor
        }

    secretRoom = {}
    secretRoom['description'] = i("You're in the secret spicy room.  Standing in the middle is an animated skeleton\n"
                                  "The skeleton seems friendly but you have a feeling this his wit may be a little dry.\n"
                                  "To the east an open door.")
    secretRoom['adjacent'] = [(['east', 'door'], 'playpenRoom')]
    secretRoom['actions'] = {
               "talk":      {   'none': i("Talk to who?")
                              , 'skeleton': talkToSkelly
                            }
    }
    secretRoom['uses'] = {}

    outside = {}
    outside['description'] = i("You are in the great oudoors. There's lots of trees and clouds\n" 
                             "and chirping birds and shit. " 
                             "Looking around you see the entrance to Bobo's hut to the north,\n" 
                             "there is a cave off the east,"
                             "and there is a carnival off to the west.\n"
                             "To the south is a long, strong, and oddly well hung road.\n") 
    outside['adjacent'] = [   (['hut', 'entrance'], 'boboRoom')
                            , (['cave', 'east'], 'cave')
                            , (['carnival','west'],'carnival') 
                            , (['road','south'],'kitchenDick') 
                          ]
    outside['actions'] = \
        {
        }

    carnival = {}
    carnival['description'] = i("You come upon a merry carnival, with tiny ponies and tents and\n"
                               "bearded ladies and shit. A wiry carnie in brightly colored\n"
                               "pantaloons with a raging but friendly-looking codpiece beckons you near him.\n"
                               "The familiar meadow near Bob's hut is off to the east.")
    carnival['adjacent'] = [(['east', 'outdoors','forest', 'outside', 'back'],'outside')]
    carnival['actions'] = \
        {  "play":     {    'none': i('Play what?')
                          , 'game': game
                         }
        ,  "talk":     {     'carnie' : talkToCarnie
                           , 'man'    : talkToCarnie
                           , 'lady'   : talkToBeardedLadies
                           , 'ladies' : talkToBeardedLadies
                           , 'none'   : i("Que?")
                       }
        }

    cave = {}
    cave['description'] = caveDescription
    cave['adjacent'] = [(['outside', 'back', 'outside', 'outdoors'], 'outside')]
    cave['actions'] = \
        {
           "talk":      {   'none': i("Talk to who?")
                          , 'man': talkToMan
                        }
        }
    cave['uses'] = \
        {    ('ball', 'man'):  i("The man bounces the ball back your way: what fun!")
           , ('monies', 'man'): i("I don't need to be bribed sonny boy.")
           , ('sword', 'man'): killMan
        }

    kitchenDick = {}
    kitchenDick['description'] = i("You are standing in the middle of a long, strong, and oddly well hung road.\n"
                                   "The road reaches to the north and to the south.")
    kitchenDick['adjacent'] = [   (['north'], 'outside')
                                , (['south'], 'kitchenDickTip')
                              ]
    kitchenDick['actions'] = \
        {
        }
    kitchenDick['uses'] = \
        {
        }

    kitchenDickTip = {}
    kitchenDickTip['description'] = kitchenDickDescrip
    kitchenDickTip['adjacent'] = [  (['north'], 'kitchenDick')
                                 ]
    kitchenDickTip['actions'] = \
        {
           "talk":      {   'none': i("Talk to who?")
                          , 'man': talkToEdwardo
                          , 'mustachioed': talkToEdwardo
                          , 'dude': talkToEdwardo
                        }
        }
    kitchenDickTip['uses'] = \
        {
               ('sword', 'man'): noDeathToEdwardo
             , ('sword', 'dude'): noDeathToEdwardo
             , ('sword', 'mustachiod'): noDeathToEdwardo
             , ('ball', 'man'): edwardoJustNeedsSomeBalls
             , ('ball', 'dude'): edwardoJustNeedsSomeBalls
             , ('ball', 'mustachiod'): edwardoJustNeedsSomeBalls

        }

    gamestate.addRoom('boboRoom', boboRoom)
    gamestate.addRoom('playpenRoom', playpenRoom)
    gamestate.addRoom('outside', outside)
    gamestate.addRoom('cave', cave)
    gamestate.addRoom('carnival', carnival)
    gamestate.addRoom('kitchenDick', kitchenDick)
    gamestate.addRoom('kitchenDickTip', kitchenDickTip)
    gamestate.addRoom('secretRoom', secretRoom)

    while True:
        currentRoom    = gamestate.currentRoom()
        currentActions = currentRoom['actions']
        currentVerbs   = currentActions.keys()
        if "enemy" not in currentRoom :
            currentRoom["enemy"] = detect_enemy()
        elif currentRoom["enemy"].defeated :
            currentRoom["enemy"] = detect_enemy()

        print
        headerBar = "----[%s]%s(%3d/%3d)--" % (
              gamestate.nameOfCurrentRoom()
            , "-" * (80 - 17 - len(gamestate.nameOfCurrentRoom()))
            , gamestate.achievmentCount(), gamestate.achievmentsPossible())
        print_color("hiyellow", headerBar)
        print
        print "While walking along, you see %s, minding its own business"%currentRoom["enemy"].name
        currentRoom['description'](currentRoom)
        print ""
        print_color('cyan', "You can do things. You can always:  %s" % ', '.join(PERSISTENT_VERBS))
        print_color('cyan', "In here you can:  %s" % ', '.join(currentVerbs))
        print '>', 
        command = raw_input()
        print
        action = parseCommand(command, currentRoom)
        if action == None:
            continue
        evaluateAction(action, currentRoom)

title()
gameLoop()
