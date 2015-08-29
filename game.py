import os
import time
from random import random, randint, sample

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

VERB_ACTIONS = {"smirk":i("Bobo smirks back at you"),
                "talk":i("Bobo is a monkey. He can talk, but he won't talk to you."),
                "play":play
               }
MISSING_NOUN = {   "smirk": i("Smirk at who?")
                 , "talk": i("Talk to who?")
                 , "play": i("With yourself?!")
               }


def parseCommand(command):
    verb = None
    for v in VERB_ACTIONS.keys() :
        if v in command.lower() :
            verb = v
            break

    if verb is None :
        return None

    if "bobo" not in command.lower() :
        print MISSING_NOUN[verb]()

    return verb


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



def gameLoop():
    while True:
        print
        print "You are in a room with Bobo. There is nothing else but Bobo."
        print "You can do things to Bobo.  Valid things include: %s" % ', '.join(VERB_ACTIONS.keys())
        print '>', 
        command = raw_input()
        print
        action = parseCommand(command)
        if action == None:
            continue
        VERB_ACTIONS[action]()


gameLoop();
