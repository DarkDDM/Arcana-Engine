import Graphics.Texture
import Brushes
import pygame
import Controls
#Pseudo Function for picking apart different game elements... Place individual constructions or functions from any class or file in the code to test here
#Debug must be enebaled in order for this quee to be called
def Debug_Queue(Graphics_Engine = None, World_Engine = None):
    controlDriveTest = Controls.Control_Driver()
    testInterpreter = Controls.Interpreter([])
    controlDriveTest.Add_Interpreter(testInterpreter)
    Clock = pygame.time.Clock()
    while True:
        Clock.tick_busy_loop(60)
        controlDriveTest.Update()
        controlOut = controlDriveTest.Convert_Keys()
        print("\rMoveVector|(" + str(controlOut[0]) + ")|MousePos(" + str(controlOut[1]) + ")|mouseClick(" + str(controlOut[2]) + ")", end="\r")
    return True