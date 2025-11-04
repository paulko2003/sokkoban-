from parser import parser, GOAL_LIST,GLOBAL_MAP
from entities import box,player
from visualisation import update, eventChecker,quit
from gamestate import gameState,gameTree
import copy
from time import sleep




class sokkoban:
    
    def __init__(self):
        parse=parser()
        # we dont touch we only copy
        print(parse.boxes,parse.player)
        self.initial_playstate=gameState(parse.boxes, parse.player)
    
    def main(self):
        game=gameTree(self.initial_playstate)
        won = game.won
        update(self.initial_playstate)
        while not won:
            game.buildDepth5()
            # print(game.investigating,"----------------")
            game.checkWin()
            won= game.won
        print(len(game.closed_set))
        move_stack=[game.min]
        while move_stack[-1].parent != None:
            move_stack.append(move_stack[-1].parent)
        # print(len(move_stack))
        print(f"won with {len(move_stack)} moves")
        for state in range(len(move_stack)-1, -1, -1):
            # print(state)
            showing_state=move_stack[state].state
            update(showing_state)
            update(showing_state)
            sleep(0.2)
        quit()
sokkoban().main()

