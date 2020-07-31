import pygame
import time
import random
from queue import PriorityQueue, Queue

# Initializing colors
VISITED_COLOR = (128, 255, 0)
PATH_COLOR = (50, 50, 140)
OBSTACLES_COLOR = (140, 140, 140)
ORIGIN_TARGET_COLOR = (0, 0, 5)
BACKGROUND = (204, 230, 255)
LINES_COLOR = (204, 204, 204)
BORDER_COLOR = (81, 81, 81)
NEIGHBORS_COLOR = (217, 217, 38)


class Block:
    def __init__(self, color, x, y, win, canBeEdited=True):
        self.color = color
        self.x = x
        self.y = y
        self.win = win
        self.canBeEdited = canBeEdited
        self.isBlocked = not self.canBeEdited

    def __lt__(self, other):
        return False

    def update_color(self):
        pygame.draw.rect(self.win, self.color, [self.x + 1, self.y + 1, gap - 1, gap - 1])
        pygame.display.update()

    def reset(self, background_color):
        if self.canBeEdited:
            self.isBlocked = False
            self.color = background_color
            self.update_color()

    def update_neighbors(self, table):
        self.neighbors = []
        totalRowsCols = len(table)
        x = self.x // gap
        y = self.y // gap
        if x + 1 < totalRowsCols and not table[y][x + 1].isBlocked:  # RIGHT
            self.neighbors.append(table[y][x + 1])
        if x - 1 > 0 and not table[y][x - 1].isBlocked:  # LEFT
            self.neighbors.append(table[y][x - 1])
        if y + 1 < totalRowsCols and not table[y + 1][x].isBlocked:  # DOWN
            self.neighbors.append(table[y + 1][x])
        if y - 1 > 0 and not table[y - 1][x].isBlocked:  # UP
            self.neighbors.append(table[y - 1][x])
        if y - 1 > 0 and x - 1 > 0 and not table[y - 1][x - 1].isBlocked:  # UP-LEFT
            self.neighbors.append(table[y - 1][x - 1])
        if y - 1 > 0 and x + 1 < totalRowsCols and not table[y - 1][x + 1].isBlocked:  # UP-RIGHT
            self.neighbors.append(table[y - 1][x + 1])
        if y + 1 < totalRowsCols and x - 1 > 0 and not table[y + 1][x - 1].isBlocked:  # DOWN-LEFT
            self.neighbors.append(table[y + 1][x - 1])
        if y + 1 < totalRowsCols and x + 1 < totalRowsCols and not table[y + 1][x + 1].isBlocked:  # DOWN-RIGHT
            self.neighbors.append(table[y + 1][x + 1])


