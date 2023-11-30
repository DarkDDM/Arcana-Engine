#The entitites file contains classes for all mobile objects in the game such as enemeies, spells, and the player

import math
import AIs
import pygame
import random
import Lighting

#Base_Entitiy Class for creating and manipulating dynamic AI controlled objects
#========================================================================================================================================================================================================
class Entity:
    def __init__(self,Position,Name):
        #All entities unanimously have a position
        self.Position = Position
        #All entities have a unique name used for tagging and indentification
        self.Name = Name
        #If the killed flag is true, this entity will be removed from the update cycle on the next iteration
        self.Killed = False
        #A boolean flag to the graphics engine determining whether the object is lit or not
        self.Lit = False

    def Kill(self):
        self.Killed = True
#========================================================================================================================================================================================================
#========================================================================================================================================================================================================
class Basic(Entity):
    def __init__(self, Position, Name, Sprite):
        super().__init__(Position, Name)
        self.Sprite = Sprite
        self.Sprite.Anchor = self
        self.Sprite.PlayAnimation(self.Sprite.Name + "_Idle")
        self.Hitbox = pygame.Rect((0, 0), self.Sprite.Size)
        self.Health = 100
        self.Speed = 10
        self.Damage = 0

    # calculate positional change required based on factors such as speed in the player and the inputs checked with the player controller or if
    # specified with an extranl force vector, note it is possible for entities to be updated multiple times based on different processing sections
    # This includes Controller Changes, World Shifts, Attacks, and Enviornemnt forces
    def Update(self, Update_Vector = (0,0)):
        if self.Health <= 0:
            self.Kill()
        else:
            U_X = Update_Vector[0]
            U_Y = Update_Vector[1]
            # sprite controls for the entity, determining which sprite animation to play based on the controller inputs
            # Left and right take pritority over up and down
            if (U_X == 0):
                if (U_Y == -1):
                    self.Sprite.PlayAnimation(self.Sprite.Name + "_Right")
                if (U_Y == 1):
                    self.Sprite.PlayAnimation(self.Sprite.Name + "_Left")
            if (U_X == -1):
                self.Sprite.PlayAnimation(self.Sprite.Name + "_Left")
            if (U_X == 1):
                self.Sprite.PlayAnimation(self.Sprite.Name + "_Right")
            if (U_X == 0 and U_Y == 0):
                if (self.Attacking == True):
                    self.Sprite.PlayAnimation(self.Sprite.Name + "_Attack")
                else:
                    self.Sprite.PlayAnimation(self.Sprite.Name + "_Idle")

            center = [self.Position[0], self.Position[1]]
            self.MovementVector = Line((center[0], center[1]),(self.Speed * U_X + center[0], -self.Speed * U_Y + center[1]))
            self.Hitbox.update(self.Position, self.Hitbox.size)




class Independent(Basic):
    def __init__(self, Position, Name, Sprite, Drops):
        super().__init__(Position,Name, Sprite)
        # Basic
        self.Droptable = Drops

#========================================================================================================================================================================================================
class Animate(Independent):
    def __init__(self, Position, Name, Sprite, Drops):
        super().__init__(Position, Name, Sprite, Drops)
        #Animate
        self.MovementVector = Line((0,0),(0,0))
        # Animate
        self.AI = None
        # Animate
        self.AttackSpeed = 120
        # Animate
        self.Attacking = False

#========================================================================================================================================================================================================
#an object that represents and stores information about the main player character
class Player(Animate):
    #takes a position on screen and a sprite created by the graphics engine
    def __init__(self, Position, Sprite, Inventory):
        super().__init__(Position, "Player", Sprite, None)
        self.Speed = 5
        self.Health = 100
        self.Inventory = Inventory
        self.Lit = True
        self.Lights = []
        self.Lights.append(Light((255,255,255,255), 100, 255, 0.7, True))
    def AddItem(self, Item):
        self.Inventory.AddItem(Item)

#========================================================================================================================================================================================================
#This is a basic enemy AI that will follow the player around
class Enemy(Animate):
    def __init__(self,Position, Name, Sprite, Drops):
        super().__init__(Position,Name, Sprite, Drops)
        self.AI = AIs.Enemy_Basic(self)
        self.Speed = 1

    def Update(self):
        # Get the distance to the player
        Player_Dist_X = abs(self.Position[0] - 500)
        Player_Dist_Y = abs(self.Position[1] - 500)
        Player_Dist = math.sqrt((Player_Dist_X * Player_Dist_X) + (Player_Dist_Y * Player_Dist_Y))
        Update_Vector = self.AI.Update(Player_Dist)

        if(Player_Dist < 50):
            self.Attacking = True
        super().Update(Update_Vector)

    def Kill(self):
        super().Kill()
        Drops = []
        for Object in self.DropTable:
            Chance = random.randint(0,100)
            if Chance < Object[1]:
                Drops.append(Object[0])
        self.Loot = Drops

