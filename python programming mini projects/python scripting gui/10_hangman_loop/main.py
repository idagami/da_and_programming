import random
import hangman_art_module_10 as ha
import hangman_words_module_10 as hw

print(ha.logo)

print("The game has started!")
lives = 6
word_list = hw.word_list
chosen_word = random.choice(word_list)

length = len(chosen_word)
blanks = []

for position in range(length):
    blanks.append("_")

## option 2 for above:
# blanks = ""
# for position in range(length):
#   blanks += "_"

blanks_word = "".join(blanks)
print(blanks_word)

game_over = False
correct_letters = []
wrong_letters = set()

while not game_over:
    print(f"Letters used so far: {correct_letters}")
    guess = input("Please enter a letter: ").lower()

    if guess in correct_letters or guess in wrong_letters:
        print(f"Letter '{guess}' was already guessed. Try another.")

    display_list = []

    for each_letter in chosen_word:
        if each_letter == guess:
            display_list.append(guess)
            correct_letters.append(guess)
        elif each_letter in correct_letters:
            display_list.append(each_letter)
        else:
            display_list.append("_")

    ## option 2 for above:
    # display = ""
    # for each_letter in chosen_word:
    #   if each_letter == guess:
    #       display += each_letter
    #   else:
    #       display += "_"

    # print(display_list)

    display_word = "".join(display_list)
    print(display_word)

    if "_" not in display_word:
        game_over = True
        print("********** You won! Congratulations! **********")

    if guess not in chosen_word:
        lives -= 1
        wrong_letters.add(guess)
        print(f"Letter '{guess}' is not correct. You lose a life.")
        if lives == 0:
            game_over = True
            print(f"The correct word was {chosen_word}")
            print("Game over. You lost")

        print(f"Wrong letters entered so far: {wrong_letters}")
        print(ha.stages[lives])
        print(f"Lives left: {lives}")
