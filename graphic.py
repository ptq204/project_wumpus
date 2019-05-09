import turtle
import math
from logic import findPathOfGame
import sys
#---------------SET UP MAP-------------------------
print(sys.argv)
if(len(sys.argv) > 1):
    f = open('map0' + sys.argv[1] + '.txt')
N = int(f.readline())
m = [[j for j in line.split()] for line in f]
area_1_block = 55
width = N*area_1_block
height = N*area_1_block
mostRight = int(width/2)
mostTop = int(height/2)
mostLeft = -mostRight
mostBottom = -mostTop
#--------------------------------------------------

wn = turtle.Screen() 

wn.bgcolor("white") 
wn.title("Wumpus World")
wn.setup(700, 700)

wn.register_shape("image/monster.gif")
wn.register_shape("image/gold.gif")
wn.register_shape("image/treasure.gif")
wn.register_shape("image/agent.gif")
wn.register_shape("image/gate.gif")
wn.register_shape("image/s.gif")
wn.register_shape("image/b.gif")
wn.register_shape("image/bs.gif")
wn.register_shape("image/bgs.gif")

class Pen(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("gray")
        self.penup()
        self.speed(0)
        self.shapesize(2.5,2.5)

class Gate(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("image/gate.gif")
        self.penup()
        self.speed(0)
        self.shapesize(2.5,2.5)

class Gold(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape("image/treasure.gif")
        self.penup()
        self.speed(0)
        self.reward = 100
        self.goto(x, y)
        self.shapesize(2,2)

    def destroy(self):
        self.goto(5000, 5000)
        self.hideturtle()

class Wumpus(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape("image/monster.gif")
        self.penup()
        self.speed(0)
        self.goto(x, y) 
        self.shapesize(2,2) 

class Stench(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape("image/s.gif")
        self.penup()
        self.speed(0)
        self.goto(x, y) 
        self.shapesize(2,2)        

class Pit(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape("circle")
        self.color("black")
        self.penup()
        self.speed(0)
        self.goto(x, y)   
        self.shapesize(2.5,2.5)      

class Breeze(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape("image/b.gif")
        self.penup()
        self.speed(0)
        self.goto(x, y) 
        self.shapesize(2,2)

class BreezeAndStench(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape("image/bs.gif")
        self.penup()
        self.speed(0)
        self.goto(x, y) 
        self.shapesize(2,2)   

class BreezeAndStenchAndGold(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape("image/bgs.gif")
        self.penup()
        self.speed(0)
        self.reward = 100
        self.goto(x, y) 
        self.shapesize(2,2)    
        
    def destroy(self):
        self.goto(5000, 5000)
        self.hideturtle()    

class Agent(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("circle")
        self.color("green")
        self.penup()
        self.speed(1)
        self.point = 0
        self.shapesize(2,2)

    def go_up(self):
        move_to_x = agent.xcor()
        move_to_y = agent.ycor() + area_1_block
        self.goto(move_to_x, move_to_y)

    def go_down(self):
        move_to_x = agent.xcor()
        move_to_y = agent.ycor() - area_1_block
        self.goto(move_to_x, move_to_y)        

    def go_left(self):
        move_to_x = agent.xcor() - area_1_block
        move_to_y = agent.ycor()
        self.goto(move_to_x, move_to_y)        

    def go_right(self):
        move_to_x = agent.xcor() + area_1_block
        move_to_y = agent.ycor() 
        self.goto(move_to_x, move_to_y)

    def is_collision(self, other):
        if self.xcor() == other.xcor() and self.ycor() == other.ycor():
            return True
        else:
            return False

    def destroy(self):
        self.goto(5000, 5000)
        self.hideturtle()

levels = [""]
goldList = []
wumpusList = []
stenchList = [] 
breezeList = []
pitList = [] 
bsList = []
bgsList = []
level_1 = m
levels.append(level_1)

def setup_maze(level):
        for x in range (len(level)):
            for y in range (len(level[x])):
                character = level[x][y]
                screen_x = mostLeft + (y *area_1_block)
                screen_y = mostTop -(x *area_1_block) 

                if character == '-':
                    pen.goto(screen_x, screen_y)
                    pen.stamp()
                
                if character == 'S':
                    stenchList.append(Stench(screen_x, screen_y))
                    x_stench = x
                    y_stench = y   

                if character == 'B':
                    breezeList.append(Breeze(screen_x, screen_y))
                    x_breeze = x
                    y_breeze = y
                
                if character == 'BS' or character == 'SB':
                    bsList.append(BreezeAndStench(screen_x, screen_y))
                    x_bs = x
                    y_bs = y

                if character == 'BGS' or character == 'BSG' or character == 'GSB' or character == 'GBS' or character == 'SGB' or character == 'SBG':
                    bgsList.append(BreezeAndStenchAndGold(screen_x, screen_y))
                    x_bgs = x
                    y_bgs = y

                if character == 'A':
                    agent.goto(screen_x, screen_y)
                    gate.goto(screen_x, screen_y)
                    x_agent = x
                    y_agent = y

                if character == 'G':
                    goldList.append(Gold(screen_x, screen_y))
                    x_gold = x
                    y_gold = y 
                if character == 'W':
                    wumpusList.append(Wumpus(screen_x, screen_y))
                    x_wumpus = x
                    y_wumpus = y
                if character == 'P':
                    pitList.append(Pit(screen_x, screen_y))
                    x_pit = x
                    y_pit = y     

pen = Pen()
agent = Agent()
gate = Gate()

x_agent = 0
y_agent = 0
for x in range (len(m)):
    for y in range (len(m[x])):
        character = m[x][y]
        if character == 'A':
            x_agent = x
            y_agent = y
            break

setup_maze(m)

#print(x_agent, y_agent)

solution = findPathOfGame(m, N, (x_agent, y_agent))

def eatGold():
    for g in goldList:
        if agent.is_collision(g):
            agent.point += g.reward
            print("Player Point: ", agent.point)
            g.destroy()
            goldList.remove(g)

def eatGold2():
    for b in bgsList:
        if agent.is_collision(b):
            agent.point += b.reward
            print("Player Point: ", agent.point)
            b.destroy()
            bgsList.remove(b)

# pen.color("orange")
for room in solution:
    (i, j) = room
    # pen.goto(mostLeft + (j *area_1_block), mostTop -(i *area_1_block))
    agent.goto(mostLeft + (j *area_1_block), mostTop -(i *area_1_block))
    eatGold()
    eatGold2()
    pen.stamp()

print("Player Point: ", agent.point + 10)
print("The Agent has escaped!!!")
print("Total move: ", len(solution))