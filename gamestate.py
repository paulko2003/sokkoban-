from entities import player,box
from copy import deepcopy
from parser import GOAL_LIST,GLOBAL_MAP
import heapq

class gameState:
        def __init__(self,box_map: list, play:player):
            self.box_map=[box(*box_pos) for box_pos in box_map]
            # for box_pos in box_map:
            #     self.box_map.append(box(*box_pos))
            # # print("box mpa", self.box_map)
            self.player=player(*play, self.box_map)
            
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
            # print("you won")
            return True

        # def __eq__(self, value:gameState):
            # my_boxes=[]
            # value_boxes=[]
            # for i in range(len(self.box_map)):
            #     my_boxes.append([self.box_map[i].y,self.box_map[i].x])
            #     value_boxes.append([value.box_map[i].y,value.box_map[i].x])
            # my_player=(self.player.y,self.player.x)
            # value_player=(value.player.y,value.player.x)
            # same_player= my_player[0] == value_player[0] and my_player[1]==value_player[1]
            # if not same_player:
            #     return False
            # same_boxes=True
            # for box in my_boxes:
            #     # print(box)
            #     if not (box in value_boxes):
            #         same_boxes=False
            #         break
            # print("in here")
            # return 1



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
    
    def buildKid(self, move: int):
        # boxes=[]
        # for box in self.state.box_map:
        #     boxes.append(box.pos())
        # stateBuilt=gameState(boxes,self.state.player.pos())
        boxes=[self.state.box_map[i].pos() for i in range(len(self.state.box_map))]
        player=self.state.player.pos()
        stateBuilt=gameState(boxes,player)
        c_cost=1
        stateBuilt.movePlayer(move)
        kid= stateNode(self.c_cost+c_cost,stateBuilt,self)
        self.kids[move]=kid
        return kid
    
    
    def newHeuristic(self, state: gameState):
        # einai h apostash manhatan olwn ton koytiown apo to kontinotero mh piasmeno goal + thn apostash toy pexti apo to kontinotero mh piasmeno box + thn apostash toy apo to closest mh piasmeno goal
        for box in state.box_map:
            if box.boxStuck(state.box_map):
                return -1
        h_cost=0
        available_goals=[goal for goal in GOAL_LIST]
        available_boxes=[box.pos() for box in state.box_map]
        for box in range(len(available_boxes)):
            try:
                available_goals.remove(available_boxes[box])
                available_boxes.remove(available_boxes[box])
            except Exception:
                continue
        # apostash manhatan olwn ton koytiown apo to kontinotero mh piasmeno goal
        for box in range(len(available_boxes)):
            min_value=900
            min_goal=None
            for goal in available_goals:
                y_value=abs(available_boxes[box][0]-goal[0])
                x_value=abs(available_boxes[box][1]-goal[1])
                value=y_value+x_value
                if value<min_value:
                    min_value=value
                    min_goal=goal
            h_cost+=min_value
            available_goals.remove(min_goal)

        # pos=state.player.pos()
        
        # min_dist=9000
        # for inner_box in range(len(available_boxes)):
        #     pos_x=abs(pos[1]-available_boxes[inner_box][1])
        #     pos_y=abs(pos[1]-available_boxes[inner_box][0]) 
        #     value=pos_x+pos_y
        #     if value<min_dist:
        #         min_dist=value
        # h_cost+=min_dist
        return h_cost

    def bearbones(self, state: gameState):
        # einai h apostash manhatan olwn ton koytiown apo to kontinotero pros to kathena goal, piasmeno h mh + thn apostash toy pexti apo to kontinotero box, on goal or not
        for box in state.box_map:
            if box.boxStuck(state.box_map):
                return -1
        h_cost=0
        for box in range(len(state.box_map)): #elenxei apo to kontinotero goal kai as einai piasmeno, as poyme fine.
            values= [abs(state.box_map[box].y-goal[0])+abs(state.box_map[box].x-goal[1]) for goal in GOAL_LIST] #einai faster me generator for sum reason
            # for goal in GOAL_LIST:
            #     y=abs(state.box_map[box].y-goal[0])
            #     x=abs(state.box_map[box].x-goal[1])
            #     value=x+y
            #     # print(value)
            #     values.append(value)
            values.sort()
            # print(values)
            h_cost+=values[0]
        if h_cost==0:
            # print("GAME IS DONE")
            print("finished here!!!!!!!!!!")
            return 0
        # print(len(working_boxes)==len(working_goals))
        values=[abs(state.player.x-state.box_map[box].x)+abs(state.player.y-state.box_map[box].y) for box in range(len(state.box_map))]
        # for box in range(len(state.box_map)):

        #     x=abs(state.player.x-state.box_map[box].x)
        #     y=abs(state.player.y-state.box_map[box].y)
        #     value=x+y
        #     values.append(value)
        values.sort()
        h_cost+=values[0]
        return h_cost

class gameTree:
    def __init__(self, initial_state: gameState):
        self.head=stateNode(0, initial_state, None)
        self.closed_set=set()
        self.investigating=list()
        heapq.heappush(self.investigating,(self.head.total_cost, self.head))
        self.closed_set.add(self.head.state.set_value())
        # self.min=self.investigating[0]
        self.won=False

    def buildKids(self, node: stateNode):
        if node.h_cost==-1:
            # # self.investigating.remove(node)
            # heapq.heappop(self.investigating)
            # # print("to the shadow realm")
            # # print(node.h_cost,"here")
            return False
        if(node.h_cost==0):
            return True
        for i in range(4):
            if(node.state.player.canMove(i,node.state.box_map)):
                kid=node.buildKid(i)
                if not(kid.state.set_value() in self.closed_set):
                    # self.investigating.append(kid)
                    heapq.heappush(self.investigating,(kid.total_cost, kid))
                    self.closed_set.add(kid.state.set_value())
        # self.investigating.remove(node)
        # self.investigating.sort(key=stateNode._cost)
        # self.min=self.investigating[0]
    
    def buildDepth5(self):
        # parent=self.investigating[0]
        parent=heapq.heappop(self.investigating)[1]
        if parent.h_cost==-1:
            return
        self.min=parent
        self.buildKids(parent)
            
        

    def checkWin(self):
        value= self.min
        
        if value.h_cost==0:
            # print(value.h_cost)
            self.won = True
            return value
        
    

