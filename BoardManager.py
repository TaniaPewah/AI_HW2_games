import numpy as np
import queue

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
        self.rival_reachable = 1

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

# i have 1 possible move, rival has none, im not moving becuse check win is True and victory, not returning the move to make  (0,1) (8,5)
    def g_check_win(self, agent):
        possible_next_locations_me = self.get_succ_moves(agent)
        possible_next_locations_rival = self.get_succ_moves(3 - agent)
        if len(possible_next_locations_me) != 0:
            if len(possible_next_locations_rival) == 0:
                return True, self.end_game_states["victory"], possible_next_locations_me[0]
            else:
                return False, self.end_game_states["continue_game"], (0,0)
        else:
            if len(possible_next_locations_rival) != 0:
                return True, self.end_game_states["loose"], (0,0)
            else:
                # TODO check who is the starting player using tile counting
                return True, self.end_game_states["tie"], (0,0)

    def get_surrounding_tiles(self, loc):
        cnt = 0
        for i in range(-1,1):
            for j in range(-1,1):
                new_loc = add(loc, (i, j))
                if self.is_move_valid(new_loc):
                    cnt +=1
        return cnt

    def bfs(self):

        helper_mat = np.zeros_like(self.map)
        qu = queue.Queue()
        qu.put(self.my_loc)

        while not qu.empty():
            curr_r, curr_c = qu.get()
            dist = helper_mat[curr_r][curr_c]
            adj_cells = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            for r_adj, c_adj in adj_cells:
                adj_row = curr_r + r_adj
                adj_col = curr_c + c_adj
                if 0 <= adj_row < self.map.shape[0] and 0 <= adj_col < self.map.shape[1]:
                    # check whether the tile is white and not visited
                    if helper_mat[adj_row][adj_col] == 0 and self.map[adj_row][adj_col] == 0:
                            helper_mat[adj_row][adj_col] = dist + 1
                            qu.put((adj_row, adj_col))
                    # check whther the tile is rival
                    elif self.map[adj_row][adj_col] == 2:
                        return dist + 1

        self.rival_reachable = 0
        return float("inf")

    def path_search(self):

        # TODO dfs?
        helper_mat = np.zeros_like(self.map)
        qu = queue.Queue()
        qu.put(self.my_loc)
        dist = 0
        while not qu.empty():
            curr_r, curr_c = qu.get()
            dist = helper_mat[curr_r][curr_c]
            adj_cells = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            for r_adj, c_adj in adj_cells:
                adj_row = curr_r + r_adj
                adj_col = curr_c + c_adj
                if 0 <= adj_row < self.map.shape[0] and 0 <= adj_col < self.map.shape[1]:
                    # check whether the tile is white and not visited
                    if helper_mat[adj_row][adj_col] == 0 and self.map[adj_row][adj_col] == 0:
                        helper_mat[adj_row][adj_col] = dist + 1
                        qu.put((adj_row, adj_col))
        return dist

    def heuristic(self):
        w = (0.25, 0.25, 0.25, 0.25)
        # TODO refine the heuristic using these:

        # if we are second player how to know that check symetry reverse sideways reverse updown to conclude

        # rival distance to our location using white tiles using BFS normalized
        if self.rival_reachable:
            distance_to_rival = self.bfs()
        else:
            distance_to_rival = float("inf")

        if distance_to_rival == float("inf"):
            distance_to_rival = 0
        else:
            distance_to_rival = (distance_to_rival / self.map.shape[0] * self.map.shape[1]) * 100

        # bsf result on maximum travel dist normalized to board size
        max_travel_dist = (self.path_search() / self.map.shape[0] * self.map.shape[1]) * 100

        # board state: num of white tiles around me
        surrounding_my = self.get_surrounding_tiles(self.my_loc)
        surrounding_rival = self.get_surrounding_tiles(self.rival_loc)
        surrounding_area = ((surrounding_my - surrounding_rival*2) / 24) * 100

        # num of available directions
        possible_next_me = self.get_succ_moves(1)
        possible_next_rival = self.get_succ_moves(2)
        possible_moves_diff = ((len(possible_next_me) - len(possible_next_rival)*2)/ 12) * 100
        #check if I can cut the rival path:
        # my_moves = add(self.my_loc, possible_next_me)
        # rival_moves = add(self.rival_loc, possible_next_rival)
        # intersection = tuple(set(my_moves) & set(rival_moves))
        # if len(intersection) == 1 and len(rival_moves) == 1:
        #     return self.end_game_states["victory"]

        return w[0]*surrounding_area + w[1]*possible_moves_diff + \
               w[2]*distance_to_rival + w[3]*max_travel_dist

    def set_rival_loc(self, loc):
        self.map[self.rival_loc] = -1
        self.rival_loc = loc
        self.map[loc] = 2

    # TODO maybe not use f and use real time threshold instead
    def f(self, prev_time, leaves):
        total_nodes = leaves * 1.5
        time_for_node = prev_time / total_nodes
        extra_leaves = leaves * 3
        extra_time = extra_leaves * time_for_node
        total_time = prev_time + extra_time
        return total_time
