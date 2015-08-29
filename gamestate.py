_gameRooms = {}
_currentRoomName = 'boboRoom'
_inventory = {'monies':10}

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

def addRoom(name, room):
    _gameRooms[name] = room

def room(name):
    return _gameRooms[name]
