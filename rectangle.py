import pygame
import random
from pygame.locals import *

RED=(255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

class Rectangle:
    def __init__(self, window):
        self.window=window
        self.width = random.choice((20,30,40))
        self.height = random.choice((20,30,40))
        self.color = random.choice((RED,GREEN,BLUE))
        self.x = random.randint(0, 400)
        self.y = random.randint(0,400)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.area = self.width*self.height

    def clickedInside(self, mousepoint):
        clicked = self.rect.collidepoint(mousepoint)
        return clicked
    
    def __eq__(self, oOtherRectangle):
        if not isinstance(oOtherRectangle, Rectangle):
            raise TypeError("Drugi obiekt nie jest typu rectangle")
        if self.area == oOtherRectangle.area:
            return True
        else:
            return False
    def __lt__(self, oOtherRectangle):
        if not isinstance(oOtherRectangle, Rectangle):
            raise TypeError("Drugi obiekt nie jest typu rectangle")
        if self.area < oOtherRectangle.area:
            return True
        else:
            return False
    def __gt__(self, oOtherRectangle):
        if not isinstance(oOtherRectangle, Rectangle):
            raise TypeError('Drugi obiekt nie jest typu rectangle')
        if self.area > oOtherRectangle.area:
            return True
        else:
            return False
    def getArea(self):
        return self.area
    def draw(self):
        pygame.draw.rect(self.window, self.color, (self.x, self.y, self.width, self.height))