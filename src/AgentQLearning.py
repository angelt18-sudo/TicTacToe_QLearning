import random
import Constants
import pickle

class AgentQLearning:
    """
    A class used to represent a AI player based on the qlearning algorithm.

    Attributes:
    ----------
    Q_table : dict
        The q table where it stores the q values.
            - Key: state
            - Value: dict
                - Key: actions
                - Value: value
    """

    def __init__(self):
        """Initializes the q table."""
        self.read_qtable()

    def movement(self, board, greedy=0):
        """Performs a movement.
        
        Params:
        ----------
        board : list of int
            The current board
        greedy : int
            The probability of performing a random movement

        Returns
        -------
        int
            The position on the board where performs a movement (0 to 8)
        """
        state = self._convert_state(board)
        rand = random.uniform(0,1)
        if rand < greedy or not state in self.Q_table:
            return self.random_movement(board)
        return max(self.Q_table[state], key=self.Q_table[state].get)

    def random_movement(self, board):
        """Performs a random movement.
        
        Params:
        ----------
        board : list of int
            The current board

        Returns
        -------
        int
            The position on the board where performs a movement (0 to 8)
        """
        free_positions = self._get_free_positions(board)
        return random.choice(free_positions)

    def _get_free_positions(self, board):
        """Gets the free positions.
        
        Params:
        ----------
        board : list of int
            The current board

        Returns
        -------
        list of int
            List with free positions
        """
        positions = []
        for index, value in enumerate(board):
            if value == Constants.EMPTY:
                positions.append(index)
        return positions

    def get_qvalue(self, board, action):
        """Gets the q value.
        
        Params:
        ----------
        board : list of int
            The current board
        action : int
            The position where place the card

        Returns
        -------
        int
            The q value
        """
        state = self._convert_state(board)
        if not state in self.Q_table:
            return 0
        return self.Q_table[state][action]

    def get_qvalue_max(self, board):
        """Returns the maximum qvalue for a given state (board)
        
        Params:
        ----------
        board : list of int
            The current board

        Returns
        -------
        int
            The maximum qvalue for a given state (board)
        """
        state = self._convert_state(board)
        if not state in self.Q_table:
            return 0
        return max(self.Q_table[state], key=self.Q_table[state].get)

    def update_qvalue(self, value, board, action):
        """Update the qtable with a new qvalue
        
        Params:
        ----------
        value : int
            The new value
        board : list of int
            The current board
        action : int
            The action to be taken
        """
        if not action in self._get_free_positions(board):
            print('Invalid Action: ', action, value)
        
        state = self._convert_state(board)
        
        if not state in self.Q_table:
            positions = self._get_free_positions(board)
            self.Q_table[state] = { i : 0 for i in positions }
            
        self.Q_table[state][action] = value

    def _convert_state(self, board):
        """Converts board to a valid state (string) for use as a dictionary key (qtable).
        
        Params:
        ----------
        board : list of int
            The current board

        Returns
        -------
        str
            The state from the board
        """
        return ''.join(str(x) for x in board)

    def write_qtable(self):
        """Writes the qtable to a file."""
        with open(Constants.QTABLE_FILE, 'wb') as handle:
            pickle.dump(self.Q_table, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def read_qtable(self):
        """Reads the qtable from a file."""
        try:
            with open(Constants.QTABLE_FILE, 'rb') as handle:
                self.Q_table = pickle.load(handle)
        except FileNotFoundError:
            self.Q_table = {}
            print('Error: File could not be read ', Constants.QTABLE_FILE)
        except EOFError:
            self.Q_table = {}
            print('EOFError reading file')
