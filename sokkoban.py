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
    
    def show_travel(self, node):
        move_stack=[node]
        while move_stack[-1].parent != None:
            move_stack.append(move_stack[-1].parent)
        print(f"won with {len(move_stack)-1} moves")
        for state in range(len(move_stack)-1, -1, -1):
            # print(state)
            showing_state=move_stack[state].state
            update(showing_state)
            sleep(0.2)

    def show_state(self,node):
        showing_state=node.state
        update(showing_state)
        sleep(0.2)

    def main(self):
        game=gameTree(self.initial_playstate)
        won = game.won
        update(self.initial_playstate)
        while not won:
            game.buildDepth5()
            # print(game.investigating,"----------------")
            game.checkWin()
            won= game.won
            # self.show_state(game.min)
        print(len(game.closed_set))
        self.show_travel(game.min)
        
        
sokkoban().main()

