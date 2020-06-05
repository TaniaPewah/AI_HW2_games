import time as tm

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

    def make_move(self, time_limit): #number of seconds to finish
        start_time = tm.time()

        #get successors
        children = self.get_succ_moves()
        print (children)
        # check is game finished then return score

        # check

        return ''


    def is_move_valid(self,loc):
        return self.board.loc_is_in_board(loc) and self.board[loc[0],loc[1]] == 0

    def get_succ_moves(self):
        up = (self.loc[0] + 1, self.loc[1])
        down = (self.loc[0] - 1, self.loc[1])
        left = (self.loc[0], self.loc[1] - 1)
        right = (self.loc[0], self.loc[1] + 1)

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
        move, = (s,)
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

'''def state_score(self, board, loc):
        return True'''

'''def count_ones(self, board):
        counter = 0
        for i, row in enumerate(board):
            for j, val in enumerate(row):
                if val == 1:
                    counter += 1
        return counter'''
