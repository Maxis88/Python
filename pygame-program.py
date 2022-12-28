import pygame
from pygame.locals import *
import sys
from pathlib import Path
import os
import random
from SimpleText import *

class Ball:
    def __init__(self, window, windowWidth, windowHeight):
        self.window = window
        self.windowWidth=windowWidth
        self.windowHeight = windowHeight

        self.image =pygame.image.load('images/ball.png')
        self.ballRect = self.image.get_rect()

        self.width=self.ballRect.width
        self.height = self.ballRect.height

        self.maxWidth = windowWidth - self.width
        self.maxHeight = windowHeight - self.height
        # losowe pozycje startowe piłki
        self.x = random.randrange(0, self.maxWidth)
        self.y = random.randrange(0, self.maxHeight)

        speedlist = [-4,-3,-2,-1,1,2,3,4]
        self.xSpeed = random.choice(speedlist)
        self.ySpeed = random.choice(speedlist)
    
    def update(self, kolizja=False):
        
        if not kolizja:
            if self.x<0 or self.x>self.maxWidth:
                self.xSpeed = -self.xSpeed
            if self.y<0 or self.y>self.maxHeight:
                self.ySpeed = -self.ySpeed
        else:
            self.xSpeed = -self.xSpeed
            self.ySpeed = -self.ySpeed
        
        self.x = self.x + self.xSpeed
        self.y = self.y + self.ySpeed
            
    def draw(self):
        self.window.blit(self.image, (self.x, self.y))
    
    

# definiowanie stałych
pygame.init()
BLACK = (0,0,0)
RED = (1,0,0)
WIDTH = 640
HEIGHT = 800
FRAMES = 30
BASE_PATH = Path(__file__).resolve().parent

#bSound = pygame.mixer.Sound('sounds/boing.wav')

# inicjalizacja środowiska pygame

window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
# wczytywanie zasobów: obrazy , dźwięki itd

# inicjalizacja zmiennych
N_BALLS = 1
ball_list = []

for oBall in range(0, N_BALLS):
    oBall = Ball(window, WIDTH, HEIGHT)
    
    ball_list.append(oBall)
    
# pętla działająca w nieskończoność

while True:
    
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    for ball in ball_list:
        ball.update()          
    
    #window.fill(BLACK)
    for ball in ball_list:
        ball.draw()
    
        
    # uaktualnienie okna
    pygame.display.update()
    # niewielkie spowolnienie całości
    clock.tick(FRAMES)