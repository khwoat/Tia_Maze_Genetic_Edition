"""
Ref: https://www.justintopfer.com/using-genetic-algorithms-to-solve-mazes-in-python/
"""

import turtle
import math
import random
import time

wn = turtle.Screen()
wn.bgcolor("papayawhip")
wn.title("A Maze Game")
wn.setup(1920,1080)

turtle.register_shape("img/tial.gif")
turtle.register_shape("img/tiar.gif")
turtle.register_shape("img/tia1l.gif")
turtle.register_shape("img/tia1r.gif")
turtle.register_shape("img/wall1.gif")
turtle.register_shape("img/wall2.gif")
turtle.register_shape("img/wall3.gif")
turtle.register_shape("img/wall4.gif")
turtle.register_shape("img/road.gif")


MOVE_OPTIONS = ["right", "left", "up", "down"]
PENALTY = 100
NUM_MOVES = 100
NUM_PLAYERS = 50
MUTATION_RATE = 0.5
GENERATION_THRESH = 50
NUM_BEST_MOVES = 20 # more than 0


# ********************************************************************
class Pen(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("white")
        self.penup()
        self.speed(0)


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


class Player(turtle.Turtle):
    num_moves = NUM_MOVES

    def __init__(self, spawn_position, img):
        turtle.Turtle.__init__(self)

        self.color("blue")
        self.penup()
        self.shape(img)

        self.move_list = []
        self.fitness = 0
        self.spawn_position = spawn_position
        self.col = spawn_position[0]
        self.row = spawn_position[1]
        self.prev_coord = (self.row, self.col)

        self.is_hit_wall = False

    """
    Call when start new generation
    """
    def new_generation(self, screen_x, screen_y):
        self.fitness = 0

        self.col = self.spawn_position[0]
        self.row = self.spawn_position[1]
        self.prev_coord = (self.row, self.col)

        self.is_hit_wall = False
        
        self.goto(screen_x, screen_y)

    """
    Move player to specified tile
    """
    def move(self, direction):

        self.showturtle()

        if direction == "right":
            self.col = self.col + 1

            move_to_x = self.xcor() + 100
            move_to_y = self.ycor()

        elif direction == "left":
            self.col = self.col - 1

            move_to_x = self.xcor() - 100
            move_to_y = self.ycor()
            
        elif direction == "up":
            self.row = self.row - 1

            move_to_x = self.xcor()
            move_to_y = self.ycor() + 100

        elif direction == "down":
            self.row = self.row + 1

            move_to_x = self.xcor()
            move_to_y = self.ycor() - 100

        else:
            print("unknown move command")

        self.goto(move_to_x,  move_to_y)

    """
    Checks to see if the move is ok, and if so, moves the player there. If the player already knows that such a move
    would result in hitting a wall, the function moves the player to a new spot that wouldn't hit a wall and
    returns this move
    """
    def check_move(self, maze_array, move, index):

        # Right, Left, Up, Down
        if move == "right":
            new_coord = (self.row, self.col + 1)
        elif move == "left":
            new_coord = (self.row, self.col - 1)
        elif move == "up":
            new_coord = (self.row - 1, self.col)
        elif move == "down":
            new_coord = (self.row + 1, self.col)
        else:
            print(move)
            return

        if maze_array[new_coord[0]][new_coord[1]] == "0" and new_coord != self.prev_coord:
            self.prev_coord = (self.row, self.col)
            self.move(move)
            return False

        elif maze_array[new_coord[0]][new_coord[1]] == "T":
            self.move(move)
            print("Found")
            print("Best path:", self.move_list[:index + 1])
            return True
        
        else:
            # If player hit the wall, find a new coordinate that is not a wall and not the previous move
            self.is_hit_wall = True
            self.destroy()

            next_coord = (-1, -1)
            current_coord = (self.row, self.col)
            while next_coord != self.prev_coord:
                next_coord = random.choice(((current_coord[0], current_coord[1]+1),
                                        (current_coord[0], current_coord[1]-1),
                                        (current_coord[0]-1, current_coord[1]),
                                        (current_coord[0]+1, current_coord[1])))
                
                if (maze_array[next_coord[0]][next_coord[1]] == "0" or 
                    maze_array[next_coord[0]][next_coord[1]] == "T" ) and next_coord != self.prev_coord:
     
                    # Replace the current position with the new position in the move list
                    self.move_list[i] = self.get_move(current_coord, next_coord)
                    return False
            
            self.fitness = PENALTY
            return False

    """
    Gets the appropriate move based on the new and previous coordinates
    """         
    def get_move(self, current_coord, next_coord):
        if next_coord[0] == current_coord[0] and next_coord[1] == current_coord[1] + 1:
            return "right"
        elif next_coord[0] == current_coord[0] and next_coord[1] == current_coord[1] - 1:
            return "left"
        elif next_coord[0] == current_coord[0] + 1 and next_coord[1] == current_coord[1]:
            return "down"
        elif next_coord[0] == current_coord[0] - 1 and next_coord[1] == current_coord[1]:
            return "up"
        else:
            return None
    
    """
    Destroy turtle (image)
    """
    def destroy(self):
        self.goto(2000, 2000)
        self.hideturtle()

"""
Random move
"""
def create_random_moves(turns):
    options = MOVE_OPTIONS
    return random.choices(options, k=turns)

"""
Create first moves list for all player
"""
def create_moves_list(x = NUM_PLAYERS, y = NUM_MOVES):
    moves = []
    for i in range(x):
        moves.append(create_random_moves(y))

    return moves

"""
Calculation for finding fitness value of moves list
"""
def calc_goal_distance(x1, y1, x2, y2, measure="euclidean"):
    if measure=="euclidean":
        goal_dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    elif measure=="manhattan":
        goal_dist = int(abs(abs(x2) - abs(x1)) + abs(abs(y2) - abs(y1)))

    return goal_dist

"""
Crossover moves list between player (that have best moves) with every player
by using uniform crossover
"""
def uniform_crossover(arr1, arr2, p = 0.5):
    assert len(arr1) == len(arr2), "Arrays must have the same length"
    new_arr = []
    for i in range(len(arr1)):
        if random.random() < p:
            new_arr.append(arr1[i])
        else:
            new_arr.append(arr2[i])
    return new_arr

"""
Mutation every move list of all player
"""
def mutate(array):
    if random.random() <= MUTATION_RATE:
        i = random.randint(0, len(array) - 1)

        ## Find new move that is not same as old move
        array[i] = random.choice([a for a in MOVE_OPTIONS if a != array[i]])

        return array
    else:
        return array


"""
Display the maze on screen
"""
def setup_maze(level):
    global start_point
    global goal_point

    for y in range(len(level)):
        for x in range(len(level[y])):
            
            character = level[y][x]
            
            screen_x = -860 + (x*100)
            screen_y = 480 - (y*100)

            if character == "X":
                pen.goto(screen_x, screen_y)
                pen.shape("img/wall1.gif")
                pen.stamp()
            if character == "A":
                pen.goto(screen_x, screen_y)
                pen.shape("img/wall2.gif")
                pen.stamp()
            if character == "B":
                pen.goto(screen_x, screen_y)
                pen.shape("img/wall3.gif")
                pen.stamp()
            if character == "C":
                pen.goto(screen_x, screen_y)
                pen.shape("img/wall4.gif")
                pen.stamp()

            if character == "P":
                start_point = [y, x]
                father_player.goto(screen_x, screen_y)
                # father_player.hideturtle()

            if character == "T":
                goal_point = [y, x]
                Treasure(screen_x, screen_y)

maze = [
    list("XXXBBXXXXXAXXAXXXX"), #0
    list("XPXAAXXXXBBBXXACXX"), #1
    list("X0XCX000000000XXBX"), #2
    list("X0XBX0BBXXXXX0XXBA"), #3
    list("X00XX0XXCABXA0XXBX"), #4
    list("X00000XXXBXXB000AX"), #5
    list("X0XXB0000ACAX0XXXX"), #6
    list("XXXXX0XXXXXXX000XX"), #7
    list("XXXXX00XXBAXXTXXXX"), #8
    list("XXXABBAXXXXXBAXXXX"), #9
]

start_point = [0, 0]
goal_point = [0, 0]

pen = Pen()
father_player = Player(start_point, "img/tiar.gif")
setup_maze(maze)

wn.tracer(0)
## Start position in screen
screen_x = -860 + (start_point[1] * 100)
screen_y = 480 - (start_point[0] * 100)


players_moves = create_moves_list()
players = [Player(start_point, "img/tia1r.gif") for i in range(NUM_PLAYERS)]

for i in range(NUM_PLAYERS):
    players[i].move_list = players_moves[i]
    players[i].new_generation(screen_x, screen_y)

generation = 1
found = False
hit_the_wall = False

## Start
while(found != True and generation <= GENERATION_THRESH):

    print("generation:", generation)

    ## Set value for players in new generation
    for player in players:
        player.new_generation(screen_x, screen_y)

    ## Move players
    for i in range(NUM_MOVES):

        if (found):
            break

        time.sleep(0.05)

        hit_wall_count = 0
        for player in players:

            if (found):
                break

            if player.is_hit_wall == False:
                found = player.check_move(maze, player.move_list[i], i)
            else:
                hit_wall_count += 1
        
        if hit_wall_count == NUM_PLAYERS:
            break
        
        wn.update()


    ## Calculate fitness value for all players
    for player in players:
        fitness = calc_goal_distance(player.row, player.col, goal_point[0], goal_point[1])

        if player.fitness < PENALTY:
            player.fitness = fitness


    players.sort(key=lambda x: x.fitness)
    best_moves_list = [players[x].move_list for x in range(NUM_BEST_MOVES)]

    k = 0  
    if (found != True):
        for player in players:
            
            new_moves = uniform_crossover(best_moves_list[k], player.move_list)
            
            new_moves = mutate(new_moves)

            player.move_list = new_moves

            if k == NUM_BEST_MOVES - 1:
                k = 0
            else:
                k += 1
            
    generation += 1
    print("best_fitness:", players[0].fitness)

if (not found):
    print("Not found. T-T")