import sys
from game_logic.game_logic_blackjack import Hand, BlackJackGame

def place_bet(money: int):
    while True:
        try:
            print(f"Money: {money}")
            action = input("Enter your bet or (Q)uit: ").strip().upper()
            if action == "Q":
                sys.exit(0)
            bet = int(action)
            if bet <= 0 or bet > money:
                print("Invalid bet.")
                continue
            return bet
        except ValueError:
            print("Please enter a number.")

def get_action( player_hand: Hand, can_double_down: bool):
    actions = ['S', 'H']
    if can_double_down:
        actions.append('D')
    while True:
        if can_double_down:
            print(f'(S)tand, (H)it or (D)ouble Down. Hand value: {player_hand.value()}')
        else:
            print(f'(S)tand or (H)it. Hand value: {player_hand.value()}')
        action = input('> ').upper()
        if action not in actions:
            print('Wrong action')
            continue
        return action
    
def show_hand( label: str, hand: Hand, hidden= False):
    print(f'{label}: ', end='')
    if hidden:
        print(f'[{hand.cards[0]}, ??]')
    else:
        print(", ".join(str(card) for card in hand.cards), f"→ {hand.value()}")

game = BlackJackGame(10000)

while game.money > 0:
    bet = place_bet(game.money)
    game.start_round(bet)

    show_hand('Player', game.player_hand)
    show_hand('Dealer', game.dealer_hand, hidden= True)

    while game.player_hand.value() < 21:
        action = get_action(game.player_hand, game.can_double_down())

        if action == 'H':
            card = game.player_hit()
            print(f'New card: {str(card)}')
        elif action == 'S':
            break
        elif action == 'D':
            game.double_down()
            card = game.player_hit()
            print(f'Double Down, new card: {str(card)}')
            break

        show_hand('Player', game.player_hand)
        show_hand('Dealer', game.dealer_hand, hidden= True)

    game.dealer_play()
    result = game.stop_round()

    print('\n-----------')
    show_hand('Player', game.player_hand)
    show_hand('Dealer', game.dealer_hand)
    print(f'\nResult: {result}')
    print('-----------\n')

print('You went bankrupt, better luck next time!')