import random

# Global scoreboard
scoreboard = {'player': 0, 'computer': 0}

def determine_winner(player_choice, computer_choice):
    global scoreboard
    if player_choice == computer_choice:
        result = "It's a tie!"
    elif player_choice == "rock":
        if computer_choice == "scissors":
            scoreboard['player'] += 1
            result = "You win!"
        else:
            scoreboard['computer'] += 1
            result = "Computer wins!"
    elif player_choice == "paper":
        if computer_choice == "rock":
            scoreboard['player'] += 1
            result = "You win!"
        else:
            scoreboard['computer'] += 1
            result = "Computer wins!"
    elif player_choice == "scissors":
        if computer_choice == "paper":
            scoreboard['player'] += 1
            result = "You win!"
        else:
            scoreboard['computer'] += 1
            result = "Computer wins!"
    return result

def generate_computer_choice():
    choices = ["rock", "paper", "scissors"]
    return random.choice(choices)

def update_scoreboard(result):
    print(result)
    print(f"Scoreboard: Player {scoreboard['player']}, Computer {scoreboard['computer']}")

def reset_scoreboard():
    global scoreboard
    scoreboard = {'player': 0, 'computer': 0}
    print("Scoreboard has been reset.")

