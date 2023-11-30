#File of classes and functoins for performing lighting operations in the graphics engine
import pygame
import math



def DrawPointLight(Color, Range, Falloff, Intensity, Inverted):
    #Create a circle that will overwrite the black overlay on the graphics engine lighting layer.
    Center = (Range / 2)
    Base = pygame.Surface((Range, Range), pygame.SRCALPHA)

    for Row in range(Range):
        for Pixel in range(Range):
            Distance_From_Center = math.sqrt((((Center - Pixel) * (Center - Pixel)) + ((Center - Row) * (Center - Row))))
            if(Distance_From_Center < (Range/2)):
                Average = abs(-Intensity * (((Distance_From_Center - Center)/(Falloff * (Distance_From_Center - Range)))))
            else:
                Average = 0
            if Inverted:
                Average = 255 - Average
            Base.set_at((Row, Pixel), (Color[0], Color[1], Color[2], (Average)))
    return Base




