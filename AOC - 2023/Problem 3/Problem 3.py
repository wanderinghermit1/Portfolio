# Directions going counterclockwise from East
directions = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
filename = "input.txt"


# Finds either end of a number
def find_end(pos, is_left):
    curr_pos = pos.copy()
    increment = 1
    if is_left:
        increment = -1

    the_range = 0
    curr_pos[1] += increment
    curr_digit = engine[curr_pos[0]][curr_pos[1]]
    while curr_pos[1] >= 0 and curr_digit.isdigit():
        the_range += 1
        curr_pos[1] += increment
        curr_digit = engine[curr_pos[0]][curr_pos[1]]

    return the_range


# Reading the file
f = open(filename)
engine = f.readlines()
f.close()


# Part 1 - Taking the sum of the part numbers in the engine
symbols = ["+", "-", "#", "@", "$", "%", "&", "/", "=", "*"]
# Getting a global map of the numbers
number_map = set()
summation = 0
# Getting the position of the symbols
for i in range(len(engine)):
    for j in range(len(engine[i])):
        if engine[i][j] in symbols:
            # Checking each direction for digits
            for direction in directions:
                # When finding a number, check both ends to get full number
                if engine[i + direction[0]][j + direction[1]].isdigit():
                    pos = [i + direction[0], j + direction[1]]

                    left = find_end(pos, 1)
                    right = find_end(pos, 0)

                    # If number has not been encountered for
                    if tuple(pos) not in number_map:
                        number = int(engine[pos[0]][pos[1] - left: pos[1] + right + 1])
                        summation += number
                        for col_pos in range(pos[1] - left, pos[1] + right + 1):
                            number_map.add((pos[0], col_pos))

print(summation)


# Part 2 - Finding the gears
summation = 0
for i in range(len(engine)):
    for j in range(len(engine[i])):
        # Only numbers adjacent to the position is applicable
        positions = set()
        numbers = []
        if engine[i][j] == "*":
            for direction in directions:
                if engine[i + direction[0]][j + direction[1]].isdigit():
                    pos = [i + direction[0], j + direction[1]]

                    left = find_end(pos, 1)
                    right = find_end(pos, 0)

                    if tuple(pos) not in positions:
                        number = int(engine[pos[0]][pos[1] - left: pos[1] + right + 1])
                        numbers.append(number)
                        for col_pos in range(pos[1] - left, pos[1] + right + 1):
                            positions.add((pos[0], col_pos))

        # Check if there are exactly two numbers
        if len(numbers) == 2:
            summation += numbers[0]*numbers[1]

print(summation)