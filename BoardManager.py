# TODO use directions instead of locations,


def add(a, b):
    return tuple(map(sum, zip(a, b)))


class BoardManager:
    def __init__(self, board):
        self.my_loc = None
        self.rival_loc = None
        self.map = board
        self.directions = {"up": (1, 0),
                           "right": (0, 1),
                           "down": (-1, 0),
                           "left": (0, -1)}
        self.end_game_states = {"victory": 100, "loose": -100, "tie": 0, "continue_game": -2}
        self.direction = None

    def set_game(self):
        for i, row in enumerate(self.map):
            for j, val in enumerate(row):
                if val == 1:
                    self.my_loc = (i, j)
                elif val == 2:
                    self.rival_loc = (i, j)

    def update_board(self, action, agent, direction):
        rival = self.rival_loc

        if action == 1:
            if agent == 1:
                self.map[self.my_loc] = -1
                self.my_loc = add(self.my_loc, direction)
                self.map[self.my_loc] = 1
            else:
                self.map[rival] = -1
                self.rival_loc = add(self.rival_loc, direction)
                self.map[self.rival_loc] = 2
        elif action == -1:
            reverse_direction = (-1 * direction[0], -1 * direction[1])
            if agent == 1:
                self.map[self.my_loc] = 0
                self.my_loc = add(self.my_loc, reverse_direction)
                self.map[self.my_loc] = 1
            else:
                self.map[rival] = 0
                self.rival_loc = add(self.rival_loc, reverse_direction)
                self.map[self.rival_loc] = 2

    def get_succ_moves(self, agent):

        if agent == 1:
            location = self.my_loc
        else:
            location = self.rival_loc

        up = add(location, self.directions["up"])
        down = add(location, self.directions["down"])
        left = add(location, self.directions["left"])
        right = add(location, self.directions["right"])

        moves = {"up": up, "down": down, "left": left, "right": right}
        legal_moves = list(filter(lambda move: self.is_move_valid(move) == True, moves.values()))
        legal_directions = []

        for key, value in moves.items():
            if value in legal_moves:
                legal_directions += [(self.directions[key])]

        return legal_directions

    def is_move_valid(self, new_loc):

        i = new_loc[0]
        j = new_loc[1]

        return 0 <= i and i < self.map.shape[0] and 0 <= j and j < self.map.shape[1] and self.map[i][j] == 0


    def g_check_win(self, agent):
        possible_next_locations_me = self.get_succ_moves(agent)
        possible_next_locations_rival = self.get_succ_moves(3 - agent)
        if len(possible_next_locations_me) != 0:
            if len(possible_next_locations_rival) == 0:
                return True, self.end_game_states["victory"]
            else:
                return False, self.end_game_states["continue_game"]
        else:
            if len(possible_next_locations_rival) != 0:
                return True, self.end_game_states["loose"]
            else:
                # TODO check who is the starting player using tile counting
                return True, self.end_game_states["tie"]

    def heuristic(self):
        # TODO refine the heuristic using these:
        # rival distance to our location using white tiles using BFS?
        # board state: num of white tiles around me
        # use self.leaves

        possible_next_me = len(self.get_succ_moves(1))
        possible_next_rival = len(self.get_succ_moves(2))

        return possible_next_me - possible_next_rival

    def set_rival_loc(self, loc):
        self.map[self.rival_loc] = -1
        self.rival_loc = loc
        self.map[loc] = 2