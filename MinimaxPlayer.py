import time as tm

class MinimaxPlayer:
    def __init__(self):
        self.loc = None
        self.rival_loc = None
        self.board = None
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.end_game_states = {"victory": 100, "loose": -100,  "tie": 0, "continue_game": -2}


    def set_game_params(self, board):
        self.board = board
        for i, row in enumerate(board):
            for j, val in enumerate(row):
                if val == 1:
                    self.loc = (i, j)
                elif val == 2:
                    self.rival_loc = (i, j)

    # TODO maybe not use f and use real time threshold instead
    def f(self, leaves, prev_time):
        total_nodes = leaves * 1.5
        time_for_node = prev_time / total_nodes
        extra_leaves = leaves * 3
        extra_time = extra_leaves * time_for_node
        total_time = prev_time + extra_time
        return total_time

    def make_move(self, time_limit): #number of seconds to finish
        d = 1
        iteration_start_time = tm.time()

        leaves = [0]
        move, score = self.minimax(self.loc, 1, d, leaves)
        if move == self.loc:
            return (0,0)

        last_iteration_time = tm.time() - iteration_start_time
        next_evaluated_time = self.f(leaves[0], last_iteration_time)

        time_limit -= last_iteration_time
        while time_limit > next_evaluated_time:
            d += 1
            iteration_start_time = tm.time()
            move, score = self.minimax(self.loc, 1, d, leaves)

            last_iteration_time = tm.time() - iteration_start_time
            time_limit -= last_iteration_time
            next_evaluated_time = self.f(leaves[0], last_iteration_time)

        return move - self.loc

    # returns true is no moves possible
    def g_check_win(self):
        possible_next_locations_me = self.get_succ_moves(self.loc)
        possible_next_locations_rival = self.get_succ_moves(self.rival_loc)
        if len(possible_next_locations_me) != 0:
            if len(possible_next_locations_rival) == 0:
                return True, self.end_game_states["win"]
            else:
                return False, self.end_game_states["continue_game"]
        else:
            if len(possible_next_locations_rival) != 0:
                return True, self.end_game_states["loose"]
            else:
                #TODO check who is the starting player using tile counting
                return True, self.end_game_states["tie"]

    def heuristic(self, leaves):
        # TODO refine the heuristic using these:
        # rival distance to our location using white tiles using BFS?
        # board state: num of white tiles around me

        possible_next_me = len(self.get_succ_moves(self.loc)) # 3
        possible_next_rival = len(self.get_succ_moves(self.rival_loc)) # 2

        return possible_next_me - possible_next_rival

    def update_board(self, action, agent, location):
        # TODO: build board manager
        # TODO use directions instead of locations, then no need to send chosen (parent location)
        # in order to revert

        rival = self.rival_loc
        if action == 1:
            if agent == 1:
                self.board[self.loc[0]][self.loc[1]] = -1
                self.loc = location
                self.board[self.loc[0]][self.loc[1]] = 1
            else:
                self.board[rival[0]][rival[1]] = -1
                self.rival_loc = location
                self.board[rival[0]][rival[1]] = 2
        elif action == -1:
            if agent == 1:
                self.board[self.loc[0]][self.loc[1]] = 1
                self.loc = location
                self.board[location[0]][location[1]] = 0
            else:
                self.board[rival[0]][rival[1]] = 2
                self.rival_loc = location
                self.board[self.rival_loc[0]][self.rival_loc[1]] = 0

    def minimax(self, location, agent, depth, leaves):

        # TODO update the board according to chosen move
        self.update_board(1, agent, location)

        chosen = self.loc

        # checking end of game, it is a leaf
        game_finished, finish_state = self.g_check_win()
        if game_finished:
            leaves[0] += 1
            return chosen, finish_state

        # if reached depth limit - update leaves and return the heuristic score and move
        if depth == 0:
            leaves[0] += 1
            # gets board, and returns value of the current leaf
            return (0,0), self.heuristic(leaves)
        depth -= 1

        # get successors
        children = self.get_succ_moves(location)

        # max player
        if agent == 1:
            cur_max = -float('inf')
            for child in children:
                _, val_of_move = self.minimax(child, 3 - agent, depth, leaves)
                # TODO check if chosen not changing
                self.update_board(-1, agent, chosen)
                if val_of_move > cur_max:
                    chosen = child

                cur_max = max(cur_max, val_of_move)
            return chosen, cur_max

        # min player
        else:
            cur_min = float('inf')
            for child in children:
                _, val_of_move = self.minimax(child, 3 - agent, depth, leaves)
                self.update_board(-1, agent, chosen)
                if val_of_move < cur_min:
                    chosen = child
                cur_min = max(cur_min, val_of_move)
            return chosen, cur_min

    def is_move_valid(self, loc):

        i = loc[0]
        j = loc[1]
        return 0 <= i < self.board.shape[0] and \
               0 <= j < self.board.shape[1] and \
               self.board[loc[0],loc[1]] == 0

    def get_succ_moves(self, location):

        up = (location[0] + 1, location[1])
        down = (location[0] - 1, location[1])
        left = (location[0], location[1] - 1)
        right = (location[0], location[1] + 1)

        moves = []
        moves += [up, down, left, right]

        return list(filter(lambda move: self.is_move_valid(move), moves))

    def set_rival_move(self, loc):
        self.board[loc] = -1

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
