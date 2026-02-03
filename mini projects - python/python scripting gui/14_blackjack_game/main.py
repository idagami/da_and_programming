import blackjack_art_14 as ba
import random


def blackjack():
    """Classical game of blackjack with replacement"""
    print(ba.logo)

    cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]

    user_cards_list = []
    dealer_cards_list = []

    def deal_card():
        """Returns a random card from the deck"""
        return random.choice(cards)

    card = deal_card()
    user_cards_list.append(card)
    card = deal_card()
    user_cards_list.append(card)

    card = deal_card()
    dealer_cards_list.append(card)
    card = deal_card()
    dealer_cards_list.append(card)
    dealer_first_card = dealer_cards_list[0]

    # # option 2 for above and below:
    # for _ in range(2):
    #     # we used _ becuz we dont need to use this variable later. could have been anything.
    #     card = deal_card()
    #     user_cards_list.append(card)
    #     dealer_cards_list.append(card)

    def calculate_score(cards_list):
        """Takes a list of cards and calculates the score from each list"""
        if len(cards_list) == 2 and 11 in cards_list and 10 in cards_list:
            return 0  # 0 represents a blackjack in game
        total = sum(cards_list)
        aces = cards_list.count(11)
        while total > 21 and aces > 0:
            total -= 10  # converting one Ace value from 11 to 1 reduces the total by 10
            aces -= 1
        return total

    # # option 2 for above:
    # def calculate_score(cards_list):
    #     if len(cards_list) == 2 and sum(cards_list) == 21:
    #         return 0 # 0 will represent a blackjack in our game
    #     if 11 in cards_list:
    #         cards_list.remove(11)
    #         cards_list.append(1)
    #     return sum(cards_list)

    user_cards_sum = calculate_score(user_cards_list)
    print(f"User cards: {user_cards_list}, current score: {user_cards_sum}")

    dealer_cards_sum = calculate_score(dealer_cards_list)
    print(f"Dealer's first card: {dealer_first_card}")
    # print(f"Dealer cards: {dealer_cards_list}")

    def winner_is(user_cards_sum, dealer_cards_sum):
        if dealer_cards_sum == 0:
            return "Dealer has Blackjack! Dealer won!"
        elif user_cards_sum == 0:
            return "User has Blackjack! User won!"
        elif user_cards_sum > 21:
            return "Dealer won!"
        elif dealer_cards_sum > 21:
            return "User won!"
        elif user_cards_sum > dealer_cards_sum:
            # also checks if one player has score = 21 (21,15)(19,21)
            return "User won!"
        elif user_cards_sum < dealer_cards_sum:
            return "Dealer won!"
        else:
            return "You have a draw!"

    game_over = False

    if dealer_cards_sum == 0:
        game_over = True
        print(winner_is(user_cards_sum, dealer_cards_sum))
    elif user_cards_sum == 0:
        game_over = True
        print(winner_is(user_cards_sum, dealer_cards_sum))

    while not game_over:
        add_card = input("Type 'y' to get another card, type 'n' to pass: ").lower()
        if add_card == "y":
            card = deal_card()
            user_cards_list.append(card)
            user_cards_sum = calculate_score(user_cards_list)
            print(f"User cards: {user_cards_list}, current score: {user_cards_sum}")
            if user_cards_sum == 0 or user_cards_sum > 21:
                game_over = True
                break
        elif add_card == "n":
            break
        else:
            print("Invalid entry, please only type 'y' or 'n': ")

    if not game_over:
        while dealer_cards_sum != 0 and dealer_cards_sum < 17:
            card = deal_card()
            dealer_cards_list.append(card)
            dealer_cards_sum = calculate_score(dealer_cards_list)

    print(f"Dealer cards: {dealer_cards_list}")

    print(f"Your final hand: {user_cards_list}, final score: {user_cards_sum}")
    print(f"Dealer's final hand: {dealer_cards_list}, final score: {dealer_cards_sum}")

    print(winner_is(user_cards_sum, dealer_cards_sum))


blackjack()

while True:
    again = input("Would you like to play again? Type 'y' or 'n': ").lower()
    if again == "y":
        print("\n" * 50)
        blackjack()
    else:
        print("Thank you and goodbye!")
        break


## Testing examples:
# print(calculate_score([11, 10])) # should return 0 (blackjack)
# print(calculate_score([10, 11])) # should return 0
# print(calculate_score([11, 9, 3])) # 11+9+3=23 → Ace should flip → expected 13
# print(calculate_score([11, 11, 9])) # 11+11+9=31 → flip one Ace → 21 expected
# print(calculate_score([10, 9, 2])) # 21 expected
# print(calculate_score([11, 11, 9])) # should return 21 (Ace flipped once).
# print(calculate_score([11, 9, 3])) # should return 13.
