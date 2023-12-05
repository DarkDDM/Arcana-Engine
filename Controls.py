import pygame
from pygame import key
import math

#Control driver is a general class for handling the control inputs from the keyboard and mouse. To make the class versatile
#The actual control driver class is created with a key reader class and an interpreter class.

class Control_Driver:
    def __init__(self):
        #Create List of interpreters which is empty on initialization
        self.Interpreters = []

    def Add_Interpreter(self, Interpreter):
        self.Interpreters.append(Interpreter)

    #Get python event list, and look through the events to find keypresses matching those in
    def Update(self):
        Events = pygame.event.get()
        #Loop through all recieved events
        keyOutDict = {}
        for Event in Events:
            #Check to see if the event is a keydown (Key goes form an off state to an on state)
            #scan through all interpreters, update keystates within
            for Interpreter in self.Interpreters:
                if Event.type == pygame.KEYDOWN:
                    #Check if the key in the event is within the interpreters outputs
                    if Event.key in Interpreter.Outputs:
                        Interpreter.setKey(Event.key, True)   
                #Check to see if the event is a KeyUp event (Key goes from an on state to an off state)
                if Event.type == pygame.KEYUP:
                    #If the key matches a key in the interpreter inputs, set the key to off
                    if Event.key in Interpreter.Outputs:
                        Interpreter.setKey(Event.key, False)
            #request updated key conversions from the interpreters
        
        for Interpreter in self.Interpreters:
            #this loop will work in the order of the interpreters, expecting minimal overlapp between, but will overwrite data items from previous interpreters
            newDataItem = Interpreter.convertKeys()
            for key in newDataItem.keys():
                keyOutDict[key] = newDataItem[key]

        return keyOutDict


#TODO: Handle Mouse Pos updating
#Menu Handling
#The bridge between character interaction and this interpreter
#Interpreter utilizes dict objects that map to a string, boolean list

#Interpreter is a collection defined key variables
class Interpreter:
    """
    Constructor initializes Dict<string keyName> : [pygame.key kEvent, Boolean keyStatus]
    keyName: internal name of the key, primarily what the pairing is called in the options menu
    kEvent: internal pygame reference to key presses
    keyStatus: the status of the current key

    Arg Inputs: python list object containing touples of keyName, kEvent for initialization
                *Note Pre Init assumes all keys will begin in up state (false)
    
    The outputs dict is indexed on the names of the pygame key event objects for easier indexing later
    """

    def __init__(self, Inputs):
        self.Outputs = {}
        for keyMap in Inputs:
            kName = keyMap[0]
            kEventName = keyMap[1]
            if kName not in self.Outputs:
                self.Outputs[kName] = [kEventName, False]
            

    """
    Convert_Keys
    Returns: a dict with labeled outputs for usefull datasets in the game
    """
    #Returns in order (Movement_Vector, Mouse_Pos, Click_Status)
    #
    def convertKeys(self):
        #eventual output array
        controlOut = {}
        #check if a move Processing function has been added to this interpreter
        controlOut["mousePos"] = (0,0)
        controlOut["playerMoveVector"] = (0,0)
        controlOut["clickStatus"] = False
        return controlOut
       
    """
    Used to add key map pairs to the interpreter post-initializaition
    Accepts kPair: [key name, pygame key object]
    """
    #if the desired kName is in the interpreter map already, replaces it
    def addKey(self, kPair):
        kName = kPair[0]
        kEventName = kPair[1]
        self.Outputs[kName] = [kEventName, False]

    """
    removes a key from the interpreter by kName
    """
    #Function removing a key from the interpreter
    def removeKey(self, kName):
        if kName in self.Outputs:
            self.Outputs.pop(kName)

    """
    retrieves a key from this interpreter by kName
    """
    #Function for reading a keybind in the interpreter (mostly for UI and menu options for the controls)
    def getKey(self, kName):
        return self.Outputs[kName]

    """
    sets the key press status of a key in the interpreter
    """
    def setKey(self, kName, kStatus):
        if kName in self.Outputs:
            self.Outputs[kName][1] = kStatus

    """
    returns all keys and their statuses from 
    """
#Standard WASD input controller with mouse position and various menu keys.
class Standard_WASD(Interpreter):
    def __init__(self):
        #initialize the keys for the interpreter.
        super().__init__([
            [pygame.K_w, "Up"],
            [pygame.K_a,"Left"],
            [pygame.K_s,"Down"],
            [pygame.K_d,"Right"]
        ])

    def convertKeys(self):
        interpDataOut = {}
        #Calculate the players move vector using standard WASD control
        #here self.getKey(pyganeEvent)[1] returns the click status for given pygame keyEvent
        moveVector = [0,0]
        if self.getKey(pygame.K_w)[1]:
            moveVector[1] += 1
        if self.getKey(pygame.K_a)[1]:
            moveVector[0] -= 1
        if self.getKey(pygame.K_s)[1]:
            moveVector[1] -= 1
        if self.getKey(pygame.K_d)[1]:
            moveVector[0] += 1
        interpDataOut["playerMoveVector"] = moveVector

        #get the mouse position from pygame
        interpDataOut["mousePosition"] = pygame.mouse.get_pos()

        #get the mouse clickStatus from pygame
        interpDataOut["mouseClick"] = pygame.mouse.get_pressed(3)

        return interpDataOut
        
    



    


