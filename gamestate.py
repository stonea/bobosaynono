from util import *
from collections import defaultdict

DEBUG=False
_gameRooms = {}
_enemies = {}
_currentRoomName = 'boboHut'
_inventory = {'monies':10}
_suckedIt = 0
_unMetAchievements = ['gotSword', 'gotDong', 'playCarnival', 'spicyRoom', 'deFuca', 'hunter']
_metAchievements = []
_achievementHints = {
      'gotSword':     "Going alone is dangerous, but perhaps a friend can be found in the caves."
    , 'playCarnival': "A game of luck, a game of chance, makes a man healthy wealthy and wise."
    , 'gotDong':      "What would make Bobo get the satisfaction he desires."
    , 'spicyRoom':    "SPICYYYYYY! You'll need a normie key and a long, strong, key."
    , 'deFuca':       "Giving a hint here would be pretty wrong-de-fuca."
    , 'hunter':       "There be beasties about."
};


_achievementsAquired = 0

def numEnemies():
    enemy_stat_d = defaultdict(int)
    for name,room in _gameRooms.items() :
        enemy = room.get("enemy")
        if enemy :
            enemy_stat_d["total"] += 1
            enemy_stat_d["alive"] += not enemy.defeated

    return enemy_stat_d

def currentRoom():
    return _gameRooms[_currentRoomName]

def nameOfCurrentRoom():
    return _currentRoomName

def moveTo(roomName):
    global _currentRoomName
    _currentRoomName = roomName

def inventory():
    global _inventory
    return _inventory

def inventoryItems():
    global _inventory
    return _inventory.keys()

def addToInventory(item, count=None):
    global _inventory
    _inventory[item] = count

def removeFromInventory(item):
    global _inventory
    if _inventory[item] is None:
        del(_inventory[item])
    else:
        _inventory[item] -= 1

def addRoom(name, room):
    _gameRooms[name] = room

def room(name):
    return _gameRooms[name]

def howManySuckedIt():
    return _suckedIt

def youSuckedIt():
    global _suckedIt
    _suckedIt = _suckedIt + 1
    if _suckedIt == 3:
        _inventory["wolfdong"] = None

def markAchieved(achievement):
    global _achievementsAquired

    assert(achievement in _metAchievements or achievement in _unMetAchievements)

    if not achievement in _metAchievements:
        print "* " * 30
        print_color('purple', "Awwww shiiiiit, you just achieved: %s.  Keep it up partna'" % achievement)
        print "* " * 30
        _achievementsAquired += 1
        _unMetAchievements.remove(achievement)
        _metAchievements.append(achievement)

def achievmentCount():
    return _achievementsAquired

def achievmentHint(achievementId):
    return _achievementHints[achievementId]

def achievmentsPossible():
    return len(_unMetAchievements) + len(_metAchievements)

def nextHint():
    if len(_unMetAchievements) == 0:
        return "You got all the hussle to you boi!!!!"

    ach = _unMetAchievements[0]
    return _achievementHints[ach]
