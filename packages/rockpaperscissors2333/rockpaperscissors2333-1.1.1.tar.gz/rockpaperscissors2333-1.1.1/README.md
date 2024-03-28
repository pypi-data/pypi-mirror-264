[![CI / CD](https://github.com/software-students-spring2024/pysong/actions/workflows/build.yaml/badge.svg)](https://github.com/software-students-spring2024/pysong/actions/workflows/build.yaml)
# Rock Paper Scissors Game

A simple, interactive Rock, Paper, Scissors game implemented in Python. This package allows users to play against the computer or simulate a game between two computer-controlled players. The package also includes a scoreboard that the user can reset at will, and a tutorial to teach you how to play.


## Installation

You can install the Rock Paper Scissors game using pip:
```pip install rockpaperscissors2333```

## Usage

To use our game, simply import the package and select a number option from the list that appears!


## Code Examples
[example](https://github.com/ZijieZha0/code-exampl)


## Documentation

This package includes the following functions:

In "_main_.py", the "main" allows you to select an option for what function you want to access in the game. If an invalid option is selected, it will let you know.

In "cli.py":

    A function "play()" for allowing the player to play against the computer. It prompts a user input for their move and provides a computer move, then compares the two and lets you know who won, updating the scoreboard.

    A function "simulate()" for allowing the player to simulate a game between two computer players. It provides two computer moves, and offers the same comparison.

    A function "tutorial()" which includes print statements that explain how the game works to the user.


In "game.py":
    
    A function "determine_winner()" takes in the player's choice and the computer's choice. It completes the logic required for play() to select a winner between the two by returning the winner.

    "generate_computer_choice()" allows for geenration of a random option from the computer between "rock," "paper," and "scissors".

    "update_scoreboard()" takes the winner from determine_winner() and, depending on who it was, adds a win to the scoreboard for either the player or the computer.

    "reset_scoreboard()" clears the scoreboard.

## For the contribution:

You can setup the virtual environment by starting with ```pipenv install```

 And then install all the dependences through ```pipenv install```

Then you could active the virtual environment through ```pipenv shell```

Then you can build and test the packages inside the virtual environment.




## Teammates

Zijie Zhao ([github](https://github.com/ZijieZha0)), Nathan Daniel ([github](https://github.com/WayyGood)), Ellis Pinsky ([github](https://github.com/ellispinsky)), Kevin Li ([github](https://github.com/Kevinli712390))


## PyPI page

[rockpaperscissors2333](https://pypi.org/project/rockpaperscissors2333/)
