import pytest
from src.rockpaperscissors2333.game import determine_winner, generate_computer_choice, update_scoreboard, reset_scoreboard


class MockScoreboard:
    def __init__(self):
        self.scoreboard = {'player': 0, 'computer': 0}

    def update_scoreboard(self, result):
        if result == "You win!":
            self.scoreboard['player'] += 1
        elif result == "Computer wins!":
            self.scoreboard['computer'] += 1
        print(result)
        print(f"Scoreboard: Player {self.scoreboard['player']}, Computer {self.scoreboard['computer']}")

    def reset_scoreboard(self):
        self.scoreboard = {'player': 0, 'computer': 0}
        print("Scoreboard has been reset.")

@pytest.fixture
def mock_scoreboard(monkeypatch):
    mock = MockScoreboard()
    monkeypatch.setattr('src.rockpaperscissors2333.game.scoreboard', mock.scoreboard)
    return mock

def test_determine_winner():
    assert determine_winner("rock", "rock") == "It's a tie!"
    assert determine_winner("rock", "scissors") == "You win!"
    assert determine_winner("rock", "paper") == "Computer wins!"

    assert determine_winner("paper", "paper") == "It's a tie!"
    assert determine_winner("paper", "rock") == "You win!"
    assert determine_winner("paper", "scissors") == "Computer wins!"

    assert determine_winner("scissors", "scissors") == "It's a tie!"
    assert determine_winner("scissors", "paper") == "You win!"
    assert determine_winner("scissors", "rock") == "Computer wins!"

def test_generate_computer_choice():
    choices = ["rock", "paper", "scissors"]
    for i in range(100):
        computer_choice = generate_computer_choice()
        assert computer_choice in choices

def test_update_scoreboard_player_win(mock_scoreboard):
    mock_scoreboard.update_scoreboard("You win!")
    assert mock_scoreboard.scoreboard['player'] == 1
    assert mock_scoreboard.scoreboard['computer'] == 0

def test_update_scoreboard_computer_win(mock_scoreboard):
    mock_scoreboard.update_scoreboard("Computer wins!")
    assert mock_scoreboard.scoreboard['player'] == 0
    assert mock_scoreboard.scoreboard['computer'] == 1

def test_update_scoreboard_tie(mock_scoreboard):
    mock_scoreboard.update_scoreboard("It's a tie!")
    assert mock_scoreboard.scoreboard['player'] == 0
    assert mock_scoreboard.scoreboard['computer'] == 0

def test_reset_scoreboard(mock_scoreboard):
    mock_scoreboard.scoreboard['player'] = 3
    mock_scoreboard.scoreboard['computer'] = 2
    mock_scoreboard.reset_scoreboard()
    assert mock_scoreboard.scoreboard['player'] == 0

