import numpy as np

"""
Hidden Markov Model using Viterbi algorithm to find most
likely sequence of hidden states.

The problem is to find out the most likely sequence of states
of the weather (hot, cold) from a describtion of the number
of ice cream eaten by a boy in the summer.

Check https://web.stanford.edu/~jurafsky/slp3/9.pdf
"""


def main():
    np.set_printoptions(suppress=True)

    states = np.array(["initial", "hot", "cold", "final"])

    # To simulate starting from index 1, we add a dummy value at index 0
    observationss = [
        [None, 3, 1, 3],
        [None, 3, 3, 1, 1, 2, 2, 3, 1, 3],
        [None, 3, 3, 1, 1, 2, 3, 3, 1, 2],
    ]
    verbose = True

    # Markov transition matrix
    # transitions[start, end]
    transitions = np.array([[.0, .8, .2, .0],  # Initial state
                            [.0, .6, .3, .1],  # Hot state
                            [.0, .4, .5, .1],  # Cold state
                            [.0, .0, .0, .0],  # Final state
                            ])

    # Emission probabilities matrix
    # emission[state, observation]
    # Note: in the problem the possible emissions are 1, 2, 3
    # In the code, since arrays start from 0, they are 0, 1, 2, 3, but the
    # probability for 0 is always 0
    emissions = np.array([[.0, .0, .0, .0],  # Initial state
                          [.0, .2, .4, .4],  # Hot state
                          [.0, .5, .4, .1],  # Cold state
                          [.0, .0, .0, .0],  # Final state
                          ])

    if verbose:
        test_parameters(states, transitions, emissions)

    for observations in observationss:
        print("Observations: {}".format(' '.join(map(str, observations[1:]))))

        probability = compute_forward(states, observations, transitions, emissions, verbose=verbose)
        print("Probability: {}".format(probability))

        path = compute_viterbi(states, observations, transitions, emissions, verbose=verbose)
        print("Path: {}".format(' '.join(path)))

        print('')


def inclusive_range(a, b):
    return range(a, b + 1)


def compute_forward(states, observations, transitions, emissions, verbose=False):
    big_n = len(states) - 2

    # The first element is dummy, so we ignore it
    big_t = len(observations) - 1

    # The last state
    f = big_n + 1

    # Initialize to 5, so it's easy to see what elements were not overwritten
    # (0 could be a valid value)
    forward = 5 * np.ones((big_n + 2, big_t + 1))

    for s in inclusive_range(1, big_n):
        # emission[state, observation]
        o1 = observations[1]

        forward[s, 1] = transitions[0, s] * emissions[s, o1]

    if verbose:
        print("forward: ", forward[:, 1])

    for t in inclusive_range(2, big_t):
        # emission[state, observation]
        ot = observations[t]

        for s in inclusive_range(1, big_n):
            forward[s, t] = sum(
                forward[s_prime, t - 1] * transitions[s_prime, s] * emissions[s, ot]
                for s_prime in inclusive_range(1, big_n)
            )

        if verbose:
            print("forward: ", forward[:, t])

    forward[f, big_t] = sum(
        forward[s, big_t] * transitions[s, f]
        for s in inclusive_range(1, big_n)
    )

    if verbose:
        print("Complete forward matrix:")
        print(forward)

    return forward[f, big_t]


def compute_viterbi(states, observations, transitions, emissions, verbose=False):
    big_n = len(states) - 2

    # The first element is dummy, so we ignore it
    big_t = len(observations) - 1

    # The last state
    f = big_n + 1

    # Initialize to 5, so it's easy to see what elements were not overwritten
    # (0 could be a valid value)
    viterbi = 5 * np.ones((big_n + 2, big_t + 1))

    # Must be of type int, otherwise it is tricky to use its elements to index
    # the states
    # Initialize to 5, so it's easy to see what elements were not overwritten
    # (0 could be a valid value)
    backpointers = 5 * np.ones((big_n + 2, big_t + 1), dtype=int)

    for s in inclusive_range(1, big_n):
        # emission[state, observation]
        o1 = observations[1]

        viterbi[s, 1] = transitions[0, s] * emissions[s, o1]
        backpointers[s, 1] = 0

    if verbose:
        print("viterbi: ", viterbi[:, 1])

    for t in inclusive_range(2, big_t):
        # emission[state, observation]
        ot = observations[t]

        for s in inclusive_range(1, big_n):
            viterbi[s, t] = max(
                viterbi[s_prime, t - 1] * transitions[s_prime, s] * emissions[s, ot]
                for s_prime in inclusive_range(1, big_n)
            )

            # Since we loop from 1 to big_n, the result of argmax is between
            # 0 and big_n - 1. However, 0 is the initial state, the actual
            # states start from 1, so we add 1.
            backpointers[s, t] = 1 + argmax(
                viterbi[s_prime, t - 1] * transitions[s_prime, s] * emissions[s, ot]
                for s_prime in inclusive_range(1, big_n)
            )

        if verbose:
            print("viterbi: ", viterbi[:, t])

    viterbi[f, big_t] = max(
        viterbi[s, big_t] * transitions[s, f]
        for s in inclusive_range(1, big_n)
    )

    # Since we loop from 1 to big_n, the result of argmax is between
    # 0 and big_n - 1. However, 0 is the initial state, the actual
    # states start from 1, so we add 1.
    backpointers[f, big_t] = 1 + argmax(
        viterbi[s, big_t] * transitions[s, f]
        for s in inclusive_range(1, big_n)
    )

    if verbose:
        print("Complete viterbi matrix")
        print(viterbi)
        print("Complete backpointers matrix")
        print(backpointers)

    path = []

    # This is the last state index
    index = backpointers[f, big_t]
    path.append(states[index])

    # We loop backward, adding the states to the path.
    for t in range(big_t + 1, 1, -1):
        index = backpointers[index, t - 1]
        path.append(states[index])

    # Finally we reverse the path, excluding the initial state
    return reversed(path[:-1])


def argmax(sequence):
    # Note: You could use np.argmax(sequence), but only if sequence is a list.
    # If it is a generator, first convert it: np.argmax(list(sequence))
    return max(enumerate(sequence), key=lambda x: x[1])[0]


def test_parameters(states, transitions, emissions):
    # Print all the probabilities, to make sure you got the matrix right

    def print_transition(a, b):
        print("Transition from ", states[a], " to ", states[b], ": ", transitions[a, b])

    def print_emission(a, b):
        print("Emission of ", b, " from ", states[a], ": ", emissions[a, b])

    f = len(states) - 1
    print_transition(0, 1)
    print_transition(0, 2)
    print_transition(1, 2)
    print_transition(1, 1)
    print_transition(2, 1)
    print_transition(2, 2)
    print_transition(1, f)
    print_transition(2, f)

    print_emission(0, 1)
    print_emission(0, 2)
    print_emission(0, 3)
    print_emission(f, 1)
    print_emission(f, 2)
    print_emission(f, 3)
    print_emission(1, 1)
    print_emission(1, 2)
    print_emission(1, 3)
    print_emission(2, 1)
    print_emission(2, 2)
    print_emission(2, 3)


if __name__ == '__main__':
    main()
