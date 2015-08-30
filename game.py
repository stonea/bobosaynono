import os
import sys
import time
from random import random, randint, sample
import gamestate

from util import say

from carnival import game, talkToCarnie
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

def talkToMan(gamestate):
    if not 'sword' in gamestate.inventory():
        say ("The man tells you that it is dangerous to go alone and to take this \n"
             "You acquire the wooden sword <uplifting, yet short, acquisation tune plays>.")
        gamestate.addToInventory('sword')
    else:
        say ("The man tells you to get going.  He's old and the world is made for the young. \n"
             "He tells you that you should go kill things, but watch out for exploding barrels and \n"
             "stray HP Lovecraft beasts.")

# /////////////////////////////////////////////////////////////////////////////
# Playpen
# /////////////////////////////////////////////////////////////////////////////

def playpenDescription(room):
    print "You are in a Bobo's playpen.",
    if('ball' not in gamestate.inventory()):
        print "It's sparse, but it does have a big bouncy ball.  There is a passage to the south."
    else:
        print "It's sparse and soulless. And now ball-less.  There is a passage to the south."

def takeBall(gamestate):
    gamestate.addToInventory('ball')
    del(gamestate.room('playpenRoom')['actions']['take'])
    del(gamestate.room('playpenRoom')['actions']['bounce'])
    print "You take the ball.  The room suddenly seems less joy filled."

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
            room['uses'][(subject, objecto)]()

    if not didIt:
        print "Don't know how to do that..."

PERSISTENT_VERBS = ["go","fight","look","exit","inventory","use"]
PERSISTENT_NOUNS = ["north", "south", "west", "east"]
PERSISTENT_ACTIONS = {   "go": go
                       , "fight":fight
                       , "look":look
                       , "exit":exit
                       , "inventory":inventory
                       , 'use':use
                     }

# /////////////////////////////////////////////////////////////////////////////
# Game logic
# /////////////////////////////////////////////////////////////////////////////

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

    # Add inventory items
    legalNouns |= set(gamestate.inventoryItems())

    return legalNouns


def gameLoop():
    boboRoom = {}
    boboRoom['description'] = i("You are in a room with Bobo. There is nothing else but Bobo.\n" 
                              "There's a door behind you. There is a passage to the north.")
    boboRoom['adjacent'] = [  (['north', 'passage', 'playpen'], 'playpenRoom')
                            , (['door', 'behind', 'backwards', 'outside'], 'outside')]
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

    outside = {}
    outside['description'] = i("You are in the great oudoors. There's lots of trees and clouds\n" 
                             "and chirping birds and shit.\n" 
                             "Behind you is the entrance to Bobo's hut.\n" 
                             "You see a cave off into the distance.\n"
                             "There is a carnival off to your left.")
    outside['adjacent'] = [   (['hut', 'entrance'], 'boboRoom')
                            , (['cave'], 'cave')
                            , (['carnival','left'],'carnival') 
                          ]
    outside['actions'] = \
        {
        }

    carnival = {}
    carnival['description'] = i("You come upon a merry carnival, with tiny ponies and tents and\n"
                               "bearded ladies and shit. A wiry carnie in brightly colored\n"
                               "pantaloons with a raging but friendly-looking codpiece beckons you near him.\n")
    carnival['adjacent'] = [     (['outdoors','forest'],'outside') ]
    carnival['actions'] = \
        {  "play":     {   'none': i('Play what?')
                          , 'game': game
                         }
        ,  "talk":     {   'carnie': talkToCarnie,
                           'man'   : talkToCarnie
                       }
        }

    cave = {}
    cave['description'] = i("You are in a cave, an old man stands in the center.  His beard is long and\n" 
                          "wizardly: sophisticated yet non-intimidating.  To his left and right are two\n" 
                          "fires.  He looks like a friendly chap")
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
        }



    gamestate.addRoom('boboRoom', boboRoom)
    gamestate.addRoom('playpenRoom', playpenRoom)
    gamestate.addRoom('outside', outside)
    gamestate.addRoom('cave', cave)
    gamestate.addRoom('carnival', carnival)

    while True:
        currentRoom    = gamestate.currentRoom()
        currentActions = currentRoom['actions']
        currentVerbs   = currentActions.keys()
        if "enemy" not in currentRoom :
            currentRoom["enemy"] = detect_enemy()
        elif currentRoom["enemy"].defeated :
            currentRoom["enemy"] = detect_enemy()

        print
        print "----[%s]%s" % (gamestate.nameOfCurrentRoom(), "-" * (80 - len(gamestate.nameOfCurrentRoom())))
        print
        print "While walking along, you see %s, minding its own business"%currentRoom["enemy"].name
        currentRoom['description'](currentRoom)
        print ""
        print "You can do things. ",
        print "You can always:  %s" % ', '.join(PERSISTENT_VERBS)
        print "In here you can:  %s" % ', '.join(currentVerbs)
        print '>', 
        command = raw_input()
        print
        action = parseCommand(command, currentRoom)
        if action == None:
            continue
        evaluateAction(action, currentRoom)


gameLoop();
