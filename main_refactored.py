from tkinter import Tk, Canvas
import numpy as np

SIZE_OF_BOARD = 600
SYMBOL_SIZE = (SIZE_OF_BOARD / 3 - SIZE_OF_BOARD / 8) / 2
SYMBOL_THICKNESS = 50
SYMBOL_X_COLOR = '#EE4035'
SYMBOL_O_COLOR = '#0492CF'
GREEN_COLOR = '#7BC043'

class TicTacToe():
    """
    The game of Tic Tac Toe
    """
    def __init__(self):
        """
        Initialization Functions:
        """
        self.window = Tk()
        self.window.title('Tic-Tac-Toe')
        self.canvas = Canvas(self.window, width=SIZE_OF_BOARD, height=SIZE_OF_BOARD)
        self.canvas.pack()
        # Input from user in form of clicks
        self.window.bind('<Button-1>', self.click)

        self.initialize_board()
        self.player_x_turns = True
        self.board_status = np.zeros(shape=(3, 3))

        self.player_x_starts = True
        self.reset_board = False
        self.game_over = False
        self.tie = False
        self.x_wins = False
        self.o_wins = False

        self.x_score = 0
        self.o_score = 0
        self.tie_score = 0

    def mainloop(self):
        """
        For repetition of the game
        """
        self.window.mainloop()

    def initialize_board(self):
        """
        Game board initialization
        """
        for i in range(2):
            self.canvas.create_line((i+1)*SIZE_OF_BOARD/3, 0, (i+1)*SIZE_OF_BOARD/3, SIZE_OF_BOARD)

        for i in range(2):
            self.canvas.create_line(0, (i+1)* SIZE_OF_BOARD/3, SIZE_OF_BOARD, (i+1)*SIZE_OF_BOARD/3)

    def play_again(self):
        """
        Initialization of a new game
        """
        self.initialize_board()
        self.player_x_starts = not self.player_x_starts
        self.player_x_turns = self.player_x_starts
        self.board_status = np.zeros(shape=(3,3))

    def draw_o(self, logical_position):
        """"
        Drawing Functions
        """
        # logical_position is the grid value on the board
        # grid_position is the actual pixel values of the center of the grid
        logical_position = np.array(logical_position)
        grid_position = self.convert_logical_to_grid_position(logical_position)
        self.canvas.create_oval(grid_position[0]-SYMBOL_SIZE, grid_position[1]-SYMBOL_SIZE,
                                grid_position[0]+SYMBOL_SIZE, grid_position[1]+SYMBOL_SIZE,
                                width=SYMBOL_THICKNESS, outline=SYMBOL_O_COLOR)

    def draw_x(self, logical_position):
        """"
        Drawing Functions
        """
        grid_position = self.convert_logical_to_grid_position(logical_position)
        self.canvas.create_line(grid_position[0]-SYMBOL_SIZE, grid_position[1]-SYMBOL_SIZE,
                                grid_position[0]+SYMBOL_SIZE, grid_position[1]+SYMBOL_SIZE,
                                width=SYMBOL_THICKNESS, fill=SYMBOL_X_COLOR)
        self.canvas.create_line(grid_position[0]-SYMBOL_SIZE, grid_position[1]+SYMBOL_SIZE,
                                grid_position[0]+SYMBOL_SIZE, grid_position[1]-SYMBOL_SIZE,
                                width=SYMBOL_THICKNESS, fill=SYMBOL_X_COLOR)

    def display_game_over(self):
        """
        UI for when the game is finished
        """
        if self.x_wins:
            self.x_score += 1
            text = 'Winner: Player 1 (X)'
            color = SYMBOL_X_COLOR
        elif self.o_wins:
            self.o_score += 1
            text = 'Winner: Player 2 (O)'
            color = SYMBOL_O_COLOR
        else:
            self.tie_score += 1
            text = 'Its a tie'
            color = 'gray'

        self.canvas.delete("all")
        self.canvas.create_text(SIZE_OF_BOARD/2, SIZE_OF_BOARD/3, font="cmr 60 bold",
                                fill=color, text=text)

        score_text = 'Scores \n'
        self.canvas.create_text(SIZE_OF_BOARD/2, 5*SIZE_OF_BOARD/8, font="cmr 40 bold",
                                fill=GREEN_COLOR, text=score_text)

        score_text = 'Player 1 (X): ' + str(self.x_score) + '\n'
        score_text += 'Player 2 (O): ' + str(self.o_score) + '\n'
        score_text += 'Tie: ' + str(self.tie_score)
        self.canvas.create_text(SIZE_OF_BOARD/2, 3*SIZE_OF_BOARD/4, font="cmr 30 bold",
                                fill=GREEN_COLOR, text=score_text)
        self.reset_board = True

        score_text = 'Click to play again \n'
        self.canvas.create_text(SIZE_OF_BOARD/2, 15*SIZE_OF_BOARD/16, font="cmr 20 bold",
                                fill="gray", text=score_text)

    @staticmethod
    def convert_logical_to_grid_position(logical_position):
        """
        Logical Function
        """
        logical_position = np.array(logical_position, dtype=int)
        return (SIZE_OF_BOARD / 3) * logical_position + SIZE_OF_BOARD / 6

    @staticmethod
    def convert_grid_to_logical_position(grid_position):
        """
        Logical Function
        """
        grid_position = np.array(grid_position)
        return np.array(grid_position // (SIZE_OF_BOARD / 3), dtype=int)

    def is_grid_occupied(self, logical_position):
        """
        Checks if the grid is already occupied or not
        """
        if self.board_status[logical_position[0]][logical_position[1]] == 0:
            return False
        return True

    def is_winner(self, player):
        """
        Checks which player is the winner of the game
        """
        player = -1 if player == 'X' else 1

        # Three in a row
        for i in range(3):
            if self.board_status[i][0]==self.board_status[i][1]==self.board_status[i][2]==player:
                return True
            if self.board_status[0][i]==self.board_status[1][i]==self.board_status[2][i]==player:
                return True

        # Diagonals
        if self.board_status[0][0]==self.board_status[1][1]==self.board_status[2][2]==player:
            return True

        if self.board_status[0][2]==self.board_status[1][1]==self.board_status[2][0]==player:
            return True

        return False

    def is_tie(self):
        """
        Checks if the result of a game is a tie
        """
        rows = np.where(self.board_status == 0)
        tie = False
        if len(rows) == 0:
            tie = True
        return tie

    def is_gameover(self):
        """
        Either someone wins or all grid occupied
        """
        self.x_wins = self.is_winner('X')
        if not self.x_wins:
            self.o_wins = self.is_winner('O')

        if not self.o_wins:
            self.tie = self.is_tie()

        game_over = self.x_wins or self.o_wins or self.tie

        if self.x_wins:
            print('X wins')
        if self.o_wins:
            print('O wins')
        if self.tie:
            print('Its a tie')

        return game_over


    def click(self, event):
        """
        Clicks
        """
        grid_position = [event.x, event.y]
        logical_position = self.convert_grid_to_logical_position(grid_position)

        if not self.reset_board:
            if self.player_x_turns:
                if not self.is_grid_occupied(logical_position):
                    self.draw_x(logical_position)
                    self.board_status[logical_position[0]][logical_position[1]] = -1
                    self.player_x_turns = not self.player_x_turns
            else:
                if not self.is_grid_occupied(logical_position):
                    self.draw_o(logical_position)
                    self.board_status[logical_position[0]][logical_position[1]] = 1
                    self.player_x_turns = not self.player_x_turns

            # Check if game is concluded
            if self.is_gameover():
                self.display_game_over()
                # print('Done')
        else:  # Play Again
            self.canvas.delete("all")
            self.play_again()
            self.reset_board = False

game_instance = TicTacToe()
game_instance.mainloop()
