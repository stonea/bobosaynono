from random import random, randint, sample

VERBS = ["smirk", "talk"]
MISSING_NOUN = {   "smirk": "Smirk at who?"
                 , "talk": "Talk to who?"}


def parseCommand(command):
    tokens = command.split(' ')
    if len(tokens) == 0:
        return None
    if len(tokens) == 1:
        verb = tokens[0]
        if verb in MISSING_NOUN.keys():
            print MISSING_NOUN[verb]
        return None
    return (tokens[0], tokens[1])

def performAction(action):
    (verb, noun) = action
    if verb == 'smirk' and noun == 'bobo':
        print "Bobo smirks back at you."
    elif verb == 'talk' and noun == 'bobo':
        talkToBobo()

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
        print "You can <verb> <noun>.  Valid verbs include: %s" % ', '.join(VERBS)
        print '>', 
        command = raw_input()
        print
        r = parseCommand(command)
        if r == None:
            continue
        performAction(r)
        


gameLoop();

