# Copyright 2014 Andrey Shevchuk, Zach Wegner

# Stupid converter for level data, using some global state and some vim magic

colors = list(range(20))
levels = []

def level(n):
    def decorate(f):
        def inner():
            global name, goals, positions, directions, arrows
            name = f.__name__
            goals = {}
            positions = {}
            directions = {}
            arrows = []
            return f()
        levels.append(inner())
    return decorate

def goal(x, y, c):
    global goals
    goals[c] = [x, y]

def square(x, y, c, d):
    global positions, directions
    positions[c] = [x, y]
    directions[c] = d

def arrow(x, y, d):
    global arrows
    arrows.append([x, y, d])

def flush():
    # Take care of default directions
    for c, d in directions.items():
        if d == 'default':
            for x, y, a in arrows:
                if [x, y] == positions[c]:
                    directions[c] = a
                    break
            assert directions[c] != 'default'
    return {
        'name': name,
        'goals': goals,
        'positions': positions,
        'directions': directions,
        'arrows': arrows
    }

@level('hi')
def hi():
    goal(0, 2, colors[0])
    square(0, 0, colors[0], 'down')
    return flush()

@level('hi2')
def hi2():
    goal(0, 0, colors[1])
    goal(2, 2, colors[0])
    square(0, 2, colors[1], 'up')
    square(2, 0, colors[0], 'down')
    return flush()

@level('hi3')
def hi3():
    goal(0, 1, colors[1])
    goal(0, 2, colors[0])
    square(0, 0, colors[1], 'down')
    square(0, 3, colors[0], 'up')
    return flush()

@level('order')
def order():
    goal(0, 0, colors[0])
    goal(0, 1, colors[1])
    goal(2, 2, colors[2])
    square(0, 2, colors[0], 'up')
    square(2, 1, colors[1], 'left')
    square(2, 0, colors[2], 'down')
    return flush()

@level('order2')
def order2():
    goal(2, 0, colors[0])
    goal(1, 0, colors[1])
    goal(1, 1, colors[2])
    square(0, 0, colors[0], 'right')
    square(1, 2, colors[1], 'up')
    square(3, 1, colors[2], 'left')
    return flush()

@level('stupidpush')
def stupidpush():
    goal(0, 2, colors[0])
    goal(0, 3, colors[2])
    square(0, 0, colors[0], 'down')
    square(0, 1, colors[2], 'up')
    return flush()

@level('push')
def push():
    goal(0, 3, colors[0])
    goal(2, 5, colors[1])
    square(2, 0, colors[1], 'down')
    square(4, 2, colors[0], 'left')
    return flush()

@level('stairs')
def stairs():
    goal(1, 1, colors[0])
    goal(2, 2, colors[2])
    goal(3, 3, colors[1])
    square(0, 1, colors[1], 'right')
    square(1, 0, colors[0], 'down')
    square(2, 1, colors[2], 'down')
    return flush()

@level('stairs2')
def stairs2():
    goal(1, 1, colors[0])
    goal(2, 2, colors[1])
    goal(3, 3, colors[2])
    square(0, 1, colors[1], 'right')
    square(1, 0, colors[0], 'down')
    square(2, 1, colors[2], 'down')
    return flush()

@level('lift')
def lift():
    goal(0, 0, colors[2])
    goal(1, 1, colors[1])
    goal(2, 3, colors[0])
    square(2, 2, colors[2], 'up')
    square(4, 1, colors[1], 'left')
    square(3, 0, colors[0], 'down')
    return flush()

@level('presq')
def presq():
    arrow(0, 2, 'right')
    arrow(2, 2, 'up')
    goal(2, 0, colors[1])
    square(0, 0, colors[1], 'down')
    return flush()

@level('sq')
def sq():
    arrow(0, 2, 'right')
    arrow(2, 2, 'up')
    goal(2, 0, colors[3])
    goal(3, 0, colors[2])
    square(0, 0, colors[3], 'down')
    square(0, 2, colors[2], 'default')
    return flush()

@level('nobrainer')
def nobrainer():
    arrow(3, 1, 'left')
    arrow(0, 1, 'right')
    arrow(2, 1, 'up')
    goal(1, 0, colors[3])
    goal(2, 0, colors[1])
    square(0, 1, colors[3], 'default')
    square(2, 1, colors[1], 'default')
    return flush()

