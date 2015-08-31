import sys
import os
import time
import gamestate
from random import random, sample
from util import say

from rpg import prompt

def talkToCarnie(room) :
    say ("\"Care to test your luck and your skill at a game that tests your luck\n"
           "and skill?\" he says, \"For indeed the two go hand in hand.\"")

def talkToBeardedLadies(room):
    print "I a gruff voice the lady says:"
    say ('"Nice to meet you."')

def game(gamestate) :
    if 'monies' not in gamestate.inventory() or gamestate.inventory()['monies'] == 0 :
        print ("\"But alas, my dear fellow, why you po. Ain' got none o dat GREEN \n"
               "na'mean? Ya'll know ain' nobady can play if ya ain' got dem monies!\" \n"
               "The logic of the man's words slowly penetrate your mind, and you realize \n"
               "this is not the time for arguing. \n"
               "\"Get yo ass out theya and kill you some kitty witties o some shit.\"\n"
               "You forthwith head out to kill some kitty witties or some shit.")
        return {}
    else:
        bet_amount = 0
        monies = gamestate.inventory()['monies']
        while bet_amount < 1 or bet_amount > monies :
            print ("\"Ay, how many of your %d pretty farthings wish thee to bet?\" [max %d]"%(monies,monies))
            try : bet_amount = int(raw_input())
            except KeyboardInterrupt as e :
                raise e
            except :
                print ("\"An integer, Dumas.\"")
        print("\"A bold bet, %d. Now let's see the mettle of your kettle!\""%bet_amount)

    skill = game_of_skill()
    skill['bet_amount'] = bet_amount
    chance = game_of_chance(skill)

    gamestate.markAchieved('playCarnival')

def game_of_skill() :
    wrds = ("\"First the test of skill. I will give you five words and you must give them back \n"
           "to me in reverse order! The words will come and go quickly, so be sharp!. Get ready.")
    print wrds,
    sys.stdout.flush()
    time.sleep(1)
    print ".",
    sys.stdout.flush()
    time.sleep(1)
    print ".\"",
    sys.stdout.flush()
    time.sleep(3)
    os.system("clear")

    wrds = wrds.replace('.','').replace('!','').replace(',','').replace('"','').lower().split()

    skill_wrds = sample(wrds,5)

    for wrd in skill_wrds :
        print
        print wrd.ljust(5)
        time.sleep(0.5)
        os.system("clear")

    print ("\"Ah ha! Now what were those words, in reverse order? Be sure ye be using the \n"
           "space delimitation, and ye olde return key only after you've typed them all!\"")
    resp = raw_input().split()
    resp.reverse()

    which_right = [_i==_j for _i,_j in zip(resp,skill_wrds)]
    num_right = sum(which_right)
    skill_resp = {'num_right':num_right}
    if num_right == len(skill_wrds) :
        print ("\"Excellent work, your skills are keen and honed. Now you will have much better \n"
               "odds at the next step! The GAME OF CHANCE!\"")
    elif num_right > 0 :
        print ("\"Well, you got some right, %d to be precise, so that will help your odds a bit later \n"
               "but if I'm being totally honest with you, Diane, it won't help much.\""%num_right)
    else :
        print ("\"Nope, not a sausage. Every word wrong. Good luck. You're gonna need it.\"")

    time.sleep(5)
    return skill_resp

def game_of_chance(skill) :

    game_width = 31
    game_height = 25
    board = [['.' for _ in range(game_width)] for __ in range(game_height)]
    bins = ['| 10x |  2x |  0x |  2x | 10x |',
            '-------------------------------']
    start_col = game_width/2 - skill['num_right']*3
    curr_col = start_col

    board[0][start_col] = 'o'

    for i in range(1,game_height) :
        os.system("clear")
        move = sample([-1,0,1],1)[0]
        trace_char = '|'
        if move == -1 :
            trace_char = '/'
        elif move == 1 :
            trace_char = '\\'
        board[i-1][curr_col] = trace_char
        curr_col = max(0,min(curr_col+move,game_width))
        board[i][curr_col] = 'o'

        print '\n'.join(''.join(_) for _ in board)
        print '\n'.join(bins)
        time.sleep(0.2)

    final_bin = curr_col/6
    payout = [10,2,0,2,10][final_bin]
    if payout == 10 :
        print("\"Brilliant! The maximum payout indeed! Here are your hard earned lucky coins \n"
              "good sir. Spend them all but naught in the same place! Adieu!\"")
    elif payout == 2 :
        print("\"Not bad, not bad. As they say, two winks are as good as a nod to a blind bat. \n"
              "Spend them all but naught in the same place! Adieu!\"")
    elif payout == 0 :
        print("\"Alas poor victim of cruel vagary, you won naught but a sense of loss and regret. \n"
              "Hone your skills, polish your mind, and return again!\"")
    gamestate.inventory()['monies'] += -skill['bet_amount']+payout*skill['bet_amount']

if __name__ == '__main__' :
    while True :
        resp = prompt("Care to play a game of chahnce?",'yn')
        if resp == 'y' : game_of_chance()
        else : break
