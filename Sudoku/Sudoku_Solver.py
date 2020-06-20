import time

def draw(table, delay=0): # Draw the chart
    for y, row in enumerate(table):
        print(" ", end="")
        for x, col in enumerate(row):
            time.sleep(delay)
            if col == 0:
                col = "x" # "x" represents blank cells
            print(col, end =" ", flush=True)
            if x == 2 or x == 5: # Draw "|" to separate the blocks of table
                print("| ", end = "")
        if y == 2 or y == 5:
            print("\n " + "-"*21) # Draw "-" to separate the blocks of table
        else:
            print()

def is_valid(table, x, y, num): # Check if num can be placed at chart[y][x] or not
    square_x = (x//3) * 3
    square_y = (y//3) * 3
    for row in range(square_y, square_y+3):
        for col in range(square_x, square_x+3):
            if table[row][col] == num:
                return False
    if num in table[y][:]:
        return False
    if num in [row[x] for row in table]:
        return False

    return True

def next_free(table): # Return the next blank cell position
    for y, row in enumerate(table):
        for x, item in enumerate(row):
            if item == 0: # Blank cell found
                return x, y
    return -1, -1

def solve(table):
    x, y = next_free(table)
    if x == -1: # No blank cell left, which means it is solved!
        print()
        return True
    else:
        for num in range(1, 10): # Try numbers 1-9 for chart[y][x] and the call "solve()" recursively
            if is_valid(table, x, y, num):
                table[y][x] = num
                if solve(table):
                    return True, table
            table[y][x] = 0
    return False

table = []
for i in range(9):
    row = input()
    table.append(list(map(int, row[:17].split(" "))))

print("\n Initial Table:   ")
draw(table)

if not solve(table):
    print(" The table is not valid! :(")
else:
    print(" The input table has been\
    \n successfully solved!")
    draw(table, 0.1)
    print()