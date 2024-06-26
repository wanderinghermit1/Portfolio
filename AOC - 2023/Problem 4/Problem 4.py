import collections


# Building the winning number and numbers on hand for each line
def build_numbers(line):
    # A card has the card name and the numbers
    card = line.split(":")[1]
    card_name = line.split(":")[0]
    card_name = " ".join(card_name.split())

    card_idx = int(card_name.split(" ")[1])

    # The numbers can be split in to the winning numbers and the ones on hand
    card_arr = card.split("|")
    winning_numbers = card_arr[0]
    numbers_on_hand = card_arr[1]

    winning_numbers = " ".join(winning_numbers.split())
    numbers_on_hand = " ".join(numbers_on_hand.split())

    #Splitting into individual numbers
    winning_numbers_arr = winning_numbers.split(" ")
    numbers_on_hand_arr = numbers_on_hand.split(" ")

    return winning_numbers_arr, numbers_on_hand_arr, card_idx


# Reading file
f = open("input.txt")
lines = f.readlines()
f.close()


# Part 1
summation = 0
for line in lines:
    winning_numbers_arr, numbers_on_hand_arr, _ = build_numbers(line)

    # Retrieving the count of the winning numbers
    count = 0
    for win_num in winning_numbers_arr:
        if win_num in numbers_on_hand_arr:
            count += 1

    if count > 0:
        summation += 2**(count - 1)

print(summation)


# Part 2
summation = 0
scratch_cards = collections.defaultdict(int)

for line in lines:
    winning_numbers_arr, numbers_on_hand_arr, card_idx = build_numbers(line)

    count = 0
    for win_num in winning_numbers_arr:
        if win_num in numbers_on_hand_arr:
            count += 1

    #Getting the count of scratch cards
    scratch_cards[card_idx] += 1
    for i in range(scratch_cards[card_idx]):
        for j in range(card_idx + 1, card_idx + count + 1):
            scratch_cards[j] += 1

for card in scratch_cards:
    summation += scratch_cards[card]

print(summation)
