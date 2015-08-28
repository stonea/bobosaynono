from random import random

boboStates = ['no', 'yes']
boboResponses = ['Bobo says %s%s' % (x,x) for x in boboStates]

def randInt(max):
    return (int)(random() * (max+1))

while True:
    print "What would you like to say to Bobo?"
    question = raw_input()
    print boboResponses[randInt(len(boboResponses)-1)]
