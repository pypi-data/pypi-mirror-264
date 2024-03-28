import argparse
from .game import determine_winner, generate_computer_choice, update_scoreboard, reset_scoreboard

def play():
    player_choice = input("Choose rock, paper, or scissors: ").lower()
    computer_choice = generate_computer_choice()
    print(f"Computer chose {computer_choice}")
    result = determine_winner(player_choice, computer_choice)
    update_scoreboard(result)

def simulate():
    choice_one = generate_computer_choice()
    choice_two = generate_computer_choice()
    print(f"You chose {choice_one}")
    print(f"Computer chose {choice_two}")
    result = determine_winner(choice_one, choice_two)
    update_scoreboard(result)

def tutorial():
    print("Welcome to Rock, Paper, Scissors!\n")
    print("Rules:")
    print("Rock beats Scissors, Paper beats Rock, Scissors beats Paper! Simple enough!")
    print("Input a number option from the menu to start! Have fun!")


def main():
    parser = argparse.ArgumentParser(description="Play Rock, Paper, Scissors")
    subparsers = parser.add_subparsers(dest="command")
    
    parser_play = subparsers.add_parser('play', help='Play against the computer')
    parser_play.set_defaults(func=play)

    parser_simulate = subparsers.add_parser('simulate', help='Simulate a game between two players')
    parser_simulate.set_defaults(func=simulate)

    parser_reset = subparsers.add_parser('reset', help='Reset the scoreboard')
    parser_reset.set_defaults(func=reset_scoreboard)

    parser_tutorial = subparsers.add_parser('tutorial', help='View tutorial')
    parser_tutorial.set_defaults(func=tutorial)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func()
    else:
        parser.print_help()

