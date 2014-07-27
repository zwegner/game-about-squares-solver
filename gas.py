# Copyright 2014 Zach Wegner

import levels

class Pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __add__(self, other):
        return Pos(self.x + other.x, self.y + other.y)
    def __hash__(self):
        return hash((self.x, self.y))
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    def __repr__(self):
        return '<%s, %s>' % (self.x, self.y)

class Dir:
    def __repr__(self):
        return dir_str[self]

# Create dummy singleton objects: stupid enum
UP, DOWN, LEFT, RIGHT = all_dirs = [Dir() for x in range(4)]
dir_vector = {
    UP: Pos(0, -1),
    DOWN: Pos(0, 1),
    LEFT: Pos(-1, 0),
    RIGHT: Pos(1, 0)
}
dir_str = {
    UP: 'up',
    DOWN: 'down',
    LEFT: 'left',
    RIGHT: 'right'
}
inv_dir_str = {v: k for k, v in dir_str.items()}

class State:
    def __init__(self, positions, directions, goals, arrows):
        self.colors = list(sorted(positions.keys()))
        self.positions = positions
        self.directions = directions
        self.goals = goals
        self.arrows = arrows

    def is_win(self):
        return all(self.positions[c] == self.goals[c] for c in self.colors)

    # Used for equality/hashing
    # XXX as an optimization, only valid for a particular level
    def essence(self):
        # Make sure to hash positions/directions in deterministic order
        return tuple((self.positions[c], self.directions[c]) for c in self.colors)

    def __hash__(self):
        return hash(self.essence())

    def __eq__(self, other):
        return self.essence() == other.essence()

    # XXX slow
    def lookup_square(self, pos):
        for c, p in self.positions.items():
            if p == pos:
                return c
        return None

    # XXX slow
    def lookup_arrow(self, pos):
        for p, d in self.arrows:
            if p == pos:
                return d
        return None

    # XXX slow
    def lookup_goal(self, pos):
        for c, p in self.goals.items():
            if p == pos:
                return c
        return None

    def move(self, color):
        # Save off undo information
        undo_pos, undo_dir = [], []

        # Push all squares in front of this one
        d = dir_vector[self.directions[color]]
        p = self.positions[color]
        undo_pos.append([color, p])
        new_pos = p + d
        while True:
            new_color = self.lookup_square(new_pos)
            self.positions[color] = new_pos
            color = new_color
            if color is None:
                break
            undo_pos.append([color, new_pos])
            new_pos = new_pos + d

        # Go through and change their directions if they are on top of arrows
        for c, p in undo_pos:
            a = self.lookup_arrow(self.positions[c])
            if a is not None:
                undo_dir.append([c, self.directions[c]])
                self.directions[c] = a

        return undo_pos, undo_dir

    def undo(self, undo_info):
        undo_pos, undo_dir = undo_info
        for c, p in undo_pos:
            self.positions[c] = p
        for c, d in undo_dir:
            self.directions[c] = d

    def print(self):
        all_features = list(self.positions.values()) + list(self.goals.values()) + [a[0] for a in self.arrows]
        # Meh, need the high end to be one more
        max_plus_1 = lambda arg: max(arg) + 1
        ranges = {coord: [minmax(getattr(p, coord) for p in all_features) for minmax in [min, max_plus_1]]
            for coord in ['x', 'y']}
        sq_table = {
            UP: '^',
            DOWN: 'v',
            LEFT: '<',
            RIGHT: '>'
        }
        for y in range(*ranges['y']):
            for x in range(*ranges['x']):
                pos = Pos(x, y)
                c = self.lookup_square(pos)
                if c is not None:
                    char = sq_table[self.directions[c]]
                elif self.lookup_arrow(pos) is not None:
                    char = '%'
                elif self.lookup_goal(pos) is not None:
                    char = '#'
                else:
                    char = ' '
                print(char, end='')
            print()

WIN_SCORE = 100000

def score_is_win(score):
    # XXX 1000 move maximum solution length
    return score > WIN_SCORE - 1000

def eval_state(state):
    score = 0
    for color in state.colors:
        position = state.positions[color]
        goal = state.goals[color]
        dist = abs(position.x - goal.x) + abs(position.y - goal.y)
        if dist == 0:
            score += 1000
        else:
            score += 100 / dist
    return score

def order_colors(state, depth):
    # Sort the different possible moves by making them and then evaluating the position
    scores = {}
    for color in state.colors:
        undo = state.move(color)
        score = eval_state(state)
        scores[color] = score
        state.undo(undo)
    return sorted(state.colors, key=lambda c: -scores[c])

def search(state, ply, depth):
    global nodes, hash_table
    nodes += 1
    if state.is_win():
        return WIN_SCORE - ply, []
    elif depth <= 0:
        return eval_state(state), []

    hash_key = (state, depth)
    if hash_key in hash_table:
        return hash_table[hash_key]

    best_score, best_moves = -1000, None
    for rank, color in enumerate(order_colors(state, depth)):
        undo = state.move(color)
        score, moves = search(state, ply + 1, depth - rank ** 2 - 1)
        if score > best_score:
            best_score = score
            best_moves = [color] + moves
        state.undo(undo)

    hash_table[hash_key] = best_score, best_moves

    return best_score, best_moves

for i, level in enumerate(levels.levels):
    print('Solving level %s: %s...' % (i, level['name']))

    # Do some simple transformations to match our data structures
    positions = {c: Pos(x, y) for c, [x, y] in level['positions'].items()}
    directions = {c: inv_dir_str[d] for c, d in level['directions'].items()}
    goals = {c: Pos(x, y) for c, [x, y] in level['goals'].items()}
    arrows = [[Pos(x, y), inv_dir_str[d]] for x, y, d in level['arrows']]
    state = State(positions, directions, goals, arrows)
    #state.print()

    nodes = 0
    hash_table = {}
    for depth in range(4, 400, 4):
        score, moves = search(state, 0, depth)
        # XXX
        if score_is_win(score):
            print('Solution found! depth=%s nodes=%s\n%s' % (depth, nodes, moves))
            break
    else:
        print('No solution, depth=%s nodes=%s' % (depth, nodes))
        state.print()
        break
