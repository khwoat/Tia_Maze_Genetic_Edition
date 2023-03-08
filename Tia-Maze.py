import turtle
import math
import time

wn = turtle.Screen()
wn.bgcolor("papayawhip")
wn.title("A Maze Game")
wn.setup(1920,1080)

turtle.register_shape("tial.gif")
turtle.register_shape("tiar.gif")
turtle.register_shape("tia1l.gif")
turtle.register_shape("tia1r.gif")
turtle.register_shape("wall1.gif")
turtle.register_shape("wall2.gif")
turtle.register_shape("wall3.gif")
turtle.register_shape("wall4.gif")
turtle.register_shape("road.gif")
turtle.register_shape("pass.gif")
turtle.register_shape("pass1.gif")

class Pen(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("white")
        self.penup()
        self.speed(0)
        
class PassW(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("pass1.gif")
        self.color("red")
        self.penup()
        self.speed(0)

class Player(turtle.Turtle):
    def __init__(self,r,l):
        turtle.Turtle.__init__(self)
        
        self.color("blue")
        self.penup()
        self.speed(0)
        self.gold = 0
        self.left = l
        self.right = r
        self.shape(r)

    def is_collision(self, other):
        a = self.xcor()-other.xcor()
        b = self.ycor()-other.ycor()
        distance = math.sqrt((a ** 2) + (b ** 2))

        if distance < 5:
            return True
        else:
            return False

    def move(self, b):
        print(b+"\n")
        time.sleep(0.5)
        self.showturtle()
        if b == "up":
            move_to_x = self.xcor()
            move_to_y = self.ycor() + 100
            self.goto(move_to_x,  move_to_y)
        elif b == "down":
            move_to_x = self.xcor()
            move_to_y = self.ycor() - 100
            self.goto(move_to_x,  move_to_y)
        elif b == "left":
            move_to_x = self.xcor() - 100
            move_to_y = self.ycor()
            self.shape(self.left)
            self.goto(move_to_x,  move_to_y)
        elif b == "right":
            move_to_x = self.xcor() + 100
            move_to_y = self.ycor()
            self.shape(self.right)
            self.goto(move_to_x,  move_to_y)

        print((move_to_x,  move_to_y))
            
    def destroy(self):
        self.goto(2000, 2000)
        self.hideturtle()


class Treasure(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape("circle")
        self.color("gold")
        self.penup()
        self.speed(0)
        self.gold = 100
        self.goto(x, y)

    def destroy(self):
        self.goto(2000, 2000)
        self.hideturtle()


    





maze = [
    list("XXXBBXXXXXAXXAXXXX"),
    list("XPXAAXXXXBBBXXACXX"),
    list("X0XCX000000000XXBX"),
    list("X0XBX0BBXXXXX0XXBA"),
    list("X0XXX0XXCABXA0XXBX"),
    list("X0X000XXXBXXB000AX"),
    list("X0XX0XX0XACAX0XXXX"),
    list("X0XX0XX00XXX0000XX"),
    list("X0000000XBAXXTXXXX"),
    list("XXXABBAXXXXXBAXXXX"),
]

treasures = []




def isconnect(a, b):
    i, j = a
    for m, n in zip([i-1, i, i+1, i], [j, j-1, j, j+1]):
        if m == b[0] and n == b[1]:
            return True
    return False
def addPass(y, x):
    screen_x = -860 + (x*100)
    screen_y = 480 - (y*100)
    passW.goto(screen_x, screen_y)
    passW.stamp()

    
def walk(a, b):
    if (a[0]==b[0]):
        if(a[1]==b[1]):
            return "start"
        elif(a[1]==b[1]+1):
            return "left"
        elif(a[1]==b[1]-1):
            return "right"
    else:
        if(a[0]==b[0]+1):
            return "up"
        elif (a[0]==b[0]-1):
            return "down"
stack = []


def setup_maze(level):
    for y in range(len(level)):
        for x in range(len(level[y])):
            
            character = level[y][x]
            
            screen_x = -860 + (x*100)
            screen_y = 480 - (y*100)

            if character == "X":
                pen.goto(screen_x, screen_y)
                pen.shape("wall1.gif")
                pen.stamp()
            if character == "A":
                pen.goto(screen_x, screen_y)
                pen.shape("wall2.gif")
                pen.stamp()
            if character == "B":
                pen.goto(screen_x, screen_y)
                pen.shape("wall3.gif")
                pen.stamp()
            if character == "C":
                pen.goto(screen_x, screen_y)
                pen.shape("wall4.gif")
                pen.stamp()

            if character == "P":
                player.goto(screen_x, screen_y)
                player2.goto(screen_x, screen_y)
                player.hideturtle()
                stack.append([y,x])

            if character == "T":

                treasures.append(Treasure(screen_x, screen_y))
                



pen = Pen()

passW = PassW()
player = Player("tia1r.gif","tia1l.gif")
player2 = Player("tiar.gif","tial.gif")
setup_maze(maze)

i, j = stack[0]


#turtle.listen()
#turtle.onkey(player.go_left,"Left")
#turtle.onkey(player.go_right,"Right")
#turtle.onkey(player.go_up,"Up")
#turtle.onkey(player.go_down,"Down")

wn.tracer(0)


path = []

#print("start ", i,j)
while maze[i][j] != 'T':
    maze[i][j] = '-'
    path.append([i, j])
    #print('path ',path)
    addPass(i,j)
    
    for m, n in zip([i-1, i, i+1, i], [j, j-1, j, j+1]):
        #print(m,n,maze[m][n],end = "...")
        if maze[m][n] == '0' or maze[m][n] == 'T':
            #print("push")
            
            stack.append([m, n])
        #else:
            #print("pass")
    #print("Stack --1\n",stack)
    if len(stack) > 0:
        w = [i, j]
        i, j = stack.pop()
        while(maze[i][j]=="-"):
            i, j = stack.pop()
    else:
        print('cannot exit!')
        break
    #print("Stack --2\n",stack)
    for [I, J] in path[::-1]:
        #print(isconnect([i, j], [I, J]))
       # print([i, j], [I, J])
        if isconnect([i, j], [I, J]):break
        
        w = path.pop()
        #print('path ',path)
        #print(w," back " ,path[-1])
        #print("back of",w,"to",path[-1])
        player.move(walk(w, path[-1]))
        wn.update()
        

        w = path[-1]
    #print("move of",w,"to",i,j)
    player.move(walk(w,[i,j]))
    wn.update()

    if(maze[i][j] == 'T'):
        path.append([i, j])

            

    wn.update()
    
time.sleep(0.5)    
player.destroy()
passW.clearstamps()
wn.update()
passW.shape("pass.gif")
print(path)
x = path[0]
for i in path[1:]:
    player2.move(walk(x,i))
    addPass(x[0],x[1])
    for treasure in treasures:
        if player2.is_collision(treasure):
            player2.gold += treasure.gold
            print("Player Gold: {}".format(player.gold))

            treasure.destroy()
            treasures.remove(treasure)

    wn.update()
    x = i

