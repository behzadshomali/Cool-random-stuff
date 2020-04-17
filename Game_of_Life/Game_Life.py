import random
import time

def draw(world, height, width): # Draw the new generation of world
    # Move the cursor to let new generation
    # of world overwrites the prevoius one
    print("\033[%d;%dH" % (0, 0))
    lives = 0
    for row in range(height):
        for col in range(width):
            if world[row][col]:
                lives += 1
                print("X", end="") # Represents living creature
            else:
                print(".", end="") # Represents dead creatures
        print()
    print("Lives: %04d" %lives)
    return lives

def check_neighbours(world, row, col, width, height): # Check the neighbourhood of the item and count lives creatures
    lives = 0
    if world[(row-1) % height][(col-1) % width]: lives += 1
    if world[(row-1) % height][col]: lives += 1
    if world[(row-1) % height][(col+1) % width]: lives += 1
    if world[(row+1) % height][(col-1) % width]: lives += 1
    if world[(row+1) % height][col]: lives += 1
    if world[(row+1) % height][(col+1) % width]: lives += 1
    if world[row][(col-1) % width]: lives += 1
    if world[row][(col+1) % width]: lives += 1

    return lives

def evolution(world, height, width): # Acording to lives creatures position, makes the new generation
    copy_world = [[False]*width for h in range(height)]
    for row in range(height):
        for col in range(width):
            lives = check_neighbours(world, row, col, width, height)
            if lives > 3:
                copy_world[row][col] = False
            elif world[row][col] and lives > 1:
                copy_world[row][col] = True
            elif lives == 3:
                copy_world[row][col] = True
            elif world[row][col] and lives < 2:
                copy_world[row][col] = False
    return copy_world

def create_glider(world, x, y):
    world[y][x-1] = True
    world[y][x+1] = True
    world[y+1][x] = True
    world[y+1][x+1] = True
    world[y-1][x+1] = True

def create_block(world, x, y):
    world[y][x] = True
    world[y+1][x] = True
    world[y][x+1] = True
    world[y+1][x+1] = True

def create_beacon(world, x, y):
    create_block(world, x, y)
    create_block(world, x+2, y+2)


width = 80
height = 40
world = [[0]*width for h in range(height)]

# Initializing the World
for w in range(width):
    for h in range(height):
        world[h][w] = random.randint(-850, 150) > 0


i = 1
while True:
    live = draw(world, height, width)
    print("Generation: %04d" %i)
    time.sleep(0.5)
    world=evolution(world, height, width)
    i += 1
