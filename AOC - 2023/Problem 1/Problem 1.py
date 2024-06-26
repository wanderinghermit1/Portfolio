import re

f = open("input.txt")
lines = f.readlines()
f.close()


# Updating the first and last digits with newly found numerical digits
def gather_num_digits(first_digit, last_digit, idx):
    if line[idx].isdigit():
        if first_digit == "":
            first_digit = line[idx]
        else:
            last_digit = line[idx]

    return first_digit, last_digit


# Updating the first and last digits with newly found word digits
def gather_word_digits(first_digit, last_digit, idx):
    digits = {"one": "1", "two": "2", "three": "3", "four": "4", "five": "5",
              "six": "6", "seven": "7", "eight": "8", "nine": "9"}

    # Searching for word matches
    for digit in digits:
        match = re.search(digit, line[idx:])

        if match is not None:
            position = match.start()
            if position == 0 and first_digit == "":
                first_digit = digits[digit]
            elif position == 0:
                last_digit = digits[digit]

    return first_digit, last_digit


# Part 1 - Calculating sum using numerical digits
summation = 0
for line in lines:
    first_digit = ""
    last_digit = ""

    for i in range(len(line)):
        first_digit, last_digit = gather_num_digits(first_digit, last_digit, i)

    if last_digit == "":
        last_digit = first_digit

    summation += int(first_digit + last_digit)

print(summation)


# Part 2 - Calculating sum using word and numerical digits
summation = 0
for line in lines:
    first_digit = ""
    last_digit = ""
    for i in range(len(line)):
        first_digit, last_digit = gather_num_digits(first_digit, last_digit, i)
        first_digit, last_digit = gather_word_digits(first_digit, last_digit, i)

    if last_digit == "":
        last_digit = first_digit

    summation += int(first_digit + last_digit)

print(summation)
