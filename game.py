from random import random, randint, sample

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

while True:
    print "What would you like to say to Bobo?"
    question = raw_input()
    print boboResponses[randint(0,len(boboResponses)-1)]

    youLikey = 'x'
    while youLikey not in 'yn' :
        print "Do you like Bobo's response? [y/n]"
        youLikey = raw_input().lower()

    print "Fine, Bobo %s"%sample(boboActivities[youLikey],1)[0]
