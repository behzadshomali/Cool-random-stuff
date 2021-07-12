from pprint import pprint

'''
Input:
	number of rows
	number of columns
	input table

Input table format:
	-1 19 23 39 39 43 34 37 -1
	30  0  0  0  0  0  0  0 -1
	31  0  0  0  0  0  0  0  9
	42  0  0  0  0  0  0  0  0
	38  0  0  0  0  0  0  0  0
	37  0  0  0  0  0  0  0 -1
	-1  27 0  0  0  0  0  0 -1
	-1  -1 22 0  0  0  0 -1 -1
	-1  -1 16 0  0  0 -1 -1 -1
where:
	-1 indicates unused blocks
	 0 indicates empty blocks
	 NUM indicates the row/column constraints
'''



def initialize_table():
	rows = int(input())
	cols = int(input())
	rows_constraint = {}
	cols_constraint = {}
	table = []

	for row in range(rows):
		table.append(list(map(int, input().split(' '))))

	for i in range(rows):
		for j in range(cols):
			if table[i][j] != -1 and (j == 0 or table[i][j-1] == -1):
				if rows_constraint.get(i, 0) == 0:
					rows_constraint[i] = table[i][j]

			if table[i][j] != -1 and (i == 0 or table[i-1][j] == -1):
				if cols_constraint.get(j, 0) == 0:
					cols_constraint[j] = table[i][j]

    # Distinguishing normal cells
    # (which should be assigned a value)
    # and cells indicating the row/column
    # constraint (sum value)
	for i in range(rows):
		for j in range(cols):
			if table[i][j] != -1 and (j == 0 or table[i][j-1] == -1):
				if rows_constraint[i] == table[i][j]:
					table[i][j] = -1

			if table[i][j] != -1 and (i == 0 or table[i-1][j] == -1):
				if cols_constraint[j] == table[i][j]:
					table[i][j] = -1

	return table, rows_constraint, cols_constraint


def next_free(table):
	rows = len(table)
	cols = len(table[0])

	for i in range(rows):
		for j in range(cols):
			if table[i][j] == 0:
				return i, j

	return -1, -1


def MRV(table):
	rows = len(table)
	cols = len(table[0])

	rows_remaining_count = {}

	for i in range(rows):
		for j in range(cols):
			if table[i][j] == 0:
				rows_remaining_count.setdefault(i, 0)
				rows_remaining_count[i] += 1

	rows_remaining_count = (sorted(rows_remaining_count.items(), key=lambda item: item[1]))

	if len(rows_remaining_count) == 0 or rows_remaining_count[0][1] == 0:
		return -1, -1

	for i in range(len(rows_remaining_count)):
		if table[rows_remaining_count[i][0]] != 0:
			for j, col in enumerate(table[rows_remaining_count[i][0]]):
				if col == 0:
					return rows_remaining_count[i][0], j


def forward_checking(val, x, y, table):
	if val in table[y]:
		return False
	if val in [row[x] for row in table]:
		return False
	return True


def is_valid(table, val, x, y, rows_constraint, cols_constraint):
	rows = len(table)
	cols = len(table[0])

	if not forward_checking(val, x, y, table):
		return False

	row_sum = val
	has_free = 0
	for j in range(cols):
		if table[y][j] != -1:
			row_sum += table[y][j]
		if table[y][j] == 0 and j != x:
			has_free = 1
	if row_sum > rows_constraint[y] or (not has_free and row_sum != rows_constraint[y]):
		return False



	col_sum = val
	has_free = 0
	for row_indx, row in enumerate(table):
		if row[x] != -1:
			col_sum += row[x]
		if row[x] == 0 and row_indx != y:
			has_free = 1
	if col_sum > cols_constraint[x] or (not has_free and col_sum != cols_constraint[x]):
		return False


	return True


def solve_backtrack(table, rows_constraint, cols_constraint):
	y, x = MRV(table)
	if x == -1:
		return True

	elif x != -1 and y != -1:
		for num in range(1,10):
			if is_valid(table, num, x, y, rows_constraint, cols_constraint):
				table[y][x] = num
				if solve_backtrack(table, rows_constraint, cols_constraint):
					return True
				else:
					table[y][x] = 0

		return False


if __name__ == '__main__':
	table, rows_constraint, cols_constraint = initialize_table()
	found = solve_backtrack(table, rows_constraint, cols_constraint)
	if found:
		print('Hooray, we found the solution :)')
		pprint(table)
	else:
		print('Oops, there is no solution :(')