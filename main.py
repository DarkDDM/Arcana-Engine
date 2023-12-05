#=====================================================================================
# Arcana Engine Central file
# Includes calls to various Inits, and runs main game loop
# CopyRight Jaxon Miller 2021
#========================================================================================

import pygame
import Debug
import Graphics.Graphics_Legacy
import World
import Controls
#initialize overall pygam system
pygame.init()
pygame.display.init()
pygame.font.init()
#===========================================================
#Debugging
#===========================================================
print(pygame.display.get_init())
Screen = Graphics.Graphics_Legacy.Screen_Space(800,450)
#Calling debug queue causes an importation of all functions in each file simulteaneuously ... very slow
print("Creating Graphics Engine")
Graphics_Engine = Graphics.Graphics_Legacy.GraphicsEngine(Screen)
print("Creating World Engine")
World_Engine = World.World_Engine(Graphics_Engine)
print("Creating Control Driver")
Control_Driver = Controls.Control_Driver(setupConfiguration="WASDStandard")
print("Running Debug")
print(pygame.display.get_init())
#Run debug Code if neccessary
Debug.Debug_Queue(Graphics_Engine)

#==========================================================
# Main Loop
#==========================================================
#Set running parameter until the user asks to quit
Running = True
ProfilerShow = True
clockTick = 0
Clock = pygame.time.Clock()
#Main Loop Begin
while Running:
    Clock.tick_busy_loop(60)
    clockTick += 1
    if(ProfilerShow):
        print("\r Clock Tick" + str(clockTick),end="")
    if(clockTick >= 1000):
        clockTick = 0
    #================================================================================================
    #update Controls
    ControlInputs = Control_Driver.Update()
    World_Engine.Update(controlsIN = ControlInputs)
    Graphics_Engine.Update()
    pygame.display.flip()
#when Mainloop is broken, the game quits
pygame.quit()

