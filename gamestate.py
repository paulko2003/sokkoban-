from entities import player,box
from copy import deepcopy
from parser import GOAL_LIST,GLOBAL_MAP,INITIAL_BOXES
import heapq

class gameState:
        def __init__(self,box_map: list, play:player):
            self.box_map=[box(*box_pos) for box_pos in box_map]
            self.player=player(*play, self.box_map)
            self.won=False

        def set_value(self):
            boxes = frozenset((b.y, b.x) for b in self.box_map)
            player = (self.player.y, self.player.x)
            return (boxes, player)
                
        def movePlayer(self,move):
            self.player.move(move,self.box_map)

        def checkForBox(self,move):
            return self.player._boxInFront(move)
        
        def getBox(self,move):
            return self.player._fetchBox(self.player.targetPos(move))

        def checkWin(self):
            for box in self.box_map:
                if not box.on_goal:
                    return False
            self.won=True
            return True


class stateNode():
    def __init__(self,c_cost: int,state:gameState, parent ):
        self.state=state
        self.c_cost=c_cost
        self.h_cost=self.newHeuristic(self.state) #if value <0 then its a loose state or a repeating one
        self.total_cost= self.c_cost+self.h_cost
        self.kids=[]
        self.parent=parent
        for i in range(4):
            self.kids.append(None)

    def _cost(self):
        return self.c_cost+self.h_cost
    
    def __eq__(self,value: stateNode):
        if type(value)==type(stateNode):
            return self.total_cost == value.total_cost
        return None
    
    def __lt__(self, value: stateNode):
        return self.total_cost < value.total_cost

    def boxPositions(self):
        box_positions=[i.pos() for i in self.state.box_map]
        return box_positions
    
    def buildKid(self, move: int, built_states: set):
        boxes=[(self.state.box_map[i].y,self.state.box_map[i].x) for i in range(len(self.state.box_map))]
        player=(self.state.player.y,self.state.player.x)
        stateBuilt=gameState(boxes,player)
        c_cost=1
        stateBuilt.movePlayer(move)
        if stateBuilt.set_value() in built_states: 
            return None
        kid= stateNode(self.c_cost+c_cost,stateBuilt,self)
        self.kids[move]=kid
        return kid
    
    def newHeuristic(self, state: gameState):
        # einai h apostash manhatan olwn ton koytiown apo to kontinotero mh piasmeno goal + thn apostash toy pexti apo to kontinotero mh piasmeno box + thn apostash toy apo to closest mh piasmeno goal
        for box in state.box_map:
            if box.boxStuck(state.box_map):
                return 100000
        h_cost=0
        to_remove=set()
        available_goals=set(GOAL_LIST)
        available_boxes=set([(box.y,box.x) for box in state.box_map])
        for box in available_boxes:
            if box in available_goals:
                to_remove.add(box)
        for pos in to_remove:
            available_boxes.remove(pos)
            available_goals.remove(pos)
        # apostash manhatan olwn ton koytiown apo to kontinotero mh piasmeno goal
        for goal in available_goals:
            min_value=900
            min_box=None
            for box in available_boxes:
                y_value=abs(box[0]-goal[0])
                x_value=abs(box[1]-goal[1])
                value=y_value+x_value
                if value<min_value:
                    min_value=value
                    min_box=box
            h_cost+=min_value
            available_boxes.remove(min_box)
        return h_cost

class gameTree:
    def __init__(self, initial_state: gameState):
        self.head=stateNode(0, initial_state, None)
        self.closed_set=set()
        self.investigating=list()
        heapq.heappush(self.investigating,(self.head.total_cost, self.head))
        self.closed_set.add(self.head.state.set_value())
        self.min=self.investigating[0]
        self.won=False

    def buildKids(self, node: stateNode):
        if(node.h_cost==0):
            return True
        for i in range(4):
            if(node.state.player.canMove(i,node.state.box_map)):
                kid=node.buildKid(i, self.closed_set)
                if kid != None:
                    heapq.heappush(self.investigating,(kid.total_cost, kid))
                    self.closed_set.add(kid.state.set_value())

    
    def buildDepth5(self):
        parent=heapq.heappop(self.investigating)[1]
        # if parent.h_cost==100000:
        #     print("how are we here")
        #     return
        self.min=parent
        self.buildKids(parent)
            
        

    def checkWin(self):
        value= self.min
        
        if value.h_cost==0:
            self.won = True
            return value
        
    

