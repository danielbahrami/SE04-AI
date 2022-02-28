A = 'A'
B = 'B'

Environment = {
    A: 'Dirty',
    B: 'Dirty',
    'Current': A
}


def reflex_vacuum_agent(loc_st):
    if loc_st[1] == 'Dirty':
        return 'Suck'
    if loc_st[0] == A:
        return 'Right'
    if loc_st[0] == B:
        return 'Left'


def sensors():
    location = Environment['Current']
    return location, Environment[location]


def actuators(action):
    location = Environment['Current']
    if action == 'Suck':
        Environment[location] = 'Clean'
    elif action == 'Right' and location == A:
        Environment['Current'] = B
    elif action == 'Left' and location == B:
        Environment['Current'] = A


def run(n):
    print('Current                     New')
    print('location    status  action  location    status')
    for i in range(1, n):
        (location, status) = sensors()
        print("{:12s}{:8s}".format(location, status), end='')
        action = reflex_vacuum_agent(sensors())
        actuators(action)
        (location, status) = sensors()
        print("{:8s}{:12s}{:8s}".format(action, location, status))


if __name__ == '__main__':
    run(10)
