#=======================================================================================================================
# Arcana Engine On demand texture brush library
# Copyright Jaxon Miller 2021
# Subfile for the Graphics system... used specifically for utility functions in drawing with different colors and patterns
#=======================================================================================================================

import pygame
import numpy as NP
from perlin_noise import PerlinNoise
import random
import math

#Returns Numpy array containing code for an image of 'Size' filled with the Debug Pattern
def Debug(Size):
    Size = (Size[0], Size[1], 3)
    Texture = NP.empty(Size, dtype="uint8")
    for Row in range(Size[0]):
        for Pixel in range(Size[1]):
            if (((Row % 4) < 2) and ((Pixel % 4) < 2) or ((Row % 4) > 2) and ((Pixel % 4) > 2)):
                Texture[Row][Pixel] = [255, 0, 255]
            else:
                Texture[Row][Pixel] = [0, 0, 0]

    Texture = pygame.surfarray.make_surface(Texture)

    Texture.convert_alpha()
    return Texture

def perlin(width, height, Scale, Clarity):

    Base = pygame.Surface((width, height), pygame.SRCALPHA)

    noise1 = PerlinNoise(octaves= (1 * Scale))
    noise2 = PerlinNoise(octaves= (2 * Scale))
    noise3 = PerlinNoise(octaves= (3 * Scale))
    noise4 = PerlinNoise(octaves= (4 * Scale))

    xpix, ypix = width, height
    pic = []
    for i in range(xpix):
        row = []
        for j in range(ypix):
            noise_val =  (1 * Clarity * Clarity) * noise1([i/xpix, j/ypix])
            noise_val += (2 * Clarity * Clarity) * noise2([i/xpix, j/ypix])
            noise_val += (3 * Clarity * Clarity) * noise3([i/xpix, j/ypix])
            noise_val += (4 * Clarity * Clarity) * noise4([i/xpix, j/ypix])

            row.append([noise_val, noise_val,noise_val])
            Base.set_at((i,j), (0, 0, 0, int(128/(abs(noise_val) + 1))))
        pic.append(row)

    return Base

def White_Noise(width, height, Coverage, Intensity):
    Base = pygame.Surface((width, height), pygame.SRCALPHA)
    for Row in range(height):
        for Pixel in range(width):
            Color = random.randint(0,255)
            Chance = random.randint(0,100)
            if Chance < Coverage:
                Base.set_at((Row, Pixel), (0, 0, 0, (Color)/(Intensity)))
    return Base

def Vinette(width, height, Intensity):
    Base = pygame.Surface((width, height), pygame.SRCALPHA)

    for Row in range(height):
        for Pixel in range(width):
            CenterX = width/2
            CenterY = height/2
            ValX = (math.exp(-Intensity * (Pixel - CenterX)) + math.exp(Intensity * (Pixel - CenterX))) / 2
            ValY = (math.exp(-Intensity * (Row - CenterY)) + math.exp(Intensity * (Row - CenterY))) / 2

            Average = 255 - (255 / ((ValY + ValX)/2))
            Base.set_at((Row, Pixel),(0,0,0,Average))
    return Base

def Stone(width,height):
    Grey = 240
    Base = pygame.Surface((width, height), pygame.SRCALPHA)
    Base.fill((Grey,Grey,Grey, 255))
    Perlin = perlin(width, height, 0.5, 0.5)
    White = White_Noise(width, height, 25,4)
    Vignette = Vinette(width, height, 0.05)

    Base.blit(Perlin, (0,0))
    Base.blit(White, (0,0))
    Base.blit(Vignette, (0,0))
    return Base

def Wall(width, height):
    Grey = 90
    Base = pygame.Surface((width, height), pygame.SRCALPHA)
    Base.fill((Grey, Grey, Grey, 255))
    Perlin = perlin(width, height, 0.5, 0.5)
    White = White_Noise(width, height, 25, 4)
    Vignette = Vinette(width, height, 0.05)

    Base.blit(Perlin, (0, 0))
    Base.blit(White, (0, 0))
    Base.blit(Vignette, (0, 0))
    return Base

def Void(width, height):
    Grey = 50
    Base = pygame.Surface((width, height), pygame.SRCALPHA)
    Base.fill((Grey, Grey, Grey, 255))
    Perlin = perlin(width, height, 0.5, 0.5)
    White = White_Noise(width, height, 25, 4)
    Vignette = Vinette(width, height, 0.05)

    Base.blit(Perlin, (0, 0))
    Base.blit(White, (0, 0))
    Base.blit(Vignette, (0, 0))
    return Base