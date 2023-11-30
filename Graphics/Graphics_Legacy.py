#===========================================================================================================================================================
# The graphics file contains drivers for printing graphics onto the screen. This collection of driver classes will take paths and locations abd display
#objects in game
#==========================================================================================================================================================
import pygame
import Dictionaries
import Brushes
import math
import os
import random
import Particles
from PIL import Image
import numpy as NP
from numpy import asarray
#==========================================================================================================================================================
#class Graphics_Object
#Defines a superclass that represents all grpahical objects used by the graphics engine
#All graphics object have a texture, stored in a numpy array, and a position stored as a touple
class Graphics_Object:
    def __init__(self, Position, Texture):
        self.Texture = Texture
        self.Position = Position

    def Update(self):
        return (self.Texture, self.Position)

#Arcana Engine Graphics Model
#Copyright Jaxon Miller 2021
#Class definition and API for texture objects in the graphics engine
import Brushes

class Texture(Graphics_Object):
    #Texture items defined by a surface and a position
    def __init__(self, Surface = None, Position = (0,0)):
        self.Surface = Surface
        self.Position = Position
        print("==Debug== Created Texture Object")
        super.__init__(Surface, Position)
    #set the position of this texture
    def SetPos(self, New_Position):
        self.Position = New_Position
    #returns the position of this texture
    def GetPos(self):
        return self.Position
    #replaces the surface of this texture object
    #input surface is a pygame surface object
    def SetSurface(self, newSurface):
        self.Surface = newSurface

    #returns the pygame surface object representing the actual texture data in this object
    def GetSurface(self):
        return self.Surface

    #overlays an image on top of this texture's surface object
    def Stain(self, New_Surface = None):
        self.Surface.blit(New_Surface)

    #Debug printout for this class
    def __str__(self):
        output = "Arcana Engine Texture Class \n"
        output += "Texture: " + str(self.Surface) + "\n"
        output += "Position: " + str(self.Position) + "\n"
        return output
    
    



#sprite is a specific texture pertaining to entities. Sprites support animations by defining a folder containing sets of images.
#sprite animations are defined with specifically named images, that are placed ona long vertical chain. Each frame of the animation
#takes up another cube continueing directly below the frame preovious.

