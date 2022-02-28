A = 'A'
B = 'B'
C = 'C'
D = 'D'

state = {}
action = None
model = {A: None, B: None, C: None, D: None}

RULE_ACTION = {
    1: 'Suck',
    2: 'Right',
    3: 'Left',
    4: 'Up',
    5: 'Down',
    6: 'NoOp'
}

rules = {
    (A, 'Dirty'): 1,
    (B, 'Dirty'): 1,
    (C, 'Dirty'): 1,
    (D, 'Dirty'): 1,
    (A, 'Clean'): 4,
    (B, 'Clean'): 2,
    (C, 'Clean'): 5,
    (D, 'Clean'): 3,
    (A, B, C, D, 'Clean'): 6
}

Environment = {
    A: 'Dirty',
    B: 'Dirty',
    C: 'Dirty',
    D: 'Dirty',
    'Current': A
}


def interpret_input(input):
    return input


def rule_match(state, rules):
    rule = rules.get(tuple(state))
    return rule


def update_state(state, action, percept):
    (location, status) = percept
    state = percept
    if model[A] == model[B] == model[C] == model[D] == 'Clean':
        state = (A, B, C, D, 'Clean')
    model[location] = status
    return state


def reflex_agent_with_state(percept):
    global state, action
    state = update_state(state, action, percept)
    rule = rule_match(state, rules)
    action = RULE_ACTION[rule]
    return action


def sensors():
    location = Environment['Current']
    return location, Environment[location]


def actuators(action):
    location = Environment['Current']
    if action == 'Suck':
        Environment[location] = 'Clean'
    elif action == 'Up' and location == A:
        Environment['Current'] = B
    elif action == 'Right' and location == B:
        Environment['Current'] = C
    elif action == 'Down' and location == C:
        Environment['Current'] = D
    elif action == 'Left' and location == D:
        Environment['Current'] = A


def run(n):
    print('Current                     New')
    print('location    status  action  location    status')
    for i in range(1, n):
        (location, status) = sensors()
        print("{:12s}{:8s}".format(location, status), end='')
        action = reflex_agent_with_state(sensors())
        actuators(action)
        (location, status) = sensors()
        print("{:8s}{:12s}{:8s}".format(action, location, status))


if __name__ == '__main__':
    run(20)
