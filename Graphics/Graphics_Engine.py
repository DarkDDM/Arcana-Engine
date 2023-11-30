#===========================================================================================================================================================
# The graphics file contains drivers for printing graphics onto the screen. This collection of driver classes will take paths and locations abd display
#objects in game
#==========================================================================================================================================================
import pygame.display
#==========================================================================================================================================================


class GraphicsEngine:
    def __init__(self, Window):
       self.ScreenSpace = Window
       self.Textures = []
       print("succesfully created Graphics engine")

    #returns touple for the size of this graphics engine screen space
    def getSurfaceDim(self):
        outSize = (self.ScreenSpace.get_width(), self.ScreenSpace.get_height())
        return outSize

    #Adds an item to the list of textures updated by the graphics engine
    def AddTexture(self,Texture):
        self.Textures.append(Texture)
        return None

    #Removes a texture from the update que for the graphics engine
    def RemoveTexture(self, Texture):
       self.Textures.remove(Texture)
       return None

    #Update function that draws all currently queued items in the graphics engine to the screen
    def Update(self):
        for item in self.Textures:
           self.ScreenSpace.blit(item.Surface, item.Position)
        
        pygame.display.flip()
