#Name is the name of the sprite object, must match up with the corresponding source file in the game assets path
#Source is the path to this specific Sprites images
#Size, the size of the sprite, sprite images will be a perfect square of ('Size'x'Size')
#Anchor, all sprites must be attached to some sort of entity in the map, where they recive thier positional and control Data.
class Sprite:
    def __init__(self, Name, Source, Anchor, Speed):
        #sprite entity mainfile is set
        self.Source = Source
        self.Name = Name
        self.Anims = []
        self.Anchor = Anchor
        self.Speed = Speed
        self.Load_All()

        for Item in range(len(self.Anims)):
            if(self.Anims[Item].Name == (self.Name + "_Idle")):
                self.Active = self.Anims[Item]
            else:
                self.Active = self.Anims[0]



    #Creates a set of Graphics_Objects to serve as each frame of each animation in the sprite
    class Sprite_Frame():
        def __init__(self,Size,Texture):
            #This initial creation of the debug texture is so that the sprite will appear as a vibrant pink to show an error in texture assignmnet
            self.Texture = pygame.Surface(Size, pygame.SRCALPHA)
            #Noe the texture gets reset to the texture used in the constructor.
            self.Texture.blit(Texture,(0,0))


    #Creates a list of Sprite Frames, indexed internally, so that the current frame can be accessed and stored
    #It recieves its frames from the Sprite mainclass, this is just an organization bundle of the individual frames to be called and iterated through
    class Animation:
        def __init__(self, Name, Frames, Looping, Speed):
            #the internal list of frames to be accessed
            self.Frames = Frames
            #The name of the animation, which will allow it to be called from the sprite superclass
            self.Name = Name
            #An internal index storing the current frame the animation will play
            self.CurrentFrame = 0
            #A flag for telling the animation to repeat after playing all of its frames. This will loop until a new animation is selected in the
            self.Looping = Looping
            #Terminate flag can be set internally or eternally, which will automatically remove this animation from the graphics queue
            self.Terminate = False
            #The name of the currently playing sprite if any
            self.Active = None
            #The speed at which the animation plays
            self.Speed = Speed

        def Update(self):
            FrameSelector = int((self.CurrentFrame - 1) / (self.Speed))

            R_Texture = self.Frames[FrameSelector].Texture
            #Check for external invocations of this animation's terminate flag
            if self.Terminate == True:
                #If true, set the Current frame to 0, and cease playing.

                self.CurrentFrame = 0
                return R_Texture
            else:
                #Check termination status based on looping status and
                if (self.CurrentFrame) + 1 == len(self.Frames) * self.Speed:
                    if self.Looping == True:
                        self.CurrentFrame = 0
                    else:
                        self.Terminate = True

                self.CurrentFrame = self.CurrentFrame + 1
                return R_Texture



    def Load_All(self):
        Sprite_Sources = os.listdir(self.Source)
        for item in Sprite_Sources:
            self.LoadAnimation(item, True, self.Speed)


        #loads and plays an animation from the Sprites Source File (Must Match Names given in Source File)

    #Loads a single animation from the source file into the RAM memory of the sprite system. Where, Anim is the name of the sprite (Note this must match with a name given in the source file)
    #Looping is a boolean flag for setting the animation to loop repeatedly.
    def LoadAnimation(self,Anim, Looping, Speed):
            #load the sprite format image from the file path specificied in the sprite class source value
            #First path to animation is specified... note that the animations are specifically named to be findable by the sprite
            Image_Path = self.Source + "/" + Anim
            #Opens the base image as a numpy image array
            Sprite_Anim_NP = asarray(Image.open(Image_Path))
            Size_Y = len(Sprite_Anim_NP)
            Size_X = len(Sprite_Anim_NP[0])
            Sprite_Anim = pygame.Surface((Size_X, Size_Y), pygame.SRCALPHA)
            for Row in range(len(Sprite_Anim_NP)):
                for Item in range(len(Sprite_Anim_NP[Row])):
                    Color_R = (Sprite_Anim_NP[Row][Item][0])
                    Color_G = (Sprite_Anim_NP[Row][Item][1])
                    Color_B = (Sprite_Anim_NP[Row][Item][2])
                    Color_A = (Sprite_Anim_NP[Row][Item][3])
                    Sprite_Anim.set_at((Item, Row), (Color_R, Color_G, Color_B, Color_A))

            Anim_Name = (Anim.rsplit(".png", 1)[0])
            self.Size = (Sprite_Anim.get_width(),Sprite_Anim.get_width())

            if Sprite_Anim.get_height() % self.Size[1] == 0:
                Framecount = int(Sprite_Anim.get_height() / self.Size[1])


                FrameList = []

                for frame in range(Framecount):
                    BoundStart = (0, self.Size[1] * frame)
                    FrameBound = pygame.Rect(BoundStart, (self.Size[0], self.Size[1]))
                    FrameSRF =  pygame.Surface((self.Size[0], self.Size[1]), pygame.SRCALPHA)
                    FrameSRF.fill((0,0,0,0))
                    FrameSRF.blit(Sprite_Anim, (0,0), area = FrameBound)
                    Frame = self.Sprite_Frame((self.Size[0], self.Size[1]), FrameSRF)
                    FrameList.append(Frame)

                Animation = self.Animation(Anim_Name, FrameList, Looping, Speed)
                self.Anims.append(Animation)
            else:
                print("Could not load sprite: Image file is incorrect size")

#With the Sprite loaded into the graphics system, it will request a single frame from the sprite set on each tick play animation is
#A control function that will determine which frame is passed to the graphics engine. It takes an argument for which seleciton from the
#sprite pack to select frames from.
#This system will terminate any current looping animation if a new one is requested.
    def PlayAnimation(self, Anim):
        #check the currently active animation, if it is the same as the requested, continue as normal if there is a mistmatch, a change is required
        if Anim != self.Active.Name:
            #Set the active anims Terminate flag true, and update it, forcing it to close

            self.Active.Terminate = True
            self.Active.Update()
            #Change the current active animation, finding it by name in the animation list
            for Item in range(len(self.Anims)):
                if self.Anims[Item].Name == Anim:
                    #If the animation is founc in the list, that animtion will be set active, and be played by the sprite class

                    self.Active = self.Anims[Item]
                    self.Active.Terminate = False
                    #The function will exit here
                    return True
            #If the file is not found, the funciton will end here, and return an error to the console.
            print("Failed to load animation:" + str(Anim) +  "on play request, is the animation loaded?")
        return False

    #A simple function, that returns the sprite's current position, and retrieves a texture from its currently active frame
    def Update(self):
        R_Position = self.Anchor.Position
        R_Texture = self.Active.Update()
        return(R_Texture, R_Position)

