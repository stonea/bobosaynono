import time, sys, art
from random import random, randint, sample
import gamestate
from util import prompt, ident

_enemies = {}
_enemy_odds_list = []
_enemy_defaults = {
  "location": None
, "hp": 0
, "base_damage": 0
, "value": 0
, "article": ""
, "art": ident("UNKNOWN")
, "appear_prob": 0
, "dead": "Whatever it is, it's dead."
}

class Actor(object) :

    def __init__(self,name,actor_d) :
        self.name = name
        for k,v in _enemy_defaults.items() :
            setattr(self,k,actor_d.get(k,v))

        self.art = eval("art.%s"%self.art())
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

        enemy_odds = []
        for k,v in gamestate._enemies.items() :
            #print k, v.keys(), v["appear_prob"]
            if v.get("location",ident("random"))() == "random" :
                odds_vec = [k]*int(v.get("appear_prob",0)*100)
                enemy_odds.extend(odds_vec)
        enemy_type = sample(enemy_odds,1)[0]
        enemy_d = gamestate._enemies[enemy_type]
        enemy = Actor(enemy_type,enemy_d)

    return enemy

def fight(room, noun) :
    room = gamestate.currentRoom()

    if "enemy" not in room :
      print ("You brandish a weapon of your choosing, and with a flourish of"
            "decidedly expert skill, you flail pointlessly in the air. You"
            "have no doubt been harshly judged by the denizens of your locale.")
      return

    your_stats = {'name': "you", 'hp': 100, 'base_damage': 20}
    bobos_stats = {'name': "Bobo", 'hp': 25, 'base_damage': 5}

    you = Actor("you",your_stats)
    bobo = Actor("Bobo",bobos_stats)
    enemy = room["enemy"]

    if enemy.defeated :
        print "The adage 'beating %s %s that is already dead' comes to mind"%(enemy.article(),enemy.name)
        return

    print "Ohkaaaaaaaay, you decide to attack the %s"%enemy.name
    print
    print enemy.art
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

def takeBeastOrb(gamestate):
    room = gamestate.currentRoom()
    gamestate.addToInventory('beast orb')
    del(gamestate.room('boboHut')['actions']['take']['beast orb'])
    print "You take the beast orb.  It growls softly and warmly in your robes."

def beastOrb(gamestate) :
  ce = gamestate.numEnemies()
  if ce["alive"] == 0 :
    print "The beast orb vibrates sensuously in your pants, telling you that you"
    print "have indeed destroyed all of the beasties of this land, and that again"
    print "the local townsfolk may feel safe and free from burninating. A hero you"
    print "are indeed!"
    gamestate.markAchievement('hunter')
  if ce["alive"] == ce["total"] :
    print "The beast orb sways to and fro in your robes, anxiously humming and"
    print "generally seeming uncomfortable. It communes with you to warn you"
    print "that you tread in a dangerous land indeed, rife with %d beasties"%ce["total"]
    print "roaming and causing everything from mild annoyances to pain and"
    print "destruction. Your task is cut out for you! Slay slayer!"
  else :
    print "You pull the softly glowing red orb out of your pants and gaze into it."
    print "From deep in your loins you get a sensation that tells you that you have"
    print "killed %d of the beasties in this land, but that there are %d more still"%(ce["total"]-ce["alive"],ce["alive"])
    print "to be slain. Go forth! Slay!"

#if __name__ == '__main__' :
#    while True :
#        fight(Stats(100,20),Stats(25,5))
