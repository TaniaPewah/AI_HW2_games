import time as tm
from BoardManager import *

class MinimaxPlayer:
    def __init__(self):
        self.loc = None
        self.rival_loc = None
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.board_manager = None
        self.leaves = 0
        self.threshold = 0.2
        self.time_limit = None
        self.move = None
        self.times_up = 0
        self.first_player = 0

    def set_game_params(self, board):
        self.board_manager = BoardManager(board)
        self.board_manager.set_game()


    def make_move(self, time_limit): #number of seconds to finish

        if not self.first_player:
            self.first_player = 1

        print( "first player: ", str(self.first_player))
        # TODO take care of time calculation
        d = 1

        self.start_move_time = tm.time()
        self.time_limit = time_limit
        self.move, score = self.minimax(1, d)
        if self.move == (0, 0):
            return (0, 0)

        #next_evaluated_time = self.board_manager.f(last_iteration_time, self.leaves)
        time = tm.time()
        while time - self.start_move_time < self.time_limit - self.threshold:
            d += 1
            move, score = self.minimax(1, d)
            if not self.times_up:
                self.move = move
            time = tm.time()

        self.board_manager.my_loc = add(self.board_manager.my_loc, self.move)
        return self.move

    def minimax(self, agent, depth):

        chosen = (0, 0)

        time = tm.time()
        if (time - self.start_move_time) > (self.time_limit - self.threshold):
            self.times_up = True
            if agent == 1:
                return self.move, float('inf')
            else:
                return self.move, -float('inf')

        # checking end of game, it is a leaf
        game_finished, finish_state, chosen = self.board_manager.g_check_win(agent)
        if game_finished:
            self.leaves += 1
            return chosen, finish_state

        # if reached depth limit - update leaves and return the heuristic score and move
        if depth == 0:
            self.leaves += 1
            # gets board, and returns value of the current leaf
            evaluated_solution = self.board_manager.heuristic()
            return chosen, evaluated_solution

        # get successors
        children = self.board_manager.get_succ_moves(agent)

        # max player
        if agent == 1:
            cur_max = -float('inf')
            for child in children:
                self.board_manager.direction = child
                self.board_manager.update_board(1, agent, child) # 1 = step into
                _, val_of_move = self.minimax(3 - agent, depth - 1, )
                self.board_manager.update_board(-1, agent, child) # -1 = step out
                if val_of_move > cur_max:
                    chosen = child
                cur_max = max(cur_max, val_of_move)
            return chosen, cur_max

        # min player agent == 2
        else:
            cur_min = float('inf')
            for child in children:
                self.board_manager.direction = child
                self.board_manager.update_board(1, agent, child) # 1 = step into
                _, val_of_move = self.minimax(3 - agent, depth - 1)
                self.board_manager.update_board(-1, agent, child)
                if val_of_move < cur_min:
                    chosen = child
                cur_min = max(cur_min, val_of_move)
            return chosen, cur_min

    def set_rival_move(self, loc):
        if not self.first_player:
            self.first_player = 2
        self.board_manager.set_rival_loc(loc)