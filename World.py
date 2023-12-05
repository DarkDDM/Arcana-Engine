#===========================================================================================================================================================
# This file contains classes and data for the world
#========================================================================================================================================================
import Dictionaries
import Lighting
import Entities
import math
import Controls
import pygame
import Graphics.Graphics_Legacy
import copy
import UI
import random
import Particles

class Structure:
    def __init__(self, Position, Size, Name):
        self.Position = Position

        self.Texture = pygame.Surface(Size, pygame.SRCALPHA)
        for Row in range(self.Texture.get_height()):
            for Pixel in range(self.Texture.get_width()):
                self.Texture.set_at((Row, Pixel), (0, 0, 0, 0))
        self.Size = Size
        self.Name = Name
        self.ActiveBound = []

#Defines a 64 by 64 grid of 64 by 64 squares that build the gameworld. They are loaded and unloaded in a 3x3 area with the player positioned in the
#center chunk.
class Chunk(Structure):
    def __init__(self, Position,Name, Size ,Elevation, Pallete):

        super().__init__(Position, [Size[0] * 32, Size[1] * 32], Name)

        #The class maintins two internal variables for the blocks in it, and the 2 chunks it uses as walls if it's elevation is >1
        self.Blocks = []
        self.Walls = []

        #creates a matrix of block objects based on the chunks size parameter
        for row in range(Size[0]):
            Block_Row = []
            for Item in range(Size[1]):
                Block_Position = ((row * 32), (Item * 32))
                New_Block = Graphics.Block(Block_Position, Pallete)
                New_Block.SetTexture("Stone")
                Block_Row.append(New_Block)

            self.Blocks.append(Block_Row)
        #Total shift is used later to create the proper sized surface for redrawing distorted isometric texture back on screen It is a return value from the distort function
        Total_Shift = 0
        if(Elevation > 0):
            Total_Shift = (self.Distort(math.pi/6, False))

        if(Elevation < 0):
            if(Elevation == -2):
                Total_Shift = (self.Distort(math.pi/3, True)) * Size[1]

        #Check if the elevation is >1, defining a chunk above ground level which is defined as 1
        if (Elevation > 1):
            #The chunk gets shifted 4 blocks up, or 4 * 32, which is the height of the walls
            self.Position[1] = self.Position[1] - ((Elevation) * 4 * 32)

            #Make the walls for the chunk
            Front_Wall = Chunk(Position, "WALL", [Size[0], 8], -1, Pallete)
            for Row in Front_Wall.Blocks:
                for Block in Row:
                    Block.SetTexture("Wall")
            Side_Wall = Chunk(Position, "WALL", [(Elevation * 5), Elevation * 4], -2, Pallete)
            for Row in Side_Wall.Blocks:
                for Block in Row:
                    Block.SetTexture("Wall")
                    Block.Distort(math.pi/3, True)
            #Add the walls under this chunks "Wall Members list"
            self.Walls.append(Front_Wall)
            self.Walls.append(Side_Wall)

            #Set a new Y value for this chunk's size, so the adjusted walls will be displayed
            self.Size[1] = self.Size[1] + ((Elevation) * 4 * 32)
            self.Texture = pygame.Surface(self.Size, pygame.SRCALPHA)

            #Draw the wall textures onto this one, making the chunk on single texture
            self.Texture.blit(self.Walls[0].Texture, [0, 512])
            self.Texture.blit(self.Walls[1].Texture, [Size[0] * 32, self.Size[1] - Side_Wall.Size[1]])
            for Row in self.Blocks:
                for Block in Row:
                    Block.SetTexture("Void")
                    Block.Distort(math.pi/6,False)
            #Draw bounding lines on the walls of the chunk, such that they mimic physical barriers
            Shift = Total_Shift - (Size[0] * 32)
            # Append all 4 active bounds to the Boundary lines of this chunk.
            B1 = Entities.Line((Shift,(Elevation * 3 * 32)),(Total_Shift, (Elevation * 3 * 32)))
            B2 = Entities.Line((Total_Shift,(Elevation * 3 * 32)),(Size[0] * 32,(self.Size[1])))
            B3 = Entities.Line((Size[0] * 32,(self.Size[1])),(0,self.Size[1]))
            B4 = Entities.Line((0,self.Size[1]), (Shift,(Elevation * 3 * 32)))

            Bounds = [B1, B2, B3, B4]
            #Append the boundaries to the active bounds list
            self.ActiveBound.extend(Bounds)


        #Blit all blocks from the block list onto the chunk's texture.
        for Row in range(len(self.Blocks)):
            for Block in self.Blocks[Row]:
                self.Texture.blit(Block.Texture, Block.Position)






    def Distort(self,Angle, Y_Axis):
        if(Y_Axis == False):
            self.Size[0] = self.Size[0] + (self.Size[1] / 32) * (math.tan(Angle) * 32)
            self.Texture = pygame.Surface(self.Size, pygame.SRCALPHA)
            #Distorted surface is blank, and needs to have 0 alpha its not the best solution each individual pixel, however its the best one can do
            for Row in range(self.Texture.get_height()):
                for Pixel in range(self.Texture.get_width()):
                    self.Texture.set_at((Row,Pixel), (0,0,0,0))
            #Now the base texture is a blank invisible slate, to be blitted too
            D_Shift = (32.0 * math.tan(Angle))
            for row in range(len(self.Blocks)):
                for column in range(len(self.Blocks[row])):
                    self.Blocks[row][column].Position = (self.Blocks[row][column].Position[0] + (D_Shift * (len(self.Blocks[row]) - 1 - column)), self.Blocks[row][column].Position[1])
                    self.Blocks[row][column].Distort(Angle, False)
            Total_Shift = (D_Shift * self.Size[0]/(32 * math.tan(Angle)))
        else:
            self.Size[1] = self.Size[1] + ((self.Size[0]) * math.tan(Angle) + 32)
            self.Texture = pygame.Surface(self.Size, pygame.SRCALPHA)
            # Distorted surface is blank, and needs to have 0 alpha its not the best solution each individual pixel, however its the best one can do
            for Row in range(self.Texture.get_height()):
                for Pixel in range(self.Texture.get_width()):
                    self.Texture.set_at((Row, Pixel), (0, 0, 0, 0))
            D_Shift = (32.0 * math.tan(Angle))
            for row in range(len(self.Blocks)):
                for column in range(len(self.Blocks[row])):
                    self.Blocks[row][column].Position = (self.Blocks[row][column].Position[0],self.Blocks[row][column].Position[1] - (D_Shift * (row)) + ((self.Size[0]) * math.tan(Angle)) - 24)
                    self.Blocks[row][column].Distort(Angle, True)

            Total_Shift = (D_Shift)

        return Total_Shift



    def Update(self):
        return (self.Texture, self.Position)

