import random

class Enemy_Basic:
    def __init__(self, Anchor):
        self.Anchor = Anchor

    def Update(self, Player_Distance):
        Player_Position = (500,500)
        if( 32 < Player_Distance < 400):
            AI_Vector = Player_Direction(Player_Position, self.Anchor.Position)
        else:
            AI_Vector = [0,0]
        return AI_Vector
#TODO: Make Particle AI that variates Velocity To make Fun Curves
class Projectile_Basic:
    def __init__(self,Anchor, Direction):
        self.Anchor = Anchor
        self.Direction = Direction
    def Update(self):
        AI_Vector = self.Direction
        return AI_Vector


#Util Functions for these AI classes are below
def Player_Direction(Player_Pos, Current_Pos):
  Direction = [0, 0]

  X = (Player_Pos[0] - Current_Pos[0])
  if X < 0:
      X = -1
  elif X > 0:
      X = 1
  else: X = 0

  Y = (Player_Pos[1] - Current_Pos[1])
  if Y < 0:
      Y = -1
  elif Y > 0:
      Y = 1
  else: Y = 0

  Direction = [X, -Y]
  return Direction


#Function Generates and points within 2 pixelrange, makig entity jitter about at random
#Used mainly for particle effects
def RandomDirections():


    return (X,Y)
