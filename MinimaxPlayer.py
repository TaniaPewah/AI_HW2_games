import time as tm

class MinimaxPlayer:
    def __init__(self):
        self.loc = None
        self.rival_loc = None
        self.board = None
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.end_game_states = {"victory": 1, "loose": -1,  "tie": 0, "continue_game": -2}


    def set_game_params(self, board):
        self.board = board
        for i, row in enumerate(board):
            for j, val in enumerate(row):
                if val == 1:
                    self.loc = (i, j)
                elif val == 2:
                    self.rival_loc = (i, j)

    def make_move(self, time_limit): #number of seconds to finish
        start_time = tm.time()
        d = 1
        move, score = self.minimax(self.loc, 1)
        if move == self.loc :
            return (0, 0)

        '''
        last_iteration_time = tm.time() - ID_start_time
        next_iteration_max_time = (, last_iteration_time)
        time_until_now = tm.time() - start_time
        While
        time_until_now + next_iteration_max_time < time_limit:
        8 += 1
        iteration_start_time = tm.time()

        move, = (s,)
        last_iteration_time = tm.time() - iteration_start_time
        next_iteration_max_time = (, last_iteration_time)
        time_until_now = tm.time() - ID_start_time
'''
        return (0,1)

    # returns true is no moves possible
    def g_check_win(self):
        possible_next_locations_me = self.get_succ_moves(1)
        possible_next_locations_rival = self.get_succ_moves(2)
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

    def minimax(self, location, agent):
        chosen = self.loc

        game_finished, finish_state = self.g_check_win()
        if game_finished:
            return chosen, finish_state

        # get successors
        children = self.get_succ_moves()
        print(children)

        # max player
        if agent == 1:
            cur_max = -float('inf')
            for child in children:
                _, val_of_move = self.minimax(child, 3 - agent)
                if val_of_move > cur_max:
                    chosen = child
                cur_max = max(cur_max, val_of_move)
            return chosen, cur_max

        # min player
        else:
            cur_min = float('inf')
            for child in children:
                _, val_of_move = self.minimax(child, 3 - agent)
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

    def get_succ_moves(self, agent):

        if agent == 1:
            location = self.loc
        else:
            location = self.rival_loc

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
