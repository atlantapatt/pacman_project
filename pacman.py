#!/usr/bin/env python
import os
os.environ['SDL_AUDIODRIVER'] = 'dsp'

from board import boards
import pygame

print('start game')
pygame.init()



WIDTH = 900
HEIGHT = 950
screen = pygame.display.set_mode([WIDTH,HEIGHT])
timer = pygame.time.Clock()
fps = 60
level = boards
# font = pygame.font.Font('freesansbold.ttf', 20)

def draw_boad(lvl):
    num1 = ((HEIGHT -  50) // 32)
    num2 = (WIDTH // 30)
    for i in range(len(lvl)):
        for j in range(len(lvl[i])):
            pass

run = True

if run == True:
    print('game is running')

while run:
    timer.tick(fps)
    screen.fill('black')
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print('quitting game')
            run = False

    pygame.display.flip()
pygame.quit()
