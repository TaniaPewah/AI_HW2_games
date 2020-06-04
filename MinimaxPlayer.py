class MinimaxPlayer:
    def __init__(self):
        self.loc = None
        self.board = None
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    def set_game_params(self, board):
        self.board = board
        for i, row in enumerate(board):
            for j, val in enumerate(row):
                if val == 1:
                    self.loc = (i, j)
                    break

    def make_move(self, time):  # time parameter is not used, we assume we have enough time.
        return True

    def set_rival_move(self, loc):
        return True


    '''def state_score(self, board, loc):
        return True

    def count_ones(self, board):
        return True'''