#Todo set mote loading in balck and white on prelaod, Do NOT add the motes to the update queue when preloading. Load them to the particle pallete
#Todo Create instantiation methods for the mote particles, gicing them the neccessary data to be added to the update queue
class Particle_Pallete:
    #Variance in the init function determines the number of particles that are made to select from by the pallete, higher variance will take longer to laod and will require more ram
    def __init__(self, Variance):
        self.Variance = Variance
        self.Motes = []
        for Item in range(Variance):
            self.Motes.append(Particles.Mote(None, "Mote", (255,125,255,255)))


    def GetByName(self, Key):
        if Key == "Mote":
            Choice = random.randint(0,(self.Variance-1))
            Selection = copy.copy(self.Motes[Choice])
            return Selection

#for higher speed loading of entities, their sprites will be stored in this pallet object, which will load and hold sprites, and pass a copy of the sprite
class Sprite_Pallete:
    #for all files in the sprite folder, this class makes a new sprite object
    #TODO Make selectable sprite palletes, IE, have the folder specificable to make winter sprites, fire sprites, etc

    #Source Specifies the location of the sprite file
    def __init__(self, Source):
        Sprite_List = os.listdir(Source)
        self.Sprites = []
        for item in range(len(Sprite_List)):
            Path_Extended = Source + "/" + Sprite_List[item]
            NewMadeSprite = Sprite(Sprite_List[item], Path_Extended, None, 5)
            self.Sprites.append(NewMadeSprite)

    def GetByName(self, Key):
        Found_Sprite = None
        for item in range(len(self.Sprites)):
            if self.Sprites[item].Name == Key:
                Found_Sprite = self.Sprites[item]
        return Found_Sprite



#IE... system updates the animations that must be played, draw effects and textures to locations etc

#Wrapper for the Pygame Screen system that stores some crucial Data for positioning such as width and height
class Screen_Space:
    def __init__(self, height, width):
        self.Height = height
        self.Width = width
        # set up drawing window
        self.Screen = pygame.display.set_mode([self.Height, self.Width])
        pygame.display.set_caption("Arcana")
        self.Screen.fill((0, 0, 0))
    #return the height of this screenspace
    def getSize(self):
        return (self.Width, self.Height)
    #return the width of this screenspace
    def getWidth(self):
        return self.Width
    #return the height of this screenspace
    def getHeight(self):
        return self.Height
    
#a 64 by 32 set of pixels used to display textures in the chunk. Works in a similar way to voxels where thee map  is created by various squares.
class Block(Graphics_Object):
    def __init__(self,Position,Pallete):
        self.Pallete = Pallete
        super().__init__((Position), Pallete.Debug)

#TODO: Add alpha surface generation on distort.
    def Distort(self, Angle, Y_Axis):
        #Check boolean value to test for Y axis distortion selection
        if(Y_Axis == False):
            #Get value of total shift value
            DistortFactor = math.tan(Angle)
            Dpixel = int(self.Texture.get_width() * DistortFactor)
            #make a new surface that is the correct size
            D_Texture = pygame.Surface((self.Texture.get_width() + Dpixel, self.Texture.get_height()), pygame.SRCALPHA)
            #Set base of the texture to be fully blank and transparent
            for Row in range(self.Texture.get_height()):
                for Pixel in range(self.Texture.get_width()):
                    D_Texture.set_at((Pixel,Row), (0,0,0,0))
            #Iterate through the old text, and place it on the new one with a distortion
            for Row in range(self.Texture.get_height()):
                #Now dpixel scales upwards based on the row value
                Dpixel = int((self.Texture.get_height() - Row) * DistortFactor)
                for Pixel in range(self.Texture.get_width()):
                    Color_Old = self.Texture.get_at((Pixel, Row))

                    D_Texture.set_at((Pixel + Dpixel, Row), Color_Old)
            self.Texture = D_Texture
        #Process for Y-Axis distorions is exactly the same with some modified parameters, and there is no transposition at the end
        else:
            #Similar process operates on a idfferent axis for y level disortions
            DistortFactor = math.tan(Angle)
            Dpixel = int(self.Texture.get_height() * DistortFactor)
            #Make a new surface to store teture data for the distort
            D_Texture = pygame.Surface((self.Texture.get_width(), self.Texture.get_height() + Dpixel), pygame.SRCALPHA)
            #Set the distorted texture to be fully blank and transparent
            for Row in range(self.Texture.get_height()):
                for Pixel in range(self.Texture.get_width()):
                    D_Texture.set_at((Pixel, Row), (0,0,0,0))
            #Overlay the old texture with a distortion onto the new one
            for Pixel in range(self.Texture.get_width()):
                Dpixel = int(Pixel * DistortFactor)
                for Row in range(self.Texture.get_height()):
                    Color_Old = self.Texture.get_at((Pixel, Row))
                    D_Texture.set_at((Pixel, (D_Texture.get_height() - Row) - Dpixel), Color_Old)
            self.Texture = D_Texture



    #Distorts the orginal texture of this block and requests a draw to screen at its position, which is determined relative to the player
    def Update(self):
        return(self.Texture, self.Position)

    def SetTexture(self, Selection):

        if(Selection == "Stone"):
            variant = random.randint(0,(len(self.Pallete.Stones) - 1))
            self.Texture = (self.Pallete.Stones[variant])

        if (Selection == "Wall"):
            variant = random.randint(0, (len(self.Pallete.Walls) - 1))
            self.Texture = (self.Pallete.Walls[variant])
        if (Selection == "Void"):
            variant = random.randint(0, (len(self.Pallete.Voids) - 1))
            self.Texture = (self.Pallete.Voids[variant])

        if (Selection == "Debug"):
            self.Texture = (self.Pallete.Debug)