@level('crosst')
def crosst():
    arrow(2, 2, 'right')
    goal(0, 2, colors[2])
    goal(1, 2, colors[0])
    goal(3, 2, colors[1])
    square(2, 0, colors[0], 'down')
    square(4, 2, colors[1], 'left')
    square(2, 4, colors[2], 'up')
    return flush()

@level('t')
def t():
    arrow(2, 0, 'down')
    goal(1, 2, colors[0])
    goal(2, 2, colors[1])
    goal(3, 2, colors[2])
    square(0, 0, colors[0], 'right')
    square(4, 0, colors[1], 'left')
    square(2, 4, colors[2], 'up')
    return flush()

@level('rotation')
def rotation():
    arrow(1, 0, 'down')
    arrow(3, 1, 'left')
    goal(1, 2, colors[3])
    goal(1, 1, colors[2])
    square(0, 2, colors[3], 'right')
    square(2, 3, colors[2], 'up')
    return flush()

@level('asymm')
def asymm():
    arrow(1, 1, 'down')
    goal(0, 4, colors[3])
    goal(1, 0, colors[2])
    goal(1, 2, colors[1])
    square(3, 3, colors[3], 'left')
    square(1, 1, colors[2], 'default')
    square(2, 5, colors[1], 'up')
    return flush()

@level('herewego')
def herewego():
    arrow(0, 0, 'right')
    arrow(2, 0, 'down')
    arrow(2, 1, 'left')
    arrow(1, 2, 'up')
    goal(0, 1, colors[0])
    goal(3, 1, colors[1])
    square(0, 0, colors[0], 'default')
    square(2, 1, colors[1], 'default')
    return flush()

@level('preherewego')
def preherewego():
    arrow(0, 0, 'right')
    arrow(2, 0, 'down')
    arrow(2, 1, 'left')
    arrow(1, 2, 'up')
    goal(1, 1, colors[0])
    goal(-1, 1, colors[1])
    square(2, 0, colors[0], 'default')
    square(1, 2, colors[1], 'default')
    return flush()

@level('clover')
def clover():
    goal(0, 0, colors[0])
    goal(1, 1, colors[1])
    goal(2, 2, colors[2])
    goal(2, 0, colors[3])
    square(1, 0, colors[2], 'down')
    square(0, 1, colors[3], 'right')
    square(2, 1, colors[0], 'left')
    square(1, 2, colors[1], 'up')
    return flush()

@level('preduced')
def preduced():
    arrow(0, 0, 'down')
    arrow(0, 1, 'right')
    arrow(3, 0, 'left')
    goal(1, 1, colors[0])
    goal(1, 2, colors[1])
    square(0, 0, colors[0], 'default')
    square(2, 2, colors[1], 'up')
    return flush()

@level('preduced2')
def preduced2():
    arrow(0, 0, 'down')
    arrow(0, 1, 'right')
    goal(1, 0, colors[2])
    goal(1, 1, colors[0])
    goal(1, 2, colors[1])
    square(0, 0, colors[0], 'default')
    square(2, 2, colors[1], 'up')
    square(3, 0, colors[2], 'left')
    return flush()

@level('reduced')
def reduced():
    arrow(0, 0, 'down')
    arrow(0, 1, 'right')
    arrow(3, 0, 'left')
    arrow(2, 2, 'up')
    goal(1, 1, colors[0])
    goal(2, 1, colors[2])
    goal(3, 1, colors[1])
    square(0, 0, colors[0], 'default')
    square(3, 0, colors[1], 'default')
    square(0, 1, colors[2], 'default')
    return flush()

@level('reduced2')
def reduced2():
    arrow(0, 0, 'down')
    arrow(0, 1, 'right')
    arrow(3, 0, 'left')
    arrow(2, 2, 'up')
    goal(1, 1, colors[0])
    goal(2, 1, colors[2])
    goal(3, 1, colors[1])
    square(0, 0, colors[2], 'default')
    square(3, 0, colors[1], 'default')
    square(0, 1, colors[0], 'default')
    return flush()

