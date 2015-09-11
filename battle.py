import time, sys, art
from random import random, randint, sample
import gamestate
from util import prompt, ident

_enemies = {}
_enemy_odds_list = []

class Actor(object) :

    def __init__(self,name,actor_d) :
        self.name = name
        self.hp = actor_d.get("stats",{}).get("hp",0)
        self.base_damage = actor_d.get("stats",{}).get("base_damage",0)
        self.value = actor_d.get("stats",{}).get("value",0)
        self.location = actor_d.get("location",None)
        self.article = actor_d.get("article","")
        self.defeated = self.hp <= 0

    def hit(self,damage) :
        self.hp -= damage
        if self.hp <= 0 :
            self.defeated = True

    def attack(self) :
        return self.base_damage+randint(0,3)

    def __str__(self) :
        if self.defeated :
            return actor_d.get("dead",ident(""))()
        return actor_d.get("description",ident(""))()

def detect_enemy() :

    # enemy detected?
    enemy = None
    if random() > 0.2 :

        #print gamestate._enemies
        enemy_odds = []
        for k,v in gamestate._enemies.items() :
            #print k, v.keys(), v["appear_prob"]
            print v.get("location",ident("random"))() == "random"
            print type(v.get("location",ident("random"))())
            if v.get("location",ident("random"))() == "random" :
                print "WHAAAAAT"
                odds_vec = [k]*int(v.get("appear_prob",0)*100)
                #print odds_vec
                enemy_odds.extend(odds_vec)
        enemy_type = sample(enemy_odds,1)[0]
        enemy_d = gamestate._enemies[enemy_type]
        enemy = Actor(enemy_type,enemy_d)

    return enemy

def fight(room, noun) :
    room = gamestate.currentRoom()

    your_stats = {'name': "you", 'hp': 100, 'base_damage': 20}
    bobos_stats = {'name': "Bobo", 'hp': 25, 'base_damage': 5}

    you = Actor(your_stats)
    bobo = Actor(bobos_stats)
    enemy = room["enemy"]

    if enemy.defeated :
        print "The adage 'beating %s that is already dead' comes to mind"%enemy.name
        return

    print "Ohkaaaaaaaay, you decide to attack the %s"%enemy.name[0]
    print
    print eval("art.%s" % enemy.art[0])
    print

    contestants = [you,bobo]

    while not enemy.defeated :
        print "[ You HP=%d, Bobo HP=%d ] vs [ %s HP=%d ]"%(you.hp,bobo.hp,enemy.name[0],enemy.hp)

        you_attack = you.attack()
        print "You attack for %d damage"%you_attack
        enemy.hit(you_attack)

        if not bobo.defeated :
            bobo_attack = bobo.attack()
            print "Bobo attacks for %d damage"%bobo_attack
            enemy.hit(bobo_attack)

        if enemy.defeated :
            break

        enemy_attack = enemy.attack()
        enemy_attack_whom = sample(contestants,1)[0]
        print "%s attacks %s for %d damage"%(enemy.name[0],enemy_attack_whom.name[0],enemy_attack)
        enemy_attack_whom.hit(enemy_attack)

        if you.defeated :
            try : contestants.remove(you)
            except : pass

        if bobo.defeated :
            try : contestants.remove(bobo)
            except : pass

        if len(contestants) == 0 :
            break

        time.sleep(0.5)

    if enemy.defeated :
        print "You slew your foe!"
        if enemy.value != 0 :
            print "ERMAGERD %s dropped %d monies!!1!1!!"%(enemy.name[0],enemy.value)
            gamestate.addToInventory("monies",gamestate.inventory()['monies']+enemy.value)

    if you.defeated :
        print "Whelp, guess fighting just wasn't your thing. You're dead."

    if bobo.defeated :
        print "But Bobo did not survive to sling poo another day. Poor Bobo."
    else :
        print "Since he survived somehow, Bobo dances valiantly on the corpse of the enemy!"

    print "But this is MAGIC BOBO WORLD AND EVERYTHING IS BACK AS IT WAS"

#if __name__ == '__main__' :
#    while True :
#        fight(Stats(100,20),Stats(25,5))
