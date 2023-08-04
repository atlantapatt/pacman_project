#!/usr/bin/env python
import os
os.environ['SDL_AUDIODRIVER'] = 'dsp'

from board import boards
import pygame
import math

print('start game')
pygame.init()



WIDTH = 900
HEIGHT = 950
screen = pygame.display.set_mode([WIDTH,HEIGHT])
timer = pygame.time.Clock()
fps = 60
level = boards
color = 'blue'
# font = pygame.font.Font('freesansbold.ttf', 20)
PI = math.pi

def draw_boad(lvl):
    num1 = ((HEIGHT -  50) // 32)
    num2 = (WIDTH // 30)
    for i in range(len(lvl)):
        for j in range(len(lvl[i])):
            if lvl[i][j] == 1:
                pygame.draw.circle(screen, 'white', (j * num2 + (0.5*num2), i * num1 + (0.5 * num1)), 4)
            if lvl[i][j] == 2:
                pygame.draw.circle(screen, 'white', (j * num2 + (0.5*num2), i * num1 + (0.5 * num1)), 10)
            if lvl[i][j] == 3:
                pygame.draw.line(screen, color, (j * num2 + (0.5 * num2), i*num1),
                                 (j * num2 + (0.5 * num2), i*num1 + num1), 3)
            if lvl[i][j] == 4:
                pygame.draw.line(screen, color, (j * num2, i*num1 + (0.5*num1)),
                                 (j * num2 + num2, i*num1 + (0.5*num1)), 3)
            if lvl[i][j] == 5:
                pygame.draw.arc(screen, color, [(j*num2 - (num2*0.5)), (i * num1 + (0.5*num1)), num2, num1], 0, PI/2, 3)

            if lvl[i][j] == 9:
                pygame.draw.line(screen, 'white', (j * num2, i*num1 + (0.5*num1)),
                                 (j * num2 + num2, i*num1 + (0.5*num1)), 3)




run = True

if run == True:
    print('game is running')

while run:
    timer.tick(fps)
    screen.fill('black')
    draw_boad(boards)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print('quitting game')
            run = False

    pygame.display.flip()
pygame.quit()
