import pygame

import Constants

class Player:
    """A class used to represent a human player."""

    def movement(self, state):
        """Performs a movement.
        
        Params:
        ----------
        board : list of int
            The current board

        Returns
        -------
        int
            The position on the board where performs a movement (0 to 8)
        """
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    current_pos = pygame.mouse.get_pos()

                    for i in range(Constants.NUM_COLUMNS*Constants.NUM_ROWS):
                        num_column = int(i%Constants.NUM_COLUMNS)
                        x = Constants.MARGIN + num_column*(Constants.PART_SIZE + Constants.STICK_WIDTH + 2*Constants.PART_MARGIN)
                        limit_x = x+Constants.PART_SIZE+2*Constants.PART_MARGIN

                        num_row =  int(i/Constants.NUM_ROWS)
                        y = Constants.PLUS + Constants.MARGIN + num_row*(Constants.PART_SIZE + Constants.STICK_WIDTH + 2*Constants.PART_MARGIN)
                        limit_y = y+Constants.PART_SIZE+2*Constants.PART_MARGIN
                        
                        # If player click some valid position
                        if x<current_pos[0] and current_pos[0]<limit_x and y<current_pos[1] and current_pos[1]<limit_y:
                            if self._check_if_position_is_free(i, state): # If the position is free
                                return i


    def _check_if_position_is_free(self, position, board):
        """Check if position on the board is free.
        
        Params:
        ----------
        position : int
            The position to check
        board : list of int
            The current board

        Returns
        -------
        boolean
            True is position is free
        """
        if 0 <= position and position < Constants.NUM_COLUMNS*Constants.NUM_ROWS:
            return board[position] == Constants.EMPTY
        return False