f = open("input.txt")
lines = f.readlines()
f.close()


# Part One - Finding possible games with the set below
bag = {"red": 12, "green": 13, "blue": 14}

# Each line is a game
summation = 0
for line in lines:
    is_possible = True
    # The id and the game sets are separated by a colon
    game = line.strip().split(":")
    game_id = int(game[0].split(" ")[1])
    # Each game_set is separated by a semicolon
    game_sets = game[1].split(";")
    for game_set in game_sets:
        # Each class of cubes in a game set is separated by a comma
        cubes = game_set.split(",")
        for cube in cubes:
            # The number and color of the cubes are separated by a space
            cube_arr = cube.split(" ")
            number = int(cube_arr[1])
            color = cube_arr[2]

            #If the cubes don't meet the bag limitations
            if bag[color] < number:
                is_possible = False

    # If the game is possible, add the game id
    if is_possible:
        summation += game_id

print(summation)


# Part 2 - Finding the number of each class of cubes to make the game possible
summation = 0
for line in lines:
    max_colors = {"red": 0, "green": 0, "blue": 0}
    game = line.strip().split(":")
    game_sets = game[1].split(";")
    for game_set in game_sets:
        cubes = game_set.split(",")
        for cube in cubes:
            cube_arr = cube.split(" ")
            number = int(cube_arr[1])
            color = cube_arr[2]

            #Find the number of cubes of a color to make a game possible
            if max_colors[color] < number:
                max_colors[color] = number

    # Finding the product the number of each type of cubes to add to the summation
    summation += max_colors["red"] * max_colors["green"] * max_colors["blue"]

print(summation)