@level('reduced3')
def reduced3():
    arrow(0, 0, 'down')
    arrow(0, 1, 'right')
    arrow(3, 0, 'left')
    arrow(2, 2, 'up')
    goal(1, 2, colors[2])
    goal(2, 1, colors[0])
    goal(3, 2, colors[1])
    square(0, 0, colors[2], 'default')
    square(3, 0, colors[1], 'default')
    square(0, 1, colors[0], 'default')
    return flush()

@level('recycle')
def recycle():
    arrow(0, 0, 'down')
    arrow(0, 1, 'right')
    arrow(3, 0, 'left')
    arrow(4, 0, 'left')
    arrow(3, 1, 'up')
    arrow(4, 1, 'up')
    goal(1, 0, colors[0])
    goal(2, 0, colors[1])
    goal(1, 1, colors[2])
    goal(2, 1, colors[3])
    square(3, 1, colors[0], 'default')
    square(3, 0, colors[1], 'default')
    square(0, 1, colors[2], 'default')
    square(0, 0, colors[3], 'default')
    return flush()

@level('recycle2')
def recycle2():
    arrow(0, 0, 'down')
    arrow(0, 2, 'right')
    arrow(2, 0, 'left')
    arrow(0, 4, 'up')
    arrow(2, 2, 'up')
    goal(1, 0, colors[4])
    goal(0, 1, colors[2])
    goal(1, 2, colors[6])
    goal(2, 1, colors[7])
    square(0, 0, colors[2], 'default')
    square(0, 2, colors[4], 'default')
    square(2, 2, colors[7], 'default')
    square(2, 0, colors[6], 'default')
    return flush()

@level('recycle3')
def recycle3():
    arrow(2, 0, 'left')
    arrow(0, 0, 'down')
    arrow(2, 4, 'up')
    arrow(0, 2, 'up')
    arrow(0, 3, 'down')
    arrow(0, 4, 'right')
    goal(2, 2, colors[10])
    goal(2, 3, colors[12])
    goal(2, 1, colors[9])
    goal(0, 1, colors[11])
    square(0, 4, colors[9], 'default')
    square(2, 4, colors[10], 'default')
    square(0, 0, colors[11], 'default')
    square(2, 0, colors[12], 'default')
    return flush()

@level('shuttle')
def shuttle():
    arrow(0, 2, 'right')
    arrow(4, 1, 'left')
    arrow(2, 0, 'down')
    arrow(2, 4, 'up')
    goal(1, 3, colors[0])
    goal(2, 3, colors[1])
    goal(3, 3, colors[2])
    square(1, 0, colors[1], 'down')
    square(0, 2, colors[2], 'default')
    square(4, 1, colors[0], 'default')
    return flush()

@level('shuttle2')
def shuttle2():
    arrow(0, 2, 'right')
    arrow(4, 1, 'left')
    arrow(3, 0, 'down')
    arrow(3, 4, 'up')
    goal(1, 3, colors[0])
    goal(2, 3, colors[1])
    goal(3, 3, colors[2])
    square(1, 0, colors[2], 'down')
    square(0, 2, colors[0], 'default')
    square(4, 1, colors[1], 'default')
    return flush()

@level('shuttle5')
def shuttle5():
    arrow(1, 1, 'right')
    arrow(3, 2, 'left')
    arrow(2, 0, 'down')
    arrow(2, 4, 'up')
    goal(0, 2, colors[1])
    goal(2, 2, colors[0])
    goal(4, 2, colors[2])
    square(2, 0, colors[1], 'default')
    square(1, 1, colors[2], 'default')
    square(3, 2, colors[0], 'default')
    return flush()

@level('spiral')
def spiral():
    goal(0, 0, colors[0])
    goal(1, 1, colors[1])
    goal(2, 2, colors[2])
    arrow(0, 2, 'down')
    arrow(3, 3, 'left')
    arrow(2, 4, 'up')
    arrow(0, 5, 'right')
    arrow(3, 5, 'up')
    arrow(1, 3, 'down')
    arrow(1, 4, 'right')
    square(0, 2, colors[0], 'default')
    square(2, 4, colors[2], 'default')
    square(1, 3, colors[1], 'default')
    return flush()

@level('spiral2')
def spiral2():
    goal(2, -1, colors[0])
    goal(2, 1, colors[1])
    goal(2, 3, colors[2])
    arrow(0, 2, 'down')
    arrow(3, 3, 'left')
    arrow(2, 4, 'up')
    arrow(0, 5, 'right')
    arrow(3, 5, 'up')
    arrow(1, 3, 'down')
    arrow(1, 4, 'right')
    square(0, 2, colors[0], 'default')
    square(2, 4, colors[2], 'default')
    square(1, 3, colors[1], 'default')
    return flush()

