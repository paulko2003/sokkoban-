from parser import GOAL_LIST,GLOBAL_MAP,INITIAL_BOXES
import numpy as np
# making corners illegal for boxes gia na mhn mporei na paei ekei efoson einai stuck state, Global_map = allowed player moves. Box_legal allowed box positions
width=len(GLOBAL_MAP[0])
BOX_LEGAL=list()
BOX_LEGAL.append([False for i in range(width)])
for i in range(1,len(GLOBAL_MAP)-1):
    BOX_LEGAL.append([False])
    for j in range(1,width-1):
        if(not GLOBAL_MAP[i][j]):
            BOX_LEGAL[i].append(False)
            continue
        left_up=not (GLOBAL_MAP[i-1][j] or GLOBAL_MAP[i][j-1]) #demorgan lol
        left_down=not (GLOBAL_MAP[i-1][j] or GLOBAL_MAP[i][j+1])
        right_up=not (GLOBAL_MAP[i+1][j] or GLOBAL_MAP[i][j-1])
        right_down=not (GLOBAL_MAP[i+1][j] or GLOBAL_MAP[i][j+1])
        BOX_LEGAL[i].append(not( left_up or left_down or right_down or right_up) or (i,j) in GOAL_LIST)
    BOX_LEGAL[i].append(False)
BOX_LEGAL.append([False for i in range(width)])
BOX_LEGAL=np.array(BOX_LEGAL)
MOVE_SET=((-1,0),(0,1),(1,0),(0,-1))

global_height=len(GLOBAL_MAP)
global_width=len(GLOBAL_MAP[0])

class entity:
    def __init__(self, y:int, x:int):
        self.y=y
        self.x=x
        
    # clockwise moving pattern
    # 0 up, 1 right 2 bottom 3 left
    def targetPos(self, move: int) -> tuple:
        target_y=self.y + MOVE_SET[move][0]
        target_x=self.x + MOVE_SET[move][1]
        return (target_y,target_x)
    
    def clearFront(self, move: int, box_map: list) -> bool:
        target=self.targetPos(move)
        y_pos=target[0]
        x_pos=target[1]
        if y_pos>=len(GLOBAL_MAP) or x_pos>=len(GLOBAL_MAP[0]):
            return False
        if GLOBAL_MAP[target[0]][target[1]] and (target not in box_map):
            return True
        return False


    def pos(self):
        return (self.y,self.x)
    
    def __eq__(self, value):
        # return self.pos() == value 10x slower
        return self.y==value[0] and self.x==value[1]
    
    def _boxInFront(self, move: int, box_map: list):
        return self.targetPos(move) in box_map
    
    def _fetchBox(self, position: tuple, box_map: list)-> box:
        for i in range(len(box_map)):
            if box_map[i]==position:
                return box_map[i]

