#File containing code and classes for menu UI systems

import pygame
#Unlike entities or game objects, UI objects are position independant of the rest of the world as such their positions are hard coded and based off the screen resolution.
#UI objects are also
class UI_Object:
    def __init__(self,Position,Size):
        self.Position = Position
        self.Size = Size
        self.Texture = pygame.Surface(Size, pygame.SRCALPHA)
    def Update(self):
        return(self.Texture, self.Position)

#A BAckground for the UI, created and drawn by the
class Menu():
    def __init__(self, Position, Size):
        self.Size = Size
        self.Appearance = pygame.Surface(Size, pygame.SRCALPHA)
        self.Position = Position
        self.Objects = []
        self.Shown = False
        self.Text = pygame.font.Font("Arcana-Engine/Assets/Fonts/Tangerine-Regular.ttf", 40)
        self.SmallText = pygame.font.Font("Arcana-Engine/Assets/Fonts/Tangerine-Regular.ttf", 20)

    def Update(self):
        for item in range(len(self.Objects)):
            self.Objects[item].Update()
            self.Appearance.blit(self.Objects[item].Texture, self.Objects[item].Position)

        return (self.Appearance, self.Position)

#Slots are small squares in the inventory that can accept items placed on them
class Slot(UI_Object):
    def __init__(self, Position, Position_Relative, Font):
        super().__init__(Position, (32,32))
        self.Texture.fill((15,15,15,255))
        self.PositionRelative = Position_Relative
        self.Item = None
        self.Font = Font

    def Update(self):
        (RTexture, RPosition) = super().Update()
        if self.Item != None:
            (PosX) = (self.Size[0] - (self.Item.Icon.get_size())[0]) / 2
            (PosY) = (self.Size[1] - (self.Item.Icon.get_size())[1]) / 2
            RTexture.blit(self.Item.Icon, (PosX,PosY))
            Item_Count = self.Font.render(str(self.Item.Count), True, (255,255,255,255))
            Count_PositionX = (self.Size[0] - Item_Count.get_size()[0])
            Count_PositionY = (self.Size[1] - Item_Count.get_size()[1])
            RTexture.blit(Item_Count,(Count_PositionX,Count_PositionY))
        return(RTexture, RPosition)



class Image(UI_Object):
    def __init__(self,Position,Size):
        super().__init__(Position, Size)
        self.Texture.fill((128,128,128,255))
    def LoadFromImages(self, Name):
        Loaded_Image = pygame.image.load("Arcana-Engine/Assets/Artwork/" + Name + ".png")
        self.Texture = Loaded_Image

class Button(UI_Object):
    def __init__(self,Position,Size,Font,Text):
        super().__init__(Position, Size)
        Background = Image((0,0), self.Size)
        Background.LoadFromImages("Menu_Button")
        self.Texture.blit(Background.Texture, (0,0))
        Text_Surface = Font.render(Text, True, (50,50,50,255))
        Text_PositionX = (self.Size[0] - Text_Surface.get_size()[0])/2
        Text_PositionY = (self.Size[1] - Text_Surface.get_size()[1])/2
        self.Name = Text
        self.Texture.blit(Text_Surface, (Text_PositionX,Text_PositionY))

class Inventory(Menu):
    def __init__(self,Position, Size):
        super().__init__(Position,Size)
        self.Slots = []
        Background = Image((0, 0), Size)
        self.Objects.append(Background)
        self.HeldItem = None
        for Row in range(9):
            for Item_Slot in range(22):
                SLot_Pos = ((Row * 34) + 20, (Item_Slot * 34) + 20)
                Position_Relative = (SLot_Pos[0] + self.Position[0], SLot_Pos[1] + self.Position[1])
                New_Slot = Slot(SLot_Pos, Position_Relative,self.SmallText)
                self.Slots.append(New_Slot)
                self.Objects.append(New_Slot)

    def AddItem(self, Item):
        for Placement in self.Slots:
            if Placement.Item != None:
                if Placement.Item.ID == Item.ID:
                    Placement.Item.Count += Item.Count
                    return True
            else:
                Placement.Item = Item
                return True

    def HoldItem(self, Slot):
        Item_Held = self.HeldItem
        self.HeldItem = Slot.Item
        Slot.Item = Item_Held


    def Update(self, Mouse_Pos, Click_Status):
        self.Appearance = pygame.Surface(self.Size, pygame.SRCALPHA)
        super().Update()
        for InvSlot in self.Slots:
            if ((InvSlot.PositionRelative[0] < Mouse_Pos[0] < (InvSlot.PositionRelative[0] + InvSlot.Size[0])) and (InvSlot.PositionRelative[1] < Mouse_Pos[1] < (InvSlot.PositionRelative[1] + InvSlot.Size[1]))):
                InvSlot.Texture.fill((255, 255, 255, 128))
                if (Click_Status):
                    self.HoldItem(InvSlot)
            else:
                InvSlot.Texture.fill((15, 15, 15, 255))
        if(self.HeldItem != None):
            DrawPos = (Mouse_Pos[0] - self.Position[0], Mouse_Pos[1] - self.Position[1])
            self.Appearance.blit(self.HeldItem.Icon, DrawPos)

        return (self.Appearance,self.Position)

class Title(Menu):
    def __init__(self, Position, Size):
        super().__init__(Position, Size)
        #Create the Title Card
        Title_Card = Image((100,100), (300,100))
        Title_Card.LoadFromImages("Title")
        self.Objects.append(Title_Card)
        self.Buttons = []
        self.Shown = True
        self.Start_True = False
        #Create the buttons for the menu

        Start_Button = Button((100,250), (200,50), self.Text, "Begin")
        Exit_Button = Button((100,325),(200,50), self.Text, "Exit")

        self.Buttons.append(Start_Button)
        self.Buttons.append(Exit_Button)

    def Update(self, Mouse_Pos, Click_Status):
        self.Appearance = pygame.Surface(self.Size, pygame.SRCALPHA)
        super().Update()

        for Object in self.Buttons:
            if((Object.Position[0] < Mouse_Pos[0] < (Object.Position[0] + Object.Size[0])) and (Object.Position[1] < Mouse_Pos[1] < Object.Position[1] + Object.Size[1])):
                Large_Texture = pygame.transform.scale(Object.Texture, (220,55))
                self.Appearance.blit(Large_Texture, Object.Position)
                if(Click_Status):
                    if Object.Name == "Exit":
                        pygame.quit()
                    if Object.Name == "Begin":
                        self.Start_True = True
                        self.Shown = False

            else:
                self.Appearance.blit(Object.Texture, Object.Position)




