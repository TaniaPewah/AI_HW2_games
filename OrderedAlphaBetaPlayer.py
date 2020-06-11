import time as tm
from BoardManager import *

class OrderedAlphaBetaPlayer:
    def __init__(self):
        self.loc = None
        self.rival_loc = None
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.board_manager = None
        self.leaves = 0
        self.alpha = float("-inf")
        self.beta = float("inf")
        self.immediate_children = []
        self.d = 0

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
        self.d = 1
        iteration_start_time = tm.time()
        start = tm.time() #debug
        move, score = self.minimax(1, self.d)
        if move == (0, 0):
            return (0, 0)

        last_iteration_time = tm.time() - iteration_start_time
        next_evaluated_time = self.board_manager.f(last_iteration_time, self.leaves)

        time_limit -= last_iteration_time
        while time_limit > next_evaluated_time:
            self.d += 1
            # for every d save the scores for all children of that location
            iteration_start_time = tm.time()
            sorted(self.immediate_children, key=lambda child: child[0], reverse=True)
            move, score = self.minimax(1, self.d)

            last_iteration_time = tm.time() - iteration_start_time
            time_limit -= last_iteration_time
            next_evaluated_time = self.board_manager.f(last_iteration_time, self.leaves)

        self.board_manager.my_loc = add(self.board_manager.my_loc, move)
        self.immediate_children = []
        return self.d

    def minimax(self, agent, depth):

        # print("self.d: ", self.d)
        # print("depth: ", depth)
        cur_depth = depth
        # print("cur_depth depth: ", cur_depth)

        chosen = (0, 0)

        # checking end of game, it is a leaf
        # returns 100 and returns (0,0)
        game_finished, finish_state, chosen = self.board_manager.g_check_win(agent)
        if game_finished:
            self.leaves += 1
            return chosen, finish_state


        # if reached depth limit - update leaves and return the heuristic score and move
        if cur_depth == 0:
            self.leaves += 1
            # gets board, and returns value of the current leaf
            evaluated_solution = self.board_manager.heuristic()
            return chosen, evaluated_solution

        # get successors
        children = self.board_manager.get_succ_moves(agent)

        # max player
        if agent == 1:
            cur_max = -float('inf')
            # TODO how to sort the children in min player as well only in
            if cur_depth == self.d and self.d != 1:
                evaluated_children = list(map(lambda x: x[1], self.immediate_children))
                self.immediate_children=[]
            else:
                evaluated_children = children

            for child in evaluated_children:
                self.board_manager.direction = child
                self.board_manager.update_board(1, agent, child) # 1 = step into

                _, val_of_move = self.minimax(3 - agent, cur_depth - 1)
                if cur_depth == self.d:
                    # print("1st checkpoint****************cur_depth: ", cur_depth)
                    self.immediate_children += [(val_of_move, child)]
                self.board_manager.update_board(-1, agent, child) # -1 = step out

                if val_of_move > cur_max:
                    chosen = child
                cur_max = max(cur_max, val_of_move)
                self.alpha = max(cur_max, self.alpha)

                #TODO check returning current child or chosen or else
                if cur_max > self.beta:
                    return child, float("inf")

            return chosen, cur_max

        # min player agent == 2
        else:
            cur_min = float('inf')

            if cur_depth == self.d:
                evaluated_children = self.immediate_children
            else:
                evaluated_children = children

            for child in evaluated_children:
                self.board_manager.direction = child
                self.board_manager.update_board(1, agent, child) # 1 = step into
                _, val_of_move = self.minimax(3 - agent, cur_depth - 1)
                # TODO check if should be here
                if cur_depth == self.d:
                     self.immediate_children += [val_of_move, child]
                self.board_manager.update_board(-1, agent, child)
                if val_of_move < cur_min:
                    chosen = child
                cur_min = max(cur_min, val_of_move)
                self.beta = min(cur_min, self.beta)
                # TODO check returning current child or chosen or else
                if cur_min < self.alpha:
                    return child, float("-inf")

            return chosen, cur_min

    def set_rival_move(self, loc):
        self.board_manager.set_rival_loc(loc)