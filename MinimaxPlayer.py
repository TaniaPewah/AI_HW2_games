import time as tm
from BoardManager import *

class MinimaxPlayer:
    def __init__(self):
        self.loc = None
        self.rival_loc = None
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.board_manager = None
        self.leaves = 0

    def set_game_params(self, board):
        self.board_manager = BoardManager(board)
        self.board_manager.set_game()

    # TODO maybe not use f and use real time threshold instead
    def f(self, prev_time):
        total_nodes = self.leaves * 1.5
        time_for_node = prev_time / total_nodes
        extra_leaves = self.leaves * 3
        extra_time = extra_leaves * time_for_node
        total_time = prev_time + extra_time
        return total_time

    def make_move(self, time_limit): #number of seconds to finish
        # TODO take care of time calculation
        d = 1
        iteration_start_time = tm.time()

        move, score = self.minimax(1, d)
        if move == (0, 0):
            return (0, 0)

        last_iteration_time = tm.time() - iteration_start_time
        next_evaluated_time = self.f(last_iteration_time)

        time_limit -= last_iteration_time
        #while time_limit > next_evaluated_time:
        while d < 3:
            d += 1
            iteration_start_time = tm.time()
            move, score = self.minimax(1, d)

            last_iteration_time = tm.time() - iteration_start_time
            time_limit -= last_iteration_time
            next_evaluated_time = self.f(last_iteration_time)

        self.board_manager.my_loc = add(self.board_manager.my_loc, move)
        return move


    def minimax(self, agent, depth):

        chosen = (0, 0)

        # checking end of game, it is a leaf
        game_finished, finish_state = self.board_manager.g_check_win(agent)
        if game_finished:
            self.leaves += 1
            return chosen, finish_state

        # if reached depth limit - update leaves and return the heuristic score and move
        if depth == 0:
            self.leaves += 1
            # gets board, and returns value of the current leaf
            evaluated_solution = self.board_manager.heuristic()
            return chosen, evaluated_solution
        #depth -= 1

        # chosen = self.loc
        # get successors TODO return possible directions instead of locations
        children = self.board_manager.get_succ_moves(agent)

        # max player
        if agent == 1:
            cur_max = -float('inf')
            for child in children:
                self.board_manager.direction = child
                self.board_manager.update_board(1, agent, child) # 1 = step into
                _, val_of_move = self.minimax(3 - agent, depth - 1)
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
        self.board_manager.set_rival_loc(loc)

