
import pygame, sys, random
from parser import GOAL_LIST,GLOBAL_MAP
import os
from entities import player,box
#gpt generated this/


pygame.init()
# Colours
BACKGROUND = (255, 255, 255)
boxes_colour=(205, 127, 50)
boxes_goal_colour=(123, 63, 0)
wall_colour=(0,0,0)
player_colour=(218,165,32)
goal_colour=(100,149,237)
grid_colour=(125,125,125)
# Game Setup
FPS = 60
fpsClock = pygame.time.Clock()

WINDOW_WIDTH = 64*len(GLOBAL_MAP[0])
WINDOW_HEIGHT = 64*len(GLOBAL_MAP)
SPRITE_SIZE=(64,64)
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('sokkoban')

# The main function that controls the game
def drawBox(boxList: list):
    for box in boxList:
        if not box.on_goal:
            pygame.draw.rect(WINDOW, boxes_colour, [box.x*64, box.y*64, 64, 64], 0)
        else:
            pygame.draw.rect(WINDOW, boxes_goal_colour, [box.x*64, box.y*64, 64, 64], 0)

def drawGoals():
    for goal in GOAL_LIST:
        pygame.draw.ellipse(WINDOW, goal_colour , [goal[1]*64 + 16, goal[0]* 64 + 16, 32, 32], 0)

def drawWalls():
    for row in range(len(GLOBAL_MAP)):
        for wall in range(len(GLOBAL_MAP[0])):
            if not GLOBAL_MAP[row][wall]:
                pygame.draw.rect(WINDOW, wall_colour, [wall*64, row*64, 64, 64], 0)

def drawGrid():
    for row in range(len(GLOBAL_MAP)):
        pygame.draw.line(WINDOW, grid_colour, [0, 64*row], [WINDOW_WIDTH, row*64], 1)
    for row in range(len(GLOBAL_MAP[0])):
        pygame.draw.line(WINDOW, grid_colour, [64*row,0], [row*64,WINDOW_HEIGHT], 1)

def drawPlayer(player:player):
    pygame.draw.rect(WINDOW, player_colour, [player.x*64+16, player.y*64+16, 32, 32], 0)

def worldDraw () :
    WINDOW.fill(BACKGROUND)
    drawGoals()
    drawWalls()
    drawGrid()

def update(gameState):
    worldDraw()
    drawBox(gameState.box_map)
    drawPlayer(gameState.player)
    pygame.display.flip()
    pygame.event.pump() 

def quit():
    pygame.quit()


def eventChecker():
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()