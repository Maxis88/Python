import pygame
from pygame.locals import *

class SimpleText:
    def __init__(self, window, localisation_tuple, textValue, textColor):
        pygame.font.init()
        self.window=window
        self.loc = localisation_tuple
        self.font = pygame.font.SysFont(None, 30)
        self.textColor = textColor
        self.text = None
        self.setValue(textValue)
    
    def setValue(self, newText):
        if self.text== newText: 
            return
        
        self.text = newText
        self.textSurface = self.font.render(self.text, True, self.textColor)

    def draw(self):
        self.window.blit(self.textSurface, self.loc)
