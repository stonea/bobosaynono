import os
import sys
import time
from random import random, randint, sample

from carnival import game
from rpg import detect_enemy, fight, prompt

gameRooms = {}
gameState = {
      'currentRoom': 'boboRoom'
    , 'inventory': {'monies':10}
}

def i(s) :
    def _(*args,**kwargs) :
        print s
    return _

def play(*args,**kwargs) :
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

def computeSetOfLegalNounsForRoom(room, legalVerbs):
    """ Yeah this function sucks """
    actions = room['actions']

    legalNouns = set(PERSISTENT_NOUNS)
    for verb in legalVerbs:
        if verb in actions:
            for noun in actions[verb]:
                legalNouns.add(noun)

    for adjacency in room['adjacent']:
        for direction in adjacency[0]:
            legalNouns.add(direction)

    return legalNouns



def parseCommand(command, room):
    actions = room['actions']
    legalVerbs = listOfAllVerbs(actions.keys())
    legalNouns = computeSetOfLegalNounsForRoom(room, legalVerbs)

    command = command.lower()
    verb = 'none'
    noun = 'none'
    for word in command.split():
        if word in legalVerbs:
            verb = word
        elif word in legalNouns:
            noun = word

    return (verb, noun)

def talkToBobo(*args,**kwargs):
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
             "gives you a flower",
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

def talkToMan(gameState):
    if not 'sword' in gameState['inventory']:
        print "The man tells you that it is dangerous to go alone and to take this"
        print "You acquire the wooden sword <uplifting, yet short, acquisation tune plays>."
        gameState['inventory']['sword'] = None
    else:
        print "The man tells you to get going.  He's old and the world is made for the young."
        print "He tells you that you should go kill things, but watch out for exploding barrels and"
        print "stray HP Lovecraft beasts."

def playpenDescription(room):
    print "You are in a Bobo's playpen.",
    if('ball' not in gameState['inventory']):
        print "It's sparse, but it does have a big bouncy ball.  There is a passage to the south."
    else:
        print "It's sparse and soulless. And now ball-less.  There is a passage to the south."

def takeBall(gameState):
    gameState['inventory']['ball'] = None
    del(gameRooms['playpenRoom']['actions']['take'])
    del(gameRooms['playpenRoom']['actions']['bounce'])
    print "You take the ball.  The room suddenly seems less joy filled."

def evaluateAction(cmd, room):
    actions  = room['actions']

    (verb, noun) = cmd
    if verb in actions:
        if noun in actions[verb]:
            actions[verb][noun](gameState)
        else:
            print "Don't know how to do that..."
    elif verb in PERSISTENT_ACTIONS:
        PERSISTENT_ACTIONS[verb](room, noun)
    else:
        print "Don't know how to do that..."

def go(room, direction):
    adjacencies = room['adjacent']
    for (expectedDirs, exitsTo) in adjacencies:
        for expectedDir in expectedDirs:
            if(expectedDir == direction):
                gameState['currentRoom'] = exitsTo
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
    inventory = gameState['inventory']
    if len(inventory) == 0:
        print "You have nothing in your inventory"
        return
    print "You have the following in your inventory:"
    for item,num in inventory.items():
        item_str = item if num is None else '%s (%d)'%(item,num)
        print "   * ", item_str




PERSISTENT_VERBS = ["go","fight","look","exit","inventory"]
PERSISTENT_NOUNS = ["north", "south", "west", "east"]
PERSISTENT_ACTIONS = {   "go": go
                       , "fight":fight
                       , "look":look
                       , "exit":exit
                       , "inventory":inventory
                     }

def listOfAllVerbs(currentVerbs):
    res = currentVerbs
    res.extend(PERSISTENT_VERBS)
    return res

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

    playpenRoom = {}
    playpenRoom['description'] = playpenDescription
    playpenRoom['adjacent'] = [(['south', 'passage'], 'boboRoom')]
    playpenRoom['actions'] = 
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
                               "bearded ladies and shit. A wiry man in brightly colored\n"
                               "pantaloons beckons you near him.\n"
                               "\"Care to test your luck and your skill at a game that tests your luck\n"
                               "and skill?\" he says, \"For indeed the two go hand in hand.\"")
    carnival['adjacent'] = [     (['outdoors','forest'],'outside') ]
    carnival['actions'] = \
        {  "play":     {   'none': i('Play what?')
                          , 'game': game
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



    gameRooms['boboRoom']    = boboRoom
    gameRooms['playpenRoom'] = playpenRoom
    gameRooms['outside']     = outside
    gameRooms['cave']        = cave
    gameRooms['carnival']    = carnival


    while True:
        currentRoom    = gameRooms[gameState['currentRoom']]
        currentActions = currentRoom['actions']
        currentVerbs   = currentActions.keys()
        if "enemy" not in currentRoom :
            currentRoom["enemy"] = detect_enemy()
        elif currentRoom["enemy"].defeated :
            currentRoom["enemy"] = detect_enemy()

        print
        print "----[%s]%s" % (gameState['currentRoom'], "-" * (80 - len(gameState['currentRoom'])))
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
