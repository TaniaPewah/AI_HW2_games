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

        move, score = self.minimax((0, 0), 1, d)
        if move == (0, 0):
            return (0, 0)

        last_iteration_time = tm.time() - iteration_start_time
        next_evaluated_time = self.f(last_iteration_time)

        time_limit -= last_iteration_time
        while time_limit > next_evaluated_time:
            d += 1
            iteration_start_time = tm.time()
            move, score = self.minimax((0, 0), 1, d)

            last_iteration_time = tm.time() - iteration_start_time
            time_limit -= last_iteration_time
            next_evaluated_time = self.f(last_iteration_time)

        return move


    def heuristic(self):
        # TODO refine the heuristic using these:
        # rival distance to our location using white tiles using BFS?
        # board state: num of white tiles around me
        # use self.leaves

        possible_next_me = 0 #len(self.get_succ_moves(self.loc)) # 3
        possible_next_rival = 1 #len(self.get_succ_moves(self.rival_loc)) # 2

        return possible_next_me - possible_next_rival

    def minimax(self, direction, agent, depth):

        # checking end of game, it is a leaf
        game_finished, finish_state = self.board_manager.g_check_win(agent)
        if game_finished:
            self.leaves += 1
            return chosen, finish_state

        # if reached depth limit - update leaves and return the heuristic score and move
        if depth == 0:
            self.leaves += 1
            # gets board, and returns value of the current leaf
            return (0,0), self.heuristic()
        depth -= 1

        # chosen = self.loc
        # get successors TODO return possible directions instead of locations
        children = self.board_manager.get_succ_moves( agent)

        # max player
        if agent == 1:
            cur_max = -float('inf')
            for child in children:
                self.board_manager.update_board(1, agent, child) # 1 = step into
                _, val_of_move = self.minimax(child, 3 - agent, depth)
                self.board_manager.update_board(-1, agent, child) # -1 = step out
                #board.update_board(-1, agent, chosen) TODO remove
                if val_of_move > cur_max:
                    chosen = child

                cur_max = max(cur_max, val_of_move)
            return chosen, cur_max

        # min player agent == 2
        else:
            cur_min = float('inf')
            for child in children:
                self.board_manager.update_board(1, agent, child) # 1 = step into
                _, val_of_move = self.minimax(child, 3 - agent, depth)
                self.board_manager.update_board(-1, agent, child)
                if val_of_move < cur_min:
                    chosen = child
                cur_min = max(cur_min, val_of_move)
            return chosen, cur_min

    def set_rival_move(self, loc):
        self.board_manager.set_rival_loc(loc)

'''
        start = time.time()

        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # find the next agent modulo the number of agents
        next_agent = 1 % gameState.getNumAgents()

        # update the depth if we finished a full round of turns
        # pacmang, ..., last ghost
        if next_agent == 0:
            next_depth = self.depth - 1
        else:
            next_depth = self.depth
        # according to staff we can assume that the game won't be launched with
        # 0 ghosts and with depth=0 therefor next_depth >= 0

        # Choose one of the best actions
        scores = [self.rbMinimax(gameState.generatePacmanSuccessor(action), \
                next_agent, next_depth) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        end = time.time()

        # update meta data
        self.time_total_actions += (end-start)
        self.num_actions += 1

        return legalMoves[chosenIndex]
'''

'''
      
'''

'''def state_score(self, board, loc):
        return True'''

'''def count_ones(self, board):
        counter = 0
        for i, row in enumerate(board):
            for j, val in enumerate(row):
                if val == 1:
                    counter += 1
        return counter'''
