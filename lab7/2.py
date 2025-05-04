import math

def alphabeta(cards, left, right, maximizing_player, alpha, beta):
    if left > right:
        return 0

    if maximizing_player:
        # Max's turn: maximize score
        take_left = cards[left] + alphabeta(cards, left + 1, right, False, alpha, beta)
        take_right = cards[right] + alphabeta(cards, left, right - 1, False, alpha, beta)
        value = max(take_left, take_right)
        alpha = max(alpha, value)
        if beta <= alpha:
            return value
        return value
    else:
        if cards[left] < cards[right]:
            return alphabeta(cards, left + 1, right, True, alpha, beta)
        else:
            return alphabeta(cards, left, right - 1, True, alpha, beta)

def max_turn(cards):
    left_val = cards[0]
    right_val = cards[-1]

    score_if_left = left_val + alphabeta(cards, 1, len(cards)-1, False, -math.inf, math.inf)
    score_if_right = right_val + alphabeta(cards, 0, len(cards)-2, False, -math.inf, math.inf)

    if score_if_left >= score_if_right:
        return cards.pop(0)
    else:
        return cards.pop(-1)

def min_turn(cards):
    if cards[0] < cards[-1]:
        return cards.pop(0)
    else:
        return cards.pop(-1)

def play_game(cards):
    max_score = 0
    min_score = 0
    turn = 'Max'

    while cards:
        print(f"Remaining cards: {cards}")
        if turn == 'Max':
            chosen = max_turn(cards)
            max_score += chosen
            print(f"Max picks: {chosen}")
            turn = 'Min'
        else:
            chosen = min_turn(cards)
            min_score += chosen
            print(f"Min picks: {chosen}")
            turn = 'Max'

    print("\nFinal Scores:")
    print(f"Max's Score: {max_score}")
    print(f"Min's Score: {min_score}")
    if max_score > min_score:
        print("Max wins!")
    elif max_score < min_score:
        print("Min wins!")
    else:
        print("It's a draw!")

cards = [1,3,5,7,9,11]
play_game(cards)
