def minmax_decision(state):
    def max_value(state):
        if is_terminal(state):
            return utility_of(state)
        v = -infinity
        for (a, s) in successors_of(state):
            v = max(v, min_value(s))
        print('V: ' + str(v))
        return v

    def min_value(state):
        if is_terminal(state):
            return utility_of(state)
        v = infinity
        for (a, s) in successors_of(state):
            v = min(v, max_value(s))
        return v

    infinity = float('inf')
    action, state = argmax(successors_of(state), lambda a: min_value(a[1]))
    return action


"""
returns True if the state is either a win or a tie (board full)
:param state: State of the checkerboard. Ex: [0; 1; 2; 3; X; 5; 6; 7; 8]
:return:
"""


def is_terminal(state):
    if state.count('X') >= 3 and check_terminal(state, 'X'):
        return True
    if state.count('O') >= 3 and check_terminal(state, 'O'):
        return True
    if state.count('X') + state.count('O') >= len(state):
        return True
    return False


def check_terminal(state, character):
    check_character = [i for i in range(0, 9) if state[i] == character]
    check_board = {
        0: [0, 4, 8],
        1: [2, 4, 6],
        2: [0, 1, 2],
        3: [0, 3, 6],
        4: [6, 7, 8],
        5: [2, 5, 8],
        6: [3, 4, 5],
        7: [1, 4, 7]
    }
    for i in range(0, len(check_board)):
        if len([value for value in check_board[i] if value in check_character]) == 3:
            return True
    return False


"""
returns +1 if winner is X (MAX player), -1 if winner is O (MIN player), or 0 otherwise
:param state: State of the checkerboard. Ex: [0; 1; 2; 3; X; 5; 6; 7; 8]
:return:
"""


def utility_of(state):
    if check_terminal(state, 'X'):
        return 1
    if check_terminal(state, 'O'):
        return -1
    return 0


"""
returns a list of tuples (move, state) as shown in the exercise slides
:param state: State of the checkerboard. Ex: [0; 1; 2; 3; X; 5; 6; 7; 8]
:return:
"""


def successors_of(state):
    possible_moves = []
    for i in range(0, 9):
        if state[i] != 'X' and state[i] != 'O':
            played_moves = []
            for j in range(0, 9):
                if j == i and state.count('X') == state.count('O'):
                    played_moves.append('X')
                elif j == i and state.count('X') > state.count('O'):
                    played_moves.append('O')
                else:
                    played_moves.append(state[j])
            possible_moves.append((i, played_moves.copy()))
    return possible_moves


def display(state):
    print("-----")
    for c in [0, 3, 6]:
        print(state[c + 0], state[c + 1], state[c + 2])


def main():
    board = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    while not is_terminal(board):
        board[minmax_decision(board)] = 'X'
        if not is_terminal(board):
            display(board)
            board[int(input('Your move? '))] = 'O'
    display(board)


def argmax(iterable, func):
    return max(iterable, key=func)


if __name__ == '__main__':
    main()
