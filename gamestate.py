_gameRooms = {}
_currentRoomName = 'boboRoom'
_inventory = {'monies':10}
_suckedIt = 0


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

