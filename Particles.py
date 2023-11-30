#File containing data for creating and updating various tyoes of particles and effects in the graphics engine effects layer
import copy
import pygame
import random
import Entities
import math

#returns a pygame surface that is a small selection of randomy generated pixels, resembling a small dust mote
#The pixels are generated black and white with varying transparencies
def Particle_Mote():
    Surface =  pygame.Surface((5,5), pygame.SRCALPHA)

    for Row in range(8):
        for Pixel in range(8):
            chance = random.randint(0,10)
            if chance > 7:
                Greyscale_Value = random.randint(100,255)
                Alpha_Value = random.randint(150, 255)

                Surface.set_at((Row, Pixel), (Greyscale_Value, Greyscale_Value, Greyscale_Value, Alpha_Value))
    return Surface


#========================================================================================================================================================================================================
#========================================================================================================================================================================================================
class Effect(Entities.Entity):
    def __init__(self, Position, Name, Texture):
        super().__init__(Position, Name)
        self.Texture = Texture

    def Update(self):
        return(self.Position, self.Texture)

class Particle(Effect):
    def __init__(self,Position, Name, Texture):
        super().__init__(Position,Name, Texture)
        self.Speed = 5
        self.AI = Particle_Basic(self)

    def Update(self):
        Update_Vector = self.AI.Update()
        center = [self.Position[0], self.Position[1]]
        Update_Vector = (Update_Vector[0] + center[0], Update_Vector[1] + center[1])
        Vector_Polarized = Entities.VectorLine(center, Update_Vector)
        X = Vector_Polarized[0] * self.Speed * math.cos(Vector_Polarized[1])
        Y = Vector_Polarized[0] * self.Speed * math.sin(Vector_Polarized[1])
        self.MovementVector = Entities.Line((center[0], center[1]),(X + center[0], Y + center[1]))
        self.Position = self.MovementVector.End
        Chance = random.randint(0,100)
        if Chance > 85:
            self.Kill()
        return self.Texture, self.Position

class Mote(Particle):
    def __init__(self, Position, Name, Color):
        Texture = Particle_Mote()
        super().__init__(Position, Name, Texture)
        #Graphics engine checks this bool to see if lighting updates are required.
        self.Lit = True
        #Graphics engine will access this list and draw all contained light objects onto the lighting layer
        self.Lights = []
        self.Lights.append(Entities.PointLight((255,255,255,255), 50, 255, 0.7, True))
        self.Lights.append(Entities.PointLight(Color, 50, 150, 1.2, False))

    #Neccessary function to be called before adding this particle to the update queue
    def SetPosition(self, Position):
        self.Position = Position

    #This particle's update function returns its texture and position. Note this does not include the update info for the lighting.
    def Update(self):
        super().Update()
        return self.Texture, self.Position


class Particle_Basic:
    def __init__(self,Anchor):
        self.Anchor = Anchor
    def Update(self):
        X = random.randint(0,10) - 5
        Y = random.randint(0,10) - 5
        Vector = (X,Y)
        return Vector