#Pallete is to drastically improve texture generation by having a set of textures ready to select.
class Pallete:
    def __init__(self):
        self.Stones = []
        for Type in range(5):
            self.Stones.append(Brushes.Stone(32, 32))

        self.Walls = []
        for Type in range(5):
            self.Walls.append(Brushes.Wall(32, 32))

        self.Voids = []
        for Type in range(5):
            self.Voids.append(Brushes.Void(32, 32))

        self.Debug = Brushes.Debug((32,32))

#Preloads the Image icons for items
class Item_Pallete:
    def __init__(self):
        self.Icons = []
        for Index in range(len(Dictionaries.Items)):
            Item_Icon = pygame.image.load(Dictionaries.Items[Index][1])
            self.Icons.append(Item_Icon)



#Base effect class, represents a graphics object that gets its texture dynamically updated based on some code
class Effect(Graphics_Object):
    #Effects have bounding boxes
    #effects have a texture
    #Unlike sprites or other objects, effect textures are dynamically updated per pixel with a variety of optional effects,
    #Or, these objects also output termintaion data to their anchor, ending the anchored entity
    def __init__(self,Texture,Position,Name):
        super().__init__((16,16),Texture,Position)

#Given 2 pygame surfaces with per pixel alphas enabled, this function will blend their colors based on those alphas. Surface A is used as the background and B is blitted with opacity
#The position argument will offset surface B when blitting
#Note this does not simply blit the values from B to A like pygame does, this uses a special version of opacity calculation to overwrite pygames blend modes
#The function will apply changes to surface A
def BlitWithOpacity(SurfaceA, SurfaceB, Position):
    X_Bound = min((SurfaceA.get_width() - Position[0]), SurfaceB.get_width())
    Y_Bound = min((SurfaceA.get_height() - Position[1]), SurfaceB.get_height())
    for Row in range(Y_Bound):
        for Column in range (X_Bound):

            Color_Base = SurfaceA.get_at((Column + Position[0], Row + Position[1]))
            Color_Over = SurfaceB.get_at((Column, Row))



            R_Combined = (Color_Over[0] * (Color_Over[3] / 255)) + (Color_Base[0] * ((255 - Color_Over[3]) / 255))
            G_Combined = (Color_Over[1] * (Color_Over[3] / 255)) + (Color_Base[1] * ((255 - Color_Over[3]) / 255))
            B_Combined = (Color_Over[2] * (Color_Over[3] / 255)) + (Color_Base[2] * ((255 - Color_Over[3]) / 255))
            A_Combined = max(Color_Base[3], Color_Over[3])
            SurfaceA.set_at(((Column + Position[0]),(Row + Position[1])),(R_Combined, G_Combined, B_Combined, A_Combined))