#This is an abstract class representing a set of chunks, treating them like a single structure, and setting up bounding boxes accordingly based on the hieghtmaps.
class Map:

    def __init__(self, Heightmap, Engine):
        self.Chunks = []
        self.Pallete = Graphics.Pallete()
        # Create an Array of chunks from a heightmap
        for Row in range(len(Heightmap)):
            Chunk_Row = []
            for Member in range(len(Heightmap[Row])):
                New_Chunk = Chunk([((Member * 512) - (Row * 295)), Row * 512], "Chunk", [16, 16], Heightmap[Row][Member], self.Pallete)
                Chunk_Row.append(New_Chunk)
                Engine.AddStructure(New_Chunk)
            self.Chunks.append(Chunk_Row)


#Global World Wrapper for all Objects Static And Dynamic. Each tick Items are First Updated with their Controllers, and then any world shifts are
#Layered onto the update vectors. When this is all done... Graphics calls its update Process, and all items are drawn to screen in their Required Positions
class World_Engine:
    def __init__(self,Graphics_Engine):
        #The Lists for all entities loaded into the game which are independant Ie the player, enemies, and structures
        self.Entities_Independant = []
        #The Lsit of all dependant entities in the game world, such as projectiles, which have an owner that they will not hurt
        self.Entities_Dependant = []
        #this list for all Structures (World Objects like chunks and things that do not move)
        self.Structures = []
        #List of all static world boundaries in the world, created and stored on world generation as a set of line and rect objects.
        self.Boundaries = []
        #List of items on the ground in the game
        self.Items = []
        #A lsit of Abstract versions of particles, to be updated by their agents to create effects
        self.Particles = []

        #The World Engine acts as a control for the graphics engine, commanding which entities and object get loaded and where.
        self.Graphics_Engine = Graphics_Engine

        #Create Preloaded Graphics palletes for faster computation
        self.Sprite_Pallete = Graphics.Graphics_Legacy.Sprite_Pallete("Arcana-Engine//Sprites")

        self.Item_Pallete = Graphics.Graphics_Legacy.Item_Pallete()

        self.Particle_Pallete = Graphics.Graphics_Legacy.Particle_Pallete(5)
        
        activeGraphicsSurfaceSize = Graphics_Engine.getSurfaceDim()
        Menu_Size = (activeGraphicsSurfaceSize[0] - 200, activeGraphicsSurfaceSize[1] - 200)

        self.Inventory = UI.Inventory((100, 100), Menu_Size)

        self.Title = UI.Title((0,0), (1000,1000))

        self.Player = Entities.Player((int(activeGraphicsSurfaceSize[0] / 2), int(activeGraphicsSurfaceSize[1] / 2)), self.Sprite_Pallete.GetByName("Player"), self.Inventory)
        self.Entities_Independant.append(self.Player);
        Graphics_Engine.AddBasicEntity(self.Player)

        self.Control_Drive = Controls.Control_Driver()

        self.Control_Drive.Add_Interpreter(Controls.Standard_WASD())

        self.Graphics_Engine.Menus.append(self.Inventory)

        self.Graphics_Engine.Menus.append(self.Title)

        self.Text_Large = pygame.font.Font("Arcana-Engine/Fonts/Tangerine-Regular.ttf", 40)
        self.Text_Small = ("Arcana-Engine/Fonts/Tangerine-Regular.ttf", 20)

    def Update(self):
        controlFlags = self.Control_Drive.Update()
        for entityIndep in (self.Entities_Independant):
            entityIndep.Update()

    #Add an independant entity to the world engine
    def AddIndependant(self, Independant_Entity):
        self.Entities_Independant.append(Independant_Entity)
        self.Graphics_Engine.AddSpritePack(Independant_Entity.Sprite)

    def AddDependant(self, Dependant_Entity):
        self.Entities_Dependant.append(Dependant_Entity)
        self.Graphics_Engine.AddSpritePack(Dependant_Entity.Sprite)

    def AddParticle(self, Particle):
        self.Particles.append(Particle)
        self.Graphics_Engine.AddParticle(Particle)

    def AddStructure(self, Structure):
        self.Structures.append(Structure)
        #If the structure being imported has built boundaries, add those to the set of active bounds in the world.
        if (len(Structure.ActiveBound) != 0):
            for item in range(len(Structure.ActiveBound)):
                P1X = Structure.ActiveBound[item].Start[0] + (Structure.Position[0] - 32)
                P1Y = Structure.ActiveBound[item].Start[1] + (Structure.Position[1] - 32)
                P2X = Structure.ActiveBound[item].End[0] + (Structure.Position[0] - 32)
                P2Y = Structure.ActiveBound[item].End[1] + (Structure.Position[1] - 32)

                Structure.ActiveBound[item].SetPoints((P1X, P1Y), (P2X, P2Y))
                self.Boundaries.append(Structure.ActiveBound[item])
        self.Graphics_Engine.AddStructure(Structure)
    #Creates a representation of an item in the game world
    def AddItem(self, Item):
        self.Items.append(Item)
        self.Graphics_Engine.AddStructure(Item)

    def RemoveIndependant(self, Entity):
        self.Entities_Independant.remove(Entity)
        self.Graphics_Engine.RemoveSpritePack(Entity.Sprite)

    def RemoveDependant(self, Entity):
        self.Entities_Dependant.remove(Entity)
        self.Graphics_Engine.RemoveSpritePack(Entity.Sprite)

    def RemoveStructure(self, Structure):
        self.Structures.remove(Structure)
        self.Graphics_Engine.RemoveStructure(Structure.Texture)

    def RemoveParticle(self, Particle):
        self.Particles.remove(Particle)
        self.Graphics_Engine.RemoveParticle(Particle)

    def RemoveItem(self, Item):
        self.Items.remove(Item)
        self.Graphics_Engine.RemoveStructure(Item)

    def CheckCollision(self,Entity):
        Collision = False
        if (Entity.MovementVector != None):
            for line in range(len(self.Boundaries)):
                Collision = Entity.MovementVector.CheckCollision(self.Boundaries[line])
                if (Collision == True):
                    return (True,None)

            for Comparer in self.Entities_Independant:
                if(Comparer != Entity):
                    if(Comparer.Name != "Particle"):
                        Collision = Entity.MovementVector.CheckRectCollision(Comparer.Hitbox)
                        if (Collision == True):

                            return (True,Comparer)
                    else:
                        return (False,None)

        if(Collision != True):
            return (False,None)

    def CheckForItems(self):
        for Object in self.Items:
            Collision = self.Player.Hitbox.colliderect(Object.Hitbox)
            if Collision:
                self.Player.AddItem(Object)
                self.RemoveItem(Object)

    def LoadWorld(self, Heightmap, EntitySpawns):
        self.Graphics_Engine.ScreenSurface.Screen.fill((0, 0, 0, 255))
        Text = self.Text_Large.render("Loading", True, (255, 255, 255, 255))
        Text_Size = Text.get_size()
        TextPosX = 500 - (Text_Size[0] / 2)
        TextPosY = 500 - (Text_Size[1] / 1)
        self.Graphics_Engine.ScreenSurface.Screen.blit(Text, (TextPosX, TextPosY))
        pygame.display.flip()
        Viridia = Map(Heightmap, self)

        for Item in EntitySpawns:
            Entity_Sprite = copy.copy(self.Sprite_Pallete.GetByName(Item[1]))
            New_Entity = Entities.Enemy(Item[0], Item[1], Entity_Sprite, Item[2])
            self.AddIndependant(New_Entity)
    def DropLoot(self, Position, DropList):
        for item in DropList:
            X = random.randint(-8,8)
            Y = random.randint(-8,8)
            DropPos = (Position[0] + X, Position[1] + Y)
            Id = item
            New_Item = Entities.Item(DropPos,Id,pygame.image.load(Dictionaries.Items[Id][1]), Dictionaries.Items[Id][2],Dictionaries.Items[Id][0], 1)
            self.AddItem(New_Item)