class Dependent(Basic):
    def __init__(self, Position, Name, Sprite, Owner):
        super().__init__(Position, Name, Sprite)
        self.Owner = Owner

#========================================================================================================================================================================================================
#A moving projectile that fires from the players position and quickly moves in a direction.
class Projectile(Dependent):
    def __init__(self,Position,Name,Direction,Sprite, Owner):
        super().__init__(Position,Name,Sprite, Owner)
        self.speed = 1
        self.Range = 300
        self.Damage = 5
        (Dir_Magnitude, Dir_Angle) = VectorLine(Position, Direction)
        X = (self.speed * Dir_Magnitude) * math.cos(Dir_Angle)
        Y = (self.speed * Dir_Magnitude) * math.sin(Dir_Angle)

        self.AI = AIs.Projectile_Basic(self,(X,Y))

    def Update(self):
        self.Range -= self.Speed
        if self.Range <= 0:
            self.Kill()

        Update_Vector = self.AI.Update()
        super().Update(Update_Vector)



class Item:
    def __init__(self, Position, ID, Icon, Tooltip, Name, count):
        self.Position = Position
        self.ID = ID
        self.Icon = Icon
        self.Tooltip = Tooltip
        self.Name = Name
        self.Count = count
        self.Hitbox = pygame.Rect((0,0), self.Icon.get_size())

    def Update(self):
        self.Hitbox.update(self.Position, self.Hitbox.size)
        return(self.Icon, self.Position)

#Classes for defining Light entities
class Light(Entity):
    def __init__(self, Color, Range, Intensity, Falloff, Inverted):
        self.Color = Color
        self. Range = Range
        self. Intensity = Intensity
        self.Falloff = Falloff
        self.Texture = None
        self.Inverted = Inverted

    #Theoretically, no particle will ever update before it has been anchored to another object in the game, this means the update function can return None if there is no anchor.
    def Update(self):
        return self.Texture


class PointLight(Light):
    def __init__(self, Color, Range, Intensity, Falloff, Inverted):
        super().__init__(Color, Range, Intensity, Falloff, Inverted)
        self.Texture = Lighting.DrawPointLight(self.Color, self.Range, self.Falloff, self.Intensity, self.Inverted)



#This is a useful class for use in most entities Movement vectors, can check for collisions with other line objects.
class Line:
    #Line Constructor meant to be used with either the entity movement vector system, or to be created by two points.

    def __init__(self, Start_Pos, End_Pos):
        self.Start = Start_Pos
        self.End = End_Pos
    #Given a secon line other than this one, this function checks for a boolean value showing whether this line intesects with another one.
    #This follows directly the wikipedia article on line-line intersection
    def CheckCollision(self, comparer):
        X1 = self.Start[0]
        Y1 = self.Start[1]
        X2 = self.End[0]
        Y2 = self.End[1]
        X3 = comparer.Start[0]
        Y3 = comparer.Start[1]
        X4 = comparer.End[0]
        Y4 = comparer.End[1]


        Den = ((X1 - X2) * (Y3 - Y4) - (Y1 - Y2)*(X3 - X4))

        if(Den != 0):
            T = ((((X1 - X3)*(Y3 - Y4)) - ((Y1 - Y3)*(X3 - X4))) / Den)
            U = ((((X2 - X1)*(Y1 - Y3)) - ((Y2 - Y1)*(X1 - X3))) / Den)
            if (0.0 <= T <= 1.0) and (0.0 <= U <= 1.0):

                return True
            else:
                return False

        else:
            return False
        #This common algorithm can be used to determine the existence of any intersections between lines, by the values of T and U

    #A slightly slower function for converting a pygame rectangle int a list of lines, and checking for collision between them, and this line.
    def CheckRectCollision(self, Rect):
        L1 = Line(Rect.topleft, Rect.topright)
        if self.CheckCollision(L1):
            return True
        else:
            L1 = Line(Rect.topright, Rect.bottomright)
            if self.CheckCollision(L1):
                return True
            else:
                L1 = Line(Rect.bottomright, Rect.bottomleft)
                if self.CheckCollision(L1):
                    return True
                else:
                    L1 = Line(Rect.bottomleft, Rect.topleft)
                    if self.CheckCollision(L1):
                        return True
                    else:
                        return False



    def SetPoints(self, Startpoint, Endpoint):
        self.Start = Startpoint
        self.End = Endpoint




#An upgrade to the 8 direction vector currently present this is a function for taking 2 points and generating a 
def VectorLine(Point1, Point2):
    X = Point2[0] - Point1[0]
    Y = Point2[1] - Point1[1]

    Base_Angle = math.atan(abs(Y)/(abs(X) + 1))

    if(X < 0):
        Base_Angle = math.pi - Base_Angle
    if(Y > 0):
        Base_Angle = -Base_Angle

    if(X == Y == 0):
        return (0, Base_Angle)
    else:
        return(1, Base_Angle)





