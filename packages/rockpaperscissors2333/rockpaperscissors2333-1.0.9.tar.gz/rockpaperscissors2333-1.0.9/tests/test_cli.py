# test_cli.py

import pytest
from unittest.mock import patch
from src.rockpaperscissors2333.cli import play, simulate

def test_play_scissors_vs_rock(mocker, capsys):
    mocker_input = mocker.patch('builtins.input', return_value='scissors')
    mocker_generate_computer_choice = mocker.patch('src.rockpaperscissors2333.cli.generate_computer_choice', return_value='rock')

    play()

    captured = capsys.readouterr()
    assert "Computer chose rock" in captured.out
    assert "Computer wins!" in captured.out

def test_play_rock_vs_paper(mocker, capsys):
    mocker_input = mocker.patch('builtins.input', return_value='rock')
    mocker_generate_computer_choice = mocker.patch('src.rockpaperscissors2333.cli.generate_computer_choice', return_value='paper')

    play()

    captured = capsys.readouterr()
    assert "Computer chose paper" in captured.out
    assert "Computer wins!" in captured.out

def test_play_paper_vs_scissors(mocker, capsys):
    mocker_input = mocker.patch('builtins.input', return_value='paper')
    mocker_generate_computer_choice = mocker.patch('src.rockpaperscissors2333.cli.generate_computer_choice', return_value='scissors')

    play()

    captured = capsys.readouterr()
    assert "Computer chose scissors" in captured.out
    assert "Computer wins!" in captured.out

def test_play_both_choose_rock(mocker, capsys):
    mocker_input = mocker.patch('builtins.input', return_value='rock')
    mocker_generate_computer_choice = mocker.patch('src.rockpaperscissors2333.cli.generate_computer_choice', return_value='rock')

    play()

    captured = capsys.readouterr()
    assert "Computer chose rock" in captured.out
    assert "It's a tie!" in captured.out

def test_simulate_scissors_rock_then_rock_paper(mocker, capsys):
    mocker_generate_computer_choice = mocker.patch('src.rockpaperscissors2333.cli.generate_computer_choice', side_effect=['scissors', 'rock'])
    
    simulate()
    
    captured = capsys.readouterr()
    assert "You chose scissors" in captured.out
    assert "Computer chose rock" in captured.out
    assert "Computer wins!" in captured.out

def test_simulate_paper_scissors_then_rock_rock(mocker, capsys):
    mocker_generate_computer_choice = mocker.patch('src.rockpaperscissors2333.cli.generate_computer_choice', side_effect=['paper', 'scissors'])
    
    simulate()
    
    captured = capsys.readouterr()
    assert "You chose paper" in captured.out
    assert "Computer chose scissors" in captured.out
    assert "Computer wins!" in captured.out

def test_simulate_rock_rock_then_rock_rock(mocker, capsys):
    mocker_generate_computer_choice = mocker.patch('src.rockpaperscissors2333.cli.generate_computer_choice', side_effect=['rock', 'rock'])

    simulate()
    
    captured = capsys.readouterr()
    assert "You chose rock" in captured.out
    assert "Computer chose rock" in captured.out
    assert "It's a tie!" in captured.out





