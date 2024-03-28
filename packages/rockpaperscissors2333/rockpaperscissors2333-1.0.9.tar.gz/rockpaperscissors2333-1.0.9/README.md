[![CI / CD](https://github.com/software-students-spring2024/pysong/actions/workflows/build.yaml/badge.svg)](https://github.com/software-students-spring2024/pysong/actions/workflows/build.yaml)
# Rock Paper Scissors Game

A simple, interactive Rock, Paper, Scissors game implemented in Python. This package allows users to play against the computer or simulate a game between two computer-controlled players.

## Installation

You can install the Rock Paper Scissors game using pip:
```pip install rockpaperscissors2333```

## Usage

### Play against the computer
To play against the computer, run: play
To simulate a play between a human and computer, run: simulate
To reset the score board, run: reset_scoreboard

### Code Snippet
```python
from rockpaperscissors2333.cli import play, simulate
from rockpaperscissors2333.game import reset_scoreboard

while True:
    print("Welcome to Rock, Paper, Scissors!")
    print("1. Play against the computer")
    print("2. Simulate a game between two players")
    print("3. Reset the scoreboard")
    print("4. Quit")
    choice = input("Enter the number of your choice: ")
    if choice == "1":
        play()
    elif choice == "2":
        simulate()
    elif choice == "3":
        reset_scoreboard()
    elif choice == "4":
        break
    else:
    print("Invalid choice. Please try again.")
```


