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
        for Event in Events:
            #Check to see if the event is a keydown (Key goes form an off state to an on state)
            if Event.type == pygame.KEYDOWN:
                #scan through all interpreters
                for Interpreter in self.Interpreters:
                    #Check if the key in the event is within the interpreters outputs
                    if Event.key in Interpreter.Outputs:

                        Interpreter.Outputs[Event.key] = []
                    
            #Check to see if the event is a KeyUp event (Key goes from an on state to an off state)
            if Event.type == pygame.KEYUP:
                #Check through all interpreters
                for Interpreter in self.Interpreters:
                    #Scan through all keys in each interpreter
                        for Key in range(len(Interpreter.Inputs)):
                            #If the key matches a key in the interpreter inputs, set the key to off
                            if Event.key == Interpreter.Inputs[Key]:
                                Interpreter.Outputs[Key] = 



    #Intepreter serves as a base class for external interpreter objects. External interpreters will need to inherit
    #From this class in order to be considered by the control driver on game load.


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
    Currently: Returns a list ordered [Movement Vector, Mouse_Pos, Click_Status]
    Eventually: Returns a dict<String>:Value of vectors and booleans for various control flags
    Defualt returns an updateVector of [0,0]
    """
    #Want to replace any reliance on the ordering below with dict calls instead J.M
    #Returns in order (Movement_Vector, Mouse_Pos, Click_Status)
    def Convert_Keys(self):
        #eventual output array
        controlOut = []
        #check if a move Processing function has been added to this interpreter
        mousePos = pygame.mouse.get_pos()
        mouseClick = pygame.mouse.get_pressed()
        print(mouseClick)
        return [[0,0], mousePos, mouseClick]
       
    """
    Used to add key map pairs to the interpreter post-initializaition
    Accepts kPair: [key name, pygame key object]
    """
    #if the desired kName is in the interpreter map already, replaces it
    def Add_Key(self, kPair):
        kName = kPair[0]
        kEventName = kPair[1]
        self.Outputs[kName] = [kEventName, False]

    """
    removes a key from the interpreter by kName
    """
    #Function removing a key from the interpreter
    def Remove_Key(self, kName):
        if kName in self.Outputs:
            self.Outputs.pop(kName)

    """
    retrieves a key from this interpreter by kName
    """
    #Function for reading a keybind in the interpreter (mostly for UI and menu options for the controls)
    def Get_Key(self, kName):
        return self.Outputs[kName]

    """
    sets the key press status of a key in the interpreter
    """
    def Set_Key(self, kName, kStatus):
        if kName in self.Outputs:
            self.Outputs[kName][1] = [kStatus]

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
        
    



    