@level('windmill')
def windmill():
    arrow(2, 0, 'down')
    arrow(4, 2, 'left')
    arrow(2, 4, 'up')
    goal(2, 1, colors[0])
    goal(3, 2, colors[1])
    goal(2, 3, colors[2])
    goal(1, 2, colors[3])
    square(2, 0, colors[1], 'default')
    square(4, 2, colors[2], 'default')
    square(2, 4, colors[3], 'default')
    square(0, 2, colors[0], 'right')
    return flush()

@level('shirt')
def shirt():
    arrow(0, 2, 'right')
    arrow(1, 0, 'down')
    arrow(1, 4, 'up')
    arrow(4, 3, 'left')
    goal(2, 0, colors[0])
    square(0, 2, colors[0], 'default')
    square(1, 0, colors[1], 'default')
    square(4, 1, colors[2], 'down')
    return flush()

@level('shirt2')
def shirt2():
    arrow(0, 2, 'right')
    arrow(1, 0, 'down')
    arrow(1, 4, 'up')
    arrow(4, 3, 'left')
    goal(0, 1, colors[1])
    square(0, 2, colors[0], 'default')
    square(1, 0, colors[1], 'default')
    square(4, 1, colors[2], 'down')
    return flush()

@level('shirtDouble')
def shirtDouble():
    arrow(0, 2, 'right')
    arrow(1, 0, 'down')
    arrow(1, 4, 'up')
    arrow(4, 3, 'left')
    goal(2, 0, colors[0])
    goal(0, 1, colors[1])
    square(0, 2, colors[0], 'default')
    square(1, 0, colors[1], 'default')
    square(4, 1, colors[2], 'down')
    return flush()

@level('paper')
def paper():
    arrow(0, 0, 'down')
    arrow(3, 0, 'left')
    arrow(0, 3, 'right')
    arrow(2, 3, 'up')
    goal(0, 2, colors[0])
    goal(0, 1, colors[1])
    goal(1, 0, colors[2])
    square(2, 3, colors[1], 'default')
    square(0, 3, colors[0], 'default')
    square(0, 0, colors[2], 'default')
    return flush()

@level('splinter')
def splinter():
    goal(0, 0, colors[0])
    goal(1, 0, colors[1])
    goal(2, 0, colors[2])
    arrow(0, 1, 'down')
    arrow(0, 3, 'right')
    arrow(2, 3, 'up')
    arrow(3, 1, 'left')
    square(0, 1, colors[1], 'default')
    square(0, 3, colors[2], 'default')
    square(2, 3, colors[0], 'default')
    return flush()

@level('splinter2')
def splinter2():
    goal(0, 0, colors[1])
    goal(1, 0, colors[0])
    goal(2, 0, colors[2])
    arrow(1, 1, 'down')
    arrow(1, 3, 'right')
    arrow(3, 3, 'up')
    arrow(4, 1, 'left')
    square(1, 1, colors[1], 'default')
    square(1, 3, colors[2], 'default')
    square(3, 3, colors[0], 'default')
    return flush()

@level('elegant')
def elegant():
    arrow(1, 0, 'down')
    arrow(0, 2, 'right')
    arrow(3, 1, 'left')
    arrow(2, 3, 'up')
    goal(0, 1, colors[1])
    goal(2, 0, colors[3])
    goal(3, 2, colors[2])
    goal(1, 3, colors[0])
    square(0, 2, colors[1], 'default')
    square(2, 3, colors[0], 'default')
    square(3, 1, colors[2], 'default')
    square(1, 0, colors[3], 'default')
    return flush()

@level('elegant2')
def elegant2():
    arrow(1, 0, 'down')
    arrow(0, 3, 'right')
    arrow(3, 4, 'up')
    arrow(4, 1, 'left')
    goal(2, 0, colors[2])
    goal(3, 0, colors[0])
    goal(4, 0, colors[3])
    square(2, 4, colors[2], 'right')
    square(0, 4, colors[3], 'right')
    square(1, 4, colors[0], 'right')
    return flush()
