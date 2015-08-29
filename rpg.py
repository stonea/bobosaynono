import time
from random import randint, sample

def prompt(q,opts=['y','n']) :
    resp = "nopenopenope"
    while resp not in opts :
        print q+" [%s]"%''.join(opts)
        resp = raw_input().lower()
    return resp

class Actor(object) :
    def __init__(self,name,stats) :
        self.name = name
        self.hp = stats.hp
        self.base_damage = stats.base_damage
        self.defeated = False

    def hit(self,damage) :
        self.hp -= damage
        if self.hp <= 0 :
            self.defeated = True

    def attack(self) :
        return self.base_damage+randint(0,3)

class Stats(object) :
    def __init__(self,hp,base_damage) :
        self.hp = hp
        self.base_damage = base_damage

enemies = {"the wumpus": Stats(100,15),
           "a kitty witty": Stats(150,3),
           "Chthuluh": Stats(1000000,1000000),
           "a ladybug": Stats(100,0),
           "an exploding barrel": Stats(26,1000000)
          }
enemy_odds = {"the wumpus": 5,
              "a kitty witty": 8,
              "Chthuluh": 1,
              "a ladybug": 3,
              "an exploding barrel": 3
             }
enemy_odds_list = []
for k,v in enemy_odds.items() :
    enemy_odds_list.extend([k]*v)

def detect_enemy() :
    enemy_type = sample(enemy_odds_list,1)[0]
    enemy = Actor(enemy_type,enemies[enemy_type])
    return enemy

def fight(room, noun) :

    your_stats = Stats(100,20)
    bobos_stats = Stats(25,5)

    you = Actor("you",your_stats)
    bobo = Actor("Bobo",bobos_stats)
    enemy = room["enemy"]

    if enemy.defeated :
        print "The adage 'beating %s that is already dead' comes to mind"%enemy.name
        return

    print "Ohkaaaaaaaay, you decide to attack the %s"%enemy.name

    contestants = [you,bobo]

    while not enemy.defeated :
        print "[ You HP=%d, Bobo HP=%d ] vs [ %s HP=%d ]"%(you.hp,bobo.hp,enemy.name,enemy.hp)

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
        print "%s attacks %s for %d damage"%(enemy.name,enemy_attack_whom.name,enemy_attack)
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

    if you.defeated :
        print "Whelp, guess fighting just wasn't your thing. You're dead."

    if bobo.defeated :
        print "But Bobo did not survive to sling poo another day. Poor Bobo."
    else :
        print "Since he survived somehow, Bobo dances valiantly on the corpse of the enemy!"

    print "But this is MAGIC BOBO WORLD AND EVERYTHING IS BACK AS IT WAS"

if __name__ == '__main__' :
    while True :
        fight(Stats(100,20),Stats(25,5))