def init_table(win):
    table = []
    for i in range(0, WIDTH, gap):
        table.append([])
        for j in range(0, WIDTH, gap):
            canBeEdited = not (i == 0 or i + gap >= WIDTH or j == 0 or j + gap >= WIDTH)
            block = Block(BACKGROUND, j, i, win, canBeEdited)
            table[i // gap].append(block)
    return table


def init():
    win = pygame.display.set_mode((WIDTH, WIDTH))
    pygame.display.set_caption('Path Finding')
    win.fill(BACKGROUND)
    table = init_table(win)
    draw_grid(win, table)

    return win, table


def draw_grid(win, table):
    for i in range(0, WIDTH, gap):
        pygame.draw.line(win, LINES_COLOR, (0, i), (WIDTH, i))
    for j in range(0, WIDTH, gap):
        pygame.draw.line(win, LINES_COLOR, (j, 0), (j, WIDTH))

    for j in range(0, WIDTH, gap):  # Draw UP-DOWN borders
        time.sleep(0.02)
        table[0][j // gap].color = BORDER_COLOR
        table[0][j // gap].update_color()
        table[-1][-(j + 1) // gap].color = BORDER_COLOR
        table[-1][-(j + 1) // gap].update_color()

    for i in range(0, WIDTH, gap):  # Draw LEFT-RIGHT borders
        time.sleep(0.02)
        table[i // gap][-1].color = BORDER_COLOR
        table[i // gap][-1].update_color()
        table[-(i + 1) // gap][0].color = BORDER_COLOR
        table[-(i + 1) // gap][0].update_color()


def draw_path(origin, target, parents):
    par = parents[target]
    while par != origin:
        par.color = (51, 51, 204)
        par.update_color()
        time.sleep(0.1)
        par = parents[par]


def diagonal_distance(block1, block2):
    #  This approach enables us to move to 8 different directions
    return max(abs(block1.x - block2.x), abs(block1.y - block2.y))


def AStar_find(origin, target):
    open_set = PriorityQueue()
    open_set_members = []  # Holds the blocks which are already in 'open_set'
    close_set = []  # Holds the blocks we've already visited them
    parents = {}  # Holds each block's parent (the block we came from)
    g_score = {block: float('inf') for row in table for block in row}
    f_score = {block: float('inf') for row in table for block in row}

    parents[origin] = -1
    g_score[origin] = 0
    f_score[origin] = diagonal_distance(origin, target)
    open_set.put((f_score[origin], origin))
    open_set_members.append(origin)

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[1]  # Represents the block we are checking now
        for neighbor in current.neighbors:
            if neighbor not in close_set and neighbor not in open_set_members:
                if g_score[current] + 1 < g_score[neighbor]:
                    g_score[neighbor] = g_score[current] + 1
                    parents[neighbor] = current

                if neighbor == target:
                    print('FOUND')
                    draw_path(origin, target, parents)
                    return True

                # Check to be sure not to change color of origin and target
                # then it will indicate where we actually are
                if current != origin and current != target:
                    current.color = PATH_COLOR
                    current.update_color()
                    time.sleep(0.01)
                f_score[neighbor] = g_score[neighbor] + diagonal_distance(neighbor, target)
                open_set.put((f_score[neighbor], neighbor))
                open_set_members.append(neighbor)

                # Check to be sure not to change color of origin and target
                if neighbor != origin and neighbor != target:
                    neighbor.color = NEIGHBORS_COLOR
                    neighbor.update_color()

                # Check to be sure not to change color of origin and target
                # then it will indicate where we've already visited
                if current != origin and current != target:
                	time.sleep(0.02)
                	current.color = VISITED_COLOR
                	current.update_color()

        close_set.append(current)
        open_set_members.remove(current)

    print('NOT FOUND!')
    there_is_no_way(table)
    return False



def BFS_find(origin, target):
    parents = {}
    visited = []
    blocks_queue = Queue()
    parents[origin] = -1
    visited.append(origin)
    blocks_queue.put(origin)
    while not blocks_queue.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = blocks_queue.get()
        if current != origin:  # To avoid changing color of ORIGIN
            current.color = PATH_COLOR
            current.update_color()
        time.sleep(0.02)
        for neighbor in current.neighbors:
            if neighbor not in visited:
                parents[neighbor] = current
                if neighbor == target:
                    print('Found!')
                    draw_path(origin, target, parents)
                    return True

                visited.append(neighbor)
                blocks_queue.put(neighbor)
                neighbor.color = VISITED_COLOR
                neighbor.update_color()
        if current != origin:  # To avoid changing color of ORIGIN
            current.color = VISITED_COLOR
            current.update_color()
        time.sleep(0.02)
    print('Not found!')
    there_is_no_way(table)
    return False

def there_is_no_way(table):  # This method will be called when there is no path between origin and target
    color = (random.randint(0, 220), random.randint(0, 220), random.randint(0, 220))  # Make a random color
    for i in range(1, len(table)//2):
        for j in range(len(table)//2):
            table[1 + j][i].color = color
            table[1 + j][i].update_color()
            table[len(table) - 2 - j][i].color = color
            table[len(table) - 2 - j][i].update_color()

            table[1 + j][len(table) - 1 - i].color = color
            table[1 + j][len(table) - 1 - i].update_color()
            table[len(table) - 2 - j][len(table) - 1 - i].color = color
            table[len(table) - 2 - j][len(table) - 1 - i].update_color()
            time.sleep(0.02)

            color = (random.randint(0, 220), random.randint(0, 220), random.randint(0, 220))


BLOCKS = int(input('Enter number of blocks in each row and column -> '))
WIDTH = int(input('Enter width and height of intended window -> '))
ALGORITHM = input('BFS or A* -> ')

WIDTH = WIDTH // BLOCKS * BLOCKS
gap = WIDTH // BLOCKS
win, table = init()

originIsChosen = False
targetIsChosen = False
isStarted = False
origin_pos = (-1, -1)
target_pos = (-1, -1)

while True:
    time.sleep(0.0000001)  # Make a little delay to avoid CPU overworking
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)

        if pygame.mouse.get_pressed()[0]:  # Left click
            x = (pygame.mouse.get_pos()[0] // gap)
            y = (pygame.mouse.get_pos()[1] // gap)
            if table[y][x].canBeEdited and not isStarted:
                if not originIsChosen:
                    origin_pos = (x, y)
                    table[y][x].color = ORIGIN_TARGET_COLOR
                    origin = table[y][x]
                    table[y][x].update_color()
                    originIsChosen = True
                    continue
                if not targetIsChosen and origin_pos != (x, y):
                    target_pos = (x, y)
                    table[y][x].color = ORIGIN_TARGET_COLOR
                    target = table[y][x]
                    table[y][x].update_color()
                    targetIsChosen = True
                    continue
                if (x, y) not in [target_pos, origin_pos]:
                    table[y][x].color = OBSTACLES_COLOR
                    table[y][x].isBlocked = True
                    table[y][x].update_color()

        if pygame.mouse.get_pressed()[2]:  # Right click
            x = (pygame.mouse.get_pos()[0] // gap)
            y = (pygame.mouse.get_pos()[1] // gap)
            if table[y][x].canBeEdited and not isStarted:
                table[y][x].isBlocked = False
                if origin_pos == (x, y):
                    originIsChosen = False
                if target_pos == (x, y):
                    targetIsChosen = False
                table[y][x].color = BACKGROUND
                table[y][x].update_color()

        if event.type == pygame.KEYDOWN:  # Key presses
            if event.key == pygame.K_SPACE and originIsChosen and \
                    targetIsChosen and not isStarted:  # SPACE_key is pressed
                for row in table:
                    for block in row:
                        if block.canBeEdited:  # There is no need to find neighbors of border blocks
                            block.update_neighbors(table)
                isStarted = True
                if ALGORITHM == 'A*':
                    AStar_find(origin, target)
                elif ALGORITHM == 'BFS':
                    BFS_find(origin, target)
            elif event.key == pygame.K_BACKSPACE:  # Reset everything if BACKSPACE_key is pressed
                targetIsChosen = False
                originIsChosen = False
                isStarted = False
                for row in table:
                    for block in row:
                        block.reset(BACKGROUND)
