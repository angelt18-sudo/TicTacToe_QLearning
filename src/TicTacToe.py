import Constants
from Player import Player

import pygame

class TicTacToe:
    """
    A class used to represent a Tic Tac Toe game.

    Attributes:
    ----------
    board : list of int
        The board of the game. It is a list with 9 elements. Values:
        - 0: there is no part in this position
        - 1: there is a player1 part in this position
        - 2: there is a player2 part in this position
    player1_turn : boolean
        Indicates if it is the player1 turn or not
    movements : int
        Number of moves remaining in the game
    """

    def __init__(self):
        """Initializes a game."""
        self._init_empty_board()

        self.playern1_turn = True
        self.movements = Constants.NUM_COLUMNS*Constants.NUM_ROWS

    def _init_empty_board(self):
        """Initializes the board of the game."""
        self.board = []
        for i in range(0, Constants.NUM_ROWS*Constants.NUM_COLUMNS):
            self.board.append(Constants.EMPTY)  # 0 in all positions

    def get_board(self):
        """Get the board.
        
        Returns
        -------
        list of int
            The board of the game. It is a list with 9 elements. Values:
            - 0: there is no part in this position
            - 1: there is a player1 part in this position
            - 2: there is a player2 part in this position
        """
        return self.board.copy()

    def get_turn(self):
        """Get turn.

        Returns
        -------
        boolean
            Indicates if it is the player1 turn or not
        """
        return self.playern1_turn

    def _check_win(self):
        """Check is some player has won

        Returns
        -------
        boolean
            True if some player has won
        """
        # Horizontal condition
        for row in range(Constants.NUM_ROWS):
            elem = Constants.NUM_ROWS*row
            if self.board[elem] != Constants.EMPTY and self.board[elem] == self.board[elem+1] and self.board[elem] == self.board[elem+2]:
                return True

        # Vertical condition
        for col in range(Constants.NUM_COLUMNS):
            elem = Constants.NUM_COLUMNS
            if self.board[col+elem] != Constants.EMPTY and self.board[col] == self.board[col+elem] and self.board[col] == self.board[col+2*elem]:
                return True

        # Diagonal condition
        if self.board[0] != Constants.EMPTY and self.board[0] == self.board[4] and self.board[0] == self.board[8]:
            return True
        if self.board[2] != Constants.EMPTY and self.board[2] == self.board[4] and self.board[2] == self.board[6]:
            return True

        return False

    def _add_movement_to_board(self, pos, symbol):
        """Add some movement to board.
        
        Params:
        ----------
        pos : int
            The position where adds the part to the board
        symbol : int
            The player that moves (1 or 2)
        """
        self.board[pos] = symbol

    def step(self, action):
        """Performs a movement.
        
        Params:
        ----------
        action : int
            The position to move

        Returns
        -------
        board : list of int
            Returns the current board with the parts
        done : boolean
            Indicates if the game has finished
        reward : int
            Reward of this movement (10 if the player has won, 2 if there is a tie, -10 if the player has lost, 0 in other case)
        info : dict 
            - turn : boolean indicates the next turn
            - winner : int (0 or 1) the player that has won
            - cheat :  boolean indicates if the player has cheated
        """
        self.movements -= 1

        if self.playern1_turn:
            player = Constants.PLAYER1
            other_player = Constants.PLAYER2
        else:
            player = Constants.PLAYER2
            other_player = Constants.PLAYER1

        if self.board[action] == Constants.EMPTY:   # If it is a valid movement
            self._add_movement_to_board(action, player) # Add movement
            cheat = False   # No cheat

            if self._check_win(): # If player has won
                done = True
                winner = player
                reward = Constants.REWARD_WIN
                self.movements = 0
            elif self.movements == 0: # If the movements are over
                done = True
                winner = None
                reward = Constants.REWARD_TIE
            else:
                done = False
                winner = None
                reward = 0

            self.playern1_turn = not self.playern1_turn
        else: # if the player has cheated
            cheat = True
            done = True
            reward = Constants.REWARD_LOST
            winner = other_player
            self.movements = 0

        info = {
            'turn': self.playern1_turn,
            'winner': winner,
            'cheat': cheat
        }

        return self.get_board(), done, reward, info

    def print_board(self):
        """Print the board on the screen."""
        for row in range(Constants.NUM_ROWS):
            for col in range(Constants.NUM_COLUMNS):
                elem = row*Constants.NUM_ROWS + col
                if self.board[elem] == Constants.PLAYER1:
                    value = 'X'
                elif self.board[elem] == Constants.PLAYER2:
                    value = 'O'
                else:
                    value = ' '
                print(value, end='|')
            print()

    def render(self, screen):
        """Render the game (update the GUI of the game).
        
        Params:
        ----------
        screen :
            The screen where draws the game
        """
        # Draws the background and the game
        screen.blit(Constants.BACKGROUND, (0, 0))

        # Draws the parts
        for i, value in enumerate(self.board):
            num_column = int(i%Constants.NUM_COLUMNS)
            x = Constants.MARGIN + Constants.PART_MARGIN + num_column*(Constants.PART_SIZE + Constants.STICK_WIDTH + 2*Constants.PART_MARGIN)

            num_row =  int(i/Constants.NUM_ROWS)
            y = Constants.PLUS + Constants.MARGIN + Constants.PART_MARGIN + num_row*(Constants.PART_SIZE + Constants.STICK_WIDTH + 2*Constants.PART_MARGIN)

            if value == Constants.PLAYER1:
                self.draw_x(x, y, Constants.PART_SIZE, Constants.PART_SIZE, Constants.COLOR_X, screen)
            elif value == Constants.PLAYER2:
                pygame.draw.ellipse(screen, Constants.COLOR_O, (x,y,Constants.PART_SIZE, Constants.PART_SIZE), 10)

        # Draws the sticks
        for stick in range(1,Constants.NUM_COLUMNS):
            x = Constants.MARGIN + stick*(Constants.PART_SIZE + 2*Constants.PART_MARGIN + Constants.STICK_WIDTH) - Constants.STICK_WIDTH
            y = Constants.PLUS + Constants.MARGIN
            largo = Constants.SCREEN_HEIGHT - 2*Constants.MARGIN - Constants.PLUS

            pygame.draw.rect(screen, Constants.COLOR_STICK, (x, y, Constants.STICK_WIDTH, largo), 0)

        # Draws the sticks
        for stick in range(1,Constants.NUM_ROWS):
            y = Constants.PLUS + Constants.MARGIN + stick*(Constants.PART_SIZE + 2*Constants.PART_MARGIN + Constants.STICK_WIDTH) - Constants.STICK_WIDTH
            x = Constants.MARGIN
            largo = Constants.SCREEN_WIDTH - 2*Constants.MARGIN

            pygame.draw.rect(screen, Constants.COLOR_STICK, (x, y, largo, Constants.STICK_WIDTH), 0)

        # Show the turn
        if self.movements > 0:
            x = Constants.SCREEN_WIDTH/2 - 105
            y = Constants.PLUS - 25
            if self.playern1_turn:
                self.draw_x(x, y, 40, 40, Constants.COLOR_X, screen)
            else:
                pygame.draw.ellipse(screen, Constants.COLOR_O, (x,y,40, 40), 8)
            
            x = x + 140
            y = Constants.PLUS
            text = Constants.TURN
            (score_text, title_text_rect) = self._define_text(font=Constants.FONT_GAMES, font_size=28, text_string=text, color=Constants.COLOR_TEXT, 
                pos_x=x, pos_y=y)
            screen.blit(score_text, title_text_rect)

        # Update the screen
        pygame.display.flip()

    def draw_x(self,x,y,width,height,color,screen):
        """Draws the part X.
        
        Params:
        ----------
        x : int
            The position x where the part X be drawn on the screen
        y : int
            The position y where the part X be drawn on the screen
        width : int
            The width of the part X
        height : int
            The height of the part X
        color : string
            The color of the part X. Example: "#b68f40"
        screen :
            The screen where draws the part X
        """

        for i in range(12):
            pygame.draw.aaline(screen,color,(x+i,y),(width+x+i,height+y))  # start_pos(x+thickness,y)---end_pos(width+x+thickness,height+y)
            pygame.draw.aaline(screen,color,(width+x+i,y),(x+i,height+y))  # start_pos(x+width+thickness,y)---end_pos(x+thickness,y+height)
            
    def _define_text(self, font, font_size, text_string, color, pos_x, pos_y):
        """Generates the text to be drawn on the screen.

        Params:
        ----------
        font : string
            The direction of the font to be used for the text. Example: 'fonts/game.ttf'
        font_size : int
            The size of the text
        text_string : string
            The content of the text
        color : string
            The color of the text. Example: "#b68f40"
        pos_x : int
            The position x where the text be drawn on the screen
        pos_y : int
            The position y where the text be drawn on the screen

        Returns
        -------
        (text, text_rect)
            text: texto to be drawn
            text_rect: position of the text
        """
        text = pygame.font.Font(font, font_size).render(text_string, True, color)
        text_rect = text.get_rect(center=(pos_x, pos_y))
        return (text, text_rect)