
import random

class wall:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class position:
    def __init__(self, x, y, distance):
        self.x = x
        self.y = y
        self.distance = distance        

class pathfinder:
    def __init__(self, parts, target):
        self.walls = []
        self.positions = []
        self.last_scan = []
        self.best_path = []

        self.target = wall(target.x, target.y)

        for i in parts:
            if i.isHead == False:
                self.walls.append(wall(i.x, i.y))
            else:
                self.positions.append(position(i.x, i.y, 0))
                self.last_scan.append(position(i.x, i.y, 0))
        for i in range(10):
            self.scan(i+1)

    def in_walls(self, x, y):
        return_me = False
        for i in self.walls:
            if x == i.x and y == i.y:
                return_me = True
        return return_me
    def in_positions(self, x, y):
        return_me = False
        for i in self.positions:
            if x == i.x and y == i.y:
                return_me = True
        return return_me
    def in_best(self, x, y):
        return_me = False
        for i in self.best_path:
            if x == i.x and y == i.y:
                return_me = True
        return return_me        
    def found_target(self):
        return_me = False
        for i in self.positions:
            if self.target.x == i.x and self.target.y == i.y:
                return_me = True
        return return_me        
    def get_next_closest(self, x, y, distance, running = False):
        valid_positions = []
        if running == False:
            for i in self.positions:
                if i.distance == distance - 1:
                    if ( x + 25 == i.x or x - 25 == i.x )and y == i.y:
                        valid_positions.append(position(i.x, i.y, distance-1))
                    elif x == i.x and (y+25 == i.y or y-25 == i.y):
                            valid_positions.append(position(i.x, i.y, distance-1))
            return random.choice(valid_positions)      
        elif running == True:
            prefered = []
            for i in self.positions:
                if self.in_best(i.x, i.y) == False:
                    if i.distance == distance:
                        if ( x + 25 == i.x or x - 25 == i.x )and y == i.y:
                            prefered.append(position(i.x, i.y, distance-1))
                        elif x == i.x and (y+25 == i.y or y-25 == i.y):
                            prefered.append(position(i.x, i.y, distance-1))
                    if i.distance == distance - 1:
                        if ( x + 25 == i.x or x - 25 == i.x )and y == i.y:
                            valid_positions.append(position(i.x, i.y, distance-1))
                        elif x == i.x and (y+25 == i.y or y-25 == i.y):
                            valid_positions.append(position(i.x, i.y, distance-1))
            if len(prefered) > 0:
                return random.choice(prefered)
            return random.choice(valid_positions)      
                
                  
                
    def update(self, parts, target):
        self.walls = []
        self.positions = []
        self.last_scan = []

        self.target = wall(target.x, target.y)

        for i in parts:
            if i.isHead == False:
                self.walls.append(wall(i.x, i.y))
            else:
                self.positions.append(position(i.x, i.y, 0))
                self.last_scan.append(position(i.x, i.y, 0))
        #for i in range(10):
        counter = 0
        found_last_scan = 1
        while self.found_target() == False and found_last_scan != 0:
            counter+=1
            found_last_scan = self.scan(counter)

        if found_last_scan != 0:
            self.best_path = []
            current = position(self.target.x, self.target.y, counter)
            self.best_path.append(current)
            while counter > 1:
                counter -=1
                current = self.get_next_closest(current.x, current.y, current.distance)
                self.best_path.append(current)
        else:
            self.best_path = []
            furthest_distances = []
            for i in self.positions:
                if i.distance == counter - 1:
                    furthest_distances.append(i)
            current = random.choice(furthest_distances)
            self.best_path.append(current)
            while counter > 2:
                counter -=1
                current = self.get_next_closest(current.x, current.y, current.distance, True)
                self.best_path.append(current)

            

    def scan(self, scan_number):
        temp = self.last_scan

        self.last_scan = []        
        for i in temp:
            if self.in_walls(i.x+25, i.y) == False and self.in_positions(i.x+25, i.y) == False and i.x+25 < 500:
                self.positions.append(position(i.x+25, i.y,scan_number))
                self.last_scan.append(position(i.x+25, i.y,scan_number)) 
            if self.in_walls(i.x-25, i.y) == False and self.in_positions(i.x-25, i.y) == False and i.x-25 >= 0:
                self.positions.append(position(i.x-25, i.y,scan_number))
                self.last_scan.append(position(i.x-25, i.y,scan_number)) 
            if self.in_walls(i.x, i.y+25) == False and self.in_positions(i.x, i.y+25) == False and i.y+25 < 500:
                self.positions.append(position(i.x, i.y+25,scan_number))
                self.last_scan.append(position(i.x, i.y+25,scan_number))  
            if self.in_walls(i.x, i.y-25) == False and self.in_positions(i.x, i.y-25) == False and i.y-25 >= 0:
                self.positions.append(position(i.x, i.y-25,scan_number))
                self.last_scan.append(position(i.x, i.y-25,scan_number))
        
        return len(self.last_scan)