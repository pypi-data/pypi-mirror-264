[![CI / CD](https://github.com/software-students-spring2024/pysong/actions/workflows/build.yaml/badge.svg)](https://github.com/software-students-spring2024/pysong/actions/workflows/build.yaml)
# Rock Paper Scissors Game

A simple, interactive Rock, Paper, Scissors game implemented in Python. This package allows users to play against the computer or simulate a game between two computer-controlled players. The package also includes a scoreboard that the user can reset at will, and a tutorial to teach you how to play.


## How to use

You can install the package using pip:
```pip install rockpaperscissors2333```

Then import the file from the package by using:

```from rockpaperscissors2333.cli import play, simulate, tutorial```

```from rockpaperscissors2333.game import reset_scoreboard```

And then you could use these function to play rock paper scissors with computer or just simulate a play.

Code Snippet:
```python
from rockpaperscissors2333.cli import play, simulate, tutorial
from rockpaperscissors2333.game import reset_scoreboard
while True:
        print("Welcome to Rock, Paper, Scissors!")
        print("1. Play against the computer")
        print("2. Simulate a game between two players")
        print("3. Reset the scoreboard")
        print("4. View tutorial")
        print("5. Quit")
        choice = input("Enter the number of your choice: ")
        if choice == "1":
            play()
        elif choice == "2":
            simulate()
        elif choice == "3":
            reset_scoreboard()
        elif choice == "4":
            tutorial()
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")   
```

## Code Examples
[example](https://github.com/ZijieZha0/code-example)


## Documentation

This package includes the following functions:

In "_main_.py", the "main" allows you to select an option for what function you want to access in the game. If an invalid option is selected, it will let you know.

In "cli.py":

```python
def play(): 
    """
    Function for allowing the player to play against the computer. 
    It prompts a user input for their move and provides a computer move, 
    then compares the two and lets you know who won, updating the scoreboard.
    """

def simulate(): 
    """
    Function for allowing the player to simulate a game between two computer players. 
    It provides two computer moves, and offers the same comparison.
    """

def tutorial(): 
    """
    Function which includes print statements that explain how the game works to the user.
    """
```


In "game.py":

```python   
def determine_winner(player_choice, computer_choice): 
    """
    A function that determines the winner between the player's choice and the computer's choice.
    
    Args:
        player_choice (str): The player's choice ("rock", "paper", or "scissors").
        computer_choice (str): The computer's choice ("rock", "paper", or "scissors").
    
    Returns:
        str: The winner of the game ("player", "computer", or "tie").
    """

def generate_computer_choice(): 
    """
    Function to generate a random option from the computer between "rock," "paper," and "scissors".
    
    Returns:
        str: The computer's random choice ("rock", "paper", or "scissors").
    """

def update_scoreboard(winner): 
    """
    Function to update the scoreboard based on the winner.
    
    Args:
        winner (str): The winner of the game ("player", "computer", or "tie").
    """

def reset_scoreboard(): 
    """
    Function to clear the scoreboard.
    """
```

## For the contribution:

You can setup the virtual environment by starting with ```pipenv install```

And then install all the dependences through ```pipenv install```

Then you could active the virtual environment through ```pipenv shell```

Then you can build and test the packages inside the virtual environment.




## Teammates

Zijie Zhao ([github](https://github.com/ZijieZha0)), Nathan Daniel ([github](https://github.com/WayyGood)), Ellis Pinsky ([github](https://github.com/ellispinsky)), Kevin Li ([github](https://github.com/Kevinli712390))


## PyPI page

[rockpaperscissors2333](https://pypi.org/project/rockpaperscissors2333/)