class GraphicsEngine:
    #Constructor function for the central Graphics Engine,
    #Input ScreenSpace: ScreenSurface Object
    def __init__(self,ScreenSpace):
        #The list of updates per frame items appended into this list, items are stored here as an IMAGE item from PIL and a location Tuple
        #(Image, (x,y))
        self.Updates = []
        #Items of type Animations
        self.Entities = []
        #List of Static texture objects to be laoded at a given position into the engine
        self.Textures = []
        #A list of the graphical representations of the UI menus from the world engine
        self.Menus = []
        #A list of particles to iterate through in the update queue, applied and updated on the effects layer
        self.Particles = []
        #List of light objects stored in the engine
        self.Lights = []
        #The screen surface from the display that the graphics engine draws to
        self.ScreenSurface = ScreenSpace

        #The three major drawing layers for the engine, Base, Effects, and Lighting
        #Base is used for basic textures of entities and structures
        self.Base = pygame.Surface(self.ScreenSurface.getSize(), pygame.SRCALPHA)
        #Effects is used for particles and shading
        self.Effects = pygame.Surface(self.ScreenSurface.getSize(), pygame.SRCALPHA)
        #Lighting is used for drawing in shadows after effects are calculated
        self.Lighting = pygame.Surface(self.ScreenSurface.getSize(), pygame.SRCALPHA)
    
    #returns touple for the size of this graphics engine screen space
    def getSurfaceDim(self):
        outSize = (self.ScreenSurface.getWidth(), self.ScreenSurface.getHeight())
        return outSize    
     #Adds an item to the list of textures updated by the graphics engine
    def AddTexture(self,Texture):
        self.Textures.append(Texture)
        return None

    #Removes a texture from the update que for the graphics engine
    def RemoveTexture(self, Texture):
       self.Textures.remove(Texture)
       return None
    #Function for adding an animated sprite system to the graphics engine update list
    def AddBasicEntity(self, Entity):
        self.Entities.append(Entity.Sprite)
    #Function for adding a static graphical object, such as an image, to the game engine graphics queue
    def AddStructure(self, Structure):
        self.Textures.append(Structure)
    #Function for adding a UI element to the graphics engine update queue
    def AddMenu(self, Menu):
        self.Menus.append(Menu)
    def AddParticle(self, Particle):
        self.Particles.append(Particle)
    
    #Function for removing a Sprite
    def RemoveBasicEntity(self, Sprite):
        self.SpritePacks.remove(Sprite)
    #Function for removing a structure from the the graphics queue
    def RemoveStructure(self, Structure):
        self.Textures.remove(Structure)
    #Function for removing particles from the graphics engine queue
    def RemoveParticle(self, Particle):
        self.Particles.remove(Particle)


    def Update(self):
        self.ScreenSurface.Screen.fill((0,0,0,0))
        self.Base.fill((0,0,0,0))
        self.Effects.fill((0,0,0,0))
        self.Lighting.fill((0,0,0,200))
        # The update queue for the graphics engine base Layer
        # ======================================================================================================================================================================================
        #Work through the list of static textures first, as they will take less time
        for Image in self.Textures:
            (Texture, Position) = Image.Update()
            self.Updates.append((Texture, Position))
        #Select the sprite frames to draw for all entities in the game world
        for Entity in self.Entities:
            Frame, Position = Entity.Update()
            self.Updates.append((Frame, Position))
        self.ScreenSurface.Screen.fill((255, 255, 255))

        #Once updates have been compiled draw them to the screen surface to make the frame.
        for Item in range(len(self.Updates)):
            self.Base.blit(self.Updates[Item][0], self.Updates[Item][1])
        self.Updates = []

        #If there is a UI to be show, overwrite the current frame and draw the ui over that.
        for UI in self.Menus:
            if UI.Shown == True:
                UI_Update = (UI.Appearance, UI.Position)
                self.ScreenSurface.Screen.blit(pygame.Surface.copy(UI_Update[0]), UI_Update[1])

        #Update queue for the Particle Layer
        #==============================================================================================================================================================================
        for Particle in self.Particles:
            Texture, Position = Particle.Update()
            self.Effects.blit(pygame.Surface.copy(Texture), Position)
            if Particle.Lit == True:
                for LightEffect in Particle.Lights:
                    Update = LightEffect.Update()
                    Blit_PositionX = Particle.Position[0] - (Update.get_width()/2)
                    Blit_PositionY = Particle.Position[1] - (Update.get_height()/2)
                    Blit_Position = (Blit_PositionX, Blit_PositionY)
                    if LightEffect.Inverted == True:
                        Flag = pygame.BLEND_RGBA_MIN
                    else:
                        Flag = 0
                    self.Lighting.blit(Update, Blit_Position, special_flags=Flag)




        #after creating the seperate layers, combine together utilizing relative alpha values and colors.

        #Placeholder here for the combination process
        Frame_Combined = pygame.Surface(self.ScreenSurface.Screen.get_size(), pygame.SRCALPHA)
        Frame_Combined.fill((255,255,255,255))
        Frame_Combined.blit(self.Base, (0,0))
        Frame_Combined.blit(self.Lighting,(0,0))
        Frame_Combined.blit(self.Effects,(0,0))
        self.ScreenSurface.Screen.blit(Frame_Combined,(0,0))
        pygame.display.flip()












