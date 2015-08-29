import os
import time
from random import random, randint, sample

gameState = { 'currentRoom': 'boboRoom' }

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


def parseCommand(command, actions):
    legalVerbs = listOfAllVerbs(actions.keys())
    legalNouns = set(PERSISTENT_NOUNS)
    for verb in legalVerbs:
        if verb in actions:
            for noun in actions[verb]:
                legalNouns.add(noun)

    command = command.lower()
    verb = 'none'
    noun = 'none'
    for word in command.split():
        if word in legalVerbs:
            verb = word
        elif word in legalNouns:
            noun = word

    return (verb, noun)

def talkToBobo():
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


def printAdjacentRoomInfo(adjacencies):
    if len(adjacencies) == 0:
        print "There are no adjacent rooms"

    print "There are adjacent rooms %s" % ', '.join(dir for (dir,room) in adjacencies)

def evaluateAction(cmd, room):
    actions  = room['actions']

    (verb, noun) = cmd
    if verb in actions:
        if noun in actions[verb]:
            actions[verb][noun]()
        else:
            print "Don't know how to do that..."
    elif verb in PERSISTENT_ACTIONS:
        PERSISTENT_ACTIONS[verb](room, noun)
    else:
        print "Don't know how to do that..."

def go(room, direction):
    adjacencies = room['adjacent']
    for (expectsDir, exitsTo) in adjacencies:
        if(expectsDir == direction):
            gameState['currentRoom'] = exitsTo
            return

    print "Can't go that way."

PERSISTENT_VERBS = "go"
PERSISTENT_NOUNS = ["north", "south", "west", "east"]
PERSISTENT_ACTIONS = {"go": go}


def listOfAllVerbs(currentVerbs):
    res = currentVerbs
    res.append(PERSISTENT_VERBS)
    return res

def gameLoop():
    boboRoom = {}
    boboRoom['description'] = "You are in a room with Bobo. There is nothing else but Bobo."
    boboRoom['adjacent'] = [('north', 'playpenRoom')]
    boboRoom['actions'] = \
        {  "smirk":     {   'none': i('Smirk at who?')
                          , 'bobo': i("Bobo smirks back at you")
                        }
         , "talk":      {   'none': i("Talk to who?")
                          , 'bobo': i("Bobo is a monkey. He can talk, but he won't talk to you.")
                        }
         , "play":      {   'none': i("With yourself?!")
                          , 'bobo': play
                        }
        }

    playpenRoom = {}
    playpenRoom['description'] = "You are in a Bobo's playpen.  It's sparse but it does have a big bouncy ball."
    playpenRoom['adjacent'] = [['south', 'boboRoom']]
    playpenRoom['actions'] = \
        {  "bounce":     {   'none': i('Bounce what?')
                          , 'ball': i("The ball bounces: what fun!")
                        }
         , "take":      {   'none': i("Take what?")
                          , 'ball': i("You take the ball.")
                        }
        }



    rooms = {}
    rooms['boboRoom'] = boboRoom
    rooms['playpenRoom'] = playpenRoom


    while True:
        currentRoom    = rooms[gameState['currentRoom']]
        currentActions = currentRoom['actions']
        currentVerbs   = currentActions.keys()

        print
        print
        print
        print currentRoom['description']
        printAdjacentRoomInfo(currentRoom['adjacent'])
        print "You can do things.  Valid things include: %s" % ', '.join(listOfAllVerbs(currentVerbs))
        print '>', 
        command = raw_input()
        print
        action = parseCommand(command, currentActions)
        if action == None:
            continue
        evaluateAction(action, currentRoom)


gameLoop();
