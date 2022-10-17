import tkinter
import pathfinding
import random as r

class Food():
    def __init__(self):
        self.Randomize_position()
    def Render(self, canvas):
        return canvas.create_rectangle(self.x, self.y, self.x+24, self.y+24, fill="red")
    def Randomize_position(self):
        self.x = r.randint(0,500-25)
        difference_in_x = self.x%25
        self.x -= difference_in_x
        self.y = r.randint(0,500-25)
        difference_in_y = self.y%25
        self.y -= difference_in_y

class Snake_part():
    def __init__(self, isHead, x, y):
        self.isHead = isHead
        if(isHead):
            self.color = "lime"
        else:
            self.color = "green"
        self.x = x-(x%25)
        self.y = y-(y%25)
    def Render(self, canvas):
        return canvas.create_rectangle(self.x, self.y, self.x+24, self.y+24, fill=self.color)
    def Did_hit(self, otherpart):
        if self.x == otherpart.x and self.y == otherpart.y:
            return True
        else:
            return False

class GUI:
    def __init__(self):
        self.score = 0
        self.parts = []
        self.reset_snake()
        self.food = Food()
        self.root = tkinter.Tk()
        self.canvas = tkinter.Canvas(self.root, width = 500, height = 500, bg="grey")
        self.canvas.pack()
        self.pathing = pathfinding.pathfinder(self.parts, self.food)

    def reset_snake(self):
        self.parts = []
        for i in range(7):
            self.parts.append(Snake_part(i==0,(500)/2, (500)/2 + 25*i))

    def render_pathing(self):
        for i in self.pathing.best_path:
            self.canvas.create_rectangle(i.x, i.y, i.x+24, i.y+24, fill="yellow")

    def check_food_in_snake(self):
        in_snake = True
        while in_snake == True:
            in_snake = False
            for i in self.parts:
                if self.food.x == i.x and self.food.y == i.y:
                    in_snake = True
                    self.food.Randomize_position()

    def move_snake(self):
        temp_x = self.parts[0].x
        temp_y = self.parts[0].y
        self.parts.insert(1, Snake_part(False, temp_x, temp_y))
        self.parts[0].x = self.pathing.best_path[-1].x
        self.parts[0].y = self.pathing.best_path[-1].y

        if self.parts[0].x == self.food.x and self.parts[0].y == self.food.y:
            self.food.Randomize_position()
            self.score += 1
            print(self.score)
        else:            
            self.parts.pop()

        if self.pathing.in_walls(self.parts[0].x, self.parts[0].y):
            self.score = 0
            print(self.score)
            self.reset_snake()
        
    def update(self):
        #self.check_food_in_snake()
        self.pathing.update(self.parts, self.food)
        self.move_snake()
        self.render_pathing()
        for i in self.parts:
            i.Render(self.canvas)
        self.food.Render(self.canvas)
        self.root.update()
        self.canvas.after(25)
        self.canvas.delete("all")