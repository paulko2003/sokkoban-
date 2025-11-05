# = wall (solid, never moves)
# space = floor (walkable)
# @ = player on floor
# $ = box/crate on floor
# . = goal/target cell
# * = box on a goal (already correctly placed)


#apothikevw 
# grid: True walkable False wall
# player position (y,x)
# box position [(y,x),..]
# goal position [(y,x),..]
class parser:
    def __init__(self,file_path="init.txt"):
               
        self.game_map_ground=list()
        self.player=tuple()
        self.boxes=list()
        self.goals=list()
        self.map_size=0
        self._path=file_path
        self._parser()

    def _parser(self):
        with open(self._path, 'r', encoding='utf-8') as file:
            full_map=file.readlines()
        #clean up \n
        for i in range(len(full_map)):
            if('\n' in full_map[i]):
                full_map[i]=full_map[i][0:-1]
        
        self.map_size= len(max(full_map,key=len))
        for y,line in enumerate(full_map):
            self.game_map_ground.append(list())
            for x in range(len(line)):
                if (line[x] == '#') or (line[x] == ' '):
                    self.game_map_ground[-1].append(line[x]==' ')
                elif(line[x] == '.'):
                    self.goals.append([y,x])
                    self.game_map_ground[-1].append(True)
                elif (line[x] == '@'):
                    self.player=(y,x)
                    self.game_map_ground[-1].append(True)
                elif(line[x] == '$'):
                    self.boxes.append([y,x])
                    self.game_map_ground[-1].append(True)
                elif (line[x] == '*'):
                    self.game_map_ground[-1].append(True)
                    self.goals.append([y,x])
                    self.boxes.append([y,x])
                elif(line[x] == '+'):
                    self.game_map_ground[-1].append(True)
                    self.player=(y,x)
                    self.goals.append([y,x])
                else:
                    raise Exception(f"character {line[x]} not in {"# $.*@"}")
            # fill in empty spaces to get grid structure
            
            for i in range(self.map_size-len(line)):
                self.game_map_ground[-1].append(True)
        return 1

parse=parser()
GOAL_LIST=parse.goals
print(GOAL_LIST)
GLOBAL_MAP=parse.game_map_ground
# player, boxes and goals are "living entities", not on map g