class box(entity):
    def __init__(self, y, x):
        super().__init__(y, x)
        self.on_goal=self.onGoal()
    
    def clearFront(self, move: int, box_map: list) -> bool:
        target=self.targetPos(move)
        y_pos=target[0]
        x_pos=target[1]
        if y_pos>=len(BOX_LEGAL) or x_pos>=len(BOX_LEGAL[0]):
            return False
        if BOX_LEGAL[target[0]][target[1]] and (target not in box_map):
            return True
        return False


    def canMove(self, move: int, box_map: list) -> int:
        # gotta move it move it
        if self.clearFront(move,box_map): #and self.clearFront(self._inverseMove(move),box_map):
            return 1
        # stuck for said move
        return 0
    
    def move(self, move: int, box_map: list) -> None:
        if self.canMove(move, box_map)==1:
            self.y+=MOVE_SET[move][0]
            self.x+=MOVE_SET[move][1]
            self.on_goal=self.onGoal()



    # takes a grid [[x-1y-1,y-1,x+1y-1],    kai elenxei gia group apo tetrades na dei an einai kapoio se tetrada. (den elenxei thn thesh toy box giati panta true)
    #               [x-1,my box_pos,x+1],
    #               [x-1y+1,y+1,x+1y-1]]
    def boxStuck(self, box_map):
        if self.on_goal:
            return False

        box_set = set([(b.y, b.x) for b in box_map])

        y,x = self.y,self.x
        y_dec,y_inc=y-1, y+1
        x_dec,x_inc=x-1, x+1
        row_eq  = GLOBAL_MAP[y][x_dec:x_inc+1]
        mid_l = ((y , x_dec) in box_set) or (not row_eq[0]) #mid left
        mid_r = ((y , x_inc) in box_set) or (not row_eq[2]) #mid right
        if not (mid_l or mid_r): return False
        row_dec = GLOBAL_MAP[y_dec][x_dec:x_inc+1]
        row_inc = GLOBAL_MAP[y_inc][x_dec:x_inc+1]
        up_m = ((y_dec, x ) in box_set) or (not row_dec[1]) #up
        bot_m = ((y_inc, x ) in box_set) or (not row_inc[1]) #bottom 
        if not (up_m or bot_m): return False
        
        up_l = ((y_dec, x_dec) in box_set) or (not row_dec[0]) #up left
        up_r = ((y_dec, x_inc) in box_set) or (not row_dec[2]) #up right

        mid_l = ((y , x_dec) in box_set) or (not row_eq[0]) #mid left
        mid_r = ((y , x_inc) in box_set) or (not row_eq[2]) #mid right

        bot_l = ((y_inc, x_dec) in box_set) or (not row_inc[0]) #bottom left
        bot_r = ((y_inc, x_inc) in box_set) or (not row_inc[2]) #bottom right

        if (up_l and up_m and mid_l ): return True #panw aristera kai panw kentro kai mesi aristera kai kentro 
        if (mid_l and bot_l and bot_m): return True ##...
        if (up_m and up_r and mid_r): return True
        if (mid_r and bot_r and bot_m): return True
        return False

    
    # 10-20% faster thn OG ,
    # def boxStuck(self, box_map):
    #     if self.on_goal:
    #         return False
    #     res=False
    #     box_set=set()
    #     for box in box_map: box_set.add(box.y,box.x)
    #     for i in range(-1,2,1):
    #         if res: return True
    #         for j in range(-1,2,1):
    #             res=(not GLOBAL_MAP[self.y+i,self.x+j]) and (not GLOBAL_MAP[self.y+i,self.x+j+1]) and (not GLOBAL_MAP[self.y+i+1,self.x+j]) and (not GLOBAL_MAP[self.y+i+1,self.x+j+1])
    #     return res
    
    # slow
    # # def boxStuck(self, box_map):
    #     if self.on_goal:
    #         return False
    #     grid_box=[
    #             [],
    #             [],
    #             []]
    #     for i in [-1,0,1]:
    #         for j in [-1,0,1]:
    #             grid_box[i+1].append([self.y+i,self.x+j] in box_map)
    #     grid_wall=[
    #             [],
    #             [],
    #             []]
    #     for i in [-1,0,1]:
    #         for j in [-1,0,1]:
    #             grid_wall[i+1].append(GLOBAL_MAP[self.y+i][self.x+j])
    #     final_grid=[
    #             [],
    #             [],
    #             []]
    #     for i in range(3):
    #         for j in range(3):
    #             final_grid[i].append(grid_box[i][j] or not grid_wall[i][j])

    #     for i in range(2):
    #         for j in range(2):
    #             if final_grid[i][j] and final_grid[i][j+1] and final_grid[i+1][j] and final_grid[i+1][j+1]:
    #                 return True
    #     return False

    def onGoal(self) -> bool:
        return self.pos() in GOAL_LIST

class player(entity):
        def __init__(self, y: int, x: int, box_map: list):
            super().__init__(y, x)
            self.boxes=box_map
        
        def _boxInFront(self, move):
            return super()._boxInFront(move, self.boxes)
        
        def _fetchBox(self, position):
            return super()._fetchBox(position, self.boxes)
        
        # 0 no, -1 moves box but can move , 1 can move
        def canMove(self, move: int,  box_map: list) -> int:
            if self.clearFront(move,box_map):
                return 1
            if not self._boxInFront(move):
                return 0    
            target=self.targetPos(move)
            front_box=self._fetchBox(target)
            if front_box.canMove(move,box_map)==1:
                return -1
            return 0

        def move(self, move: int,box_map: list) -> None:
            target=self.targetPos(move)
            move_result=self.canMove(move,box_map)
            if move_result == 0:
                return None
            if move_result==-1:
                target_box=self._fetchBox(target)
                target_box.move(move,box_map)
            self.y=target[0]
            self.x=target[1]