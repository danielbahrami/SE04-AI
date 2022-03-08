class Node:  # Node has only PARENT_NODE, STATE, DEPTH
    def __init__(self, state, parent=None, depth=0):
        self.STATE = state
        self.PARENT_NODE = parent
        self.DEPTH = depth

    def path(self):  # Create a list of nodes from the root to this node.
        current_node = self
        path = [self]
        while current_node.PARENT_NODE:  # while current node has parent
            current_node = current_node.PARENT_NODE  # make parent the current node
            path.append(current_node)  # add current node to path
        return path

    def display(self):
        print(self)

    def __repr__(self):
        return 'State: ' + str(self.STATE) + ' - Depth: ' + str(self.DEPTH)


'''
Search the tree for the goal state and return path from initial state to goal state
'''


def tree_search():
    fringe = []
    initial_node = Node(INITIAL_STATE)
    fringe = insert(initial_node, fringe)
    while fringe is not None:
        node = remove_first(fringe)
        if node.STATE == GOAL_STATE:
            return node.path()
        children = expand(node)
        fringe = insert_all(children, fringe)
        print("fringe: {}".format(fringe))


'''
Expands node and gets the successors (children) of that node.
Return list of the successor nodes.
'''


def expand(node):
    successors = []
    children = successor_fn(node.STATE)
    for child in children:
        s = Node(node)  # create node for each in state list
        s.STATE = child  # e.g. result = 'F' then 'G' from list ['F', 'G']
        s.PARENT_NODE = node
        s.DEPTH = node.DEPTH + 1
        successors = insert(s, successors)
    return successors


'''
Insert node in to the queue (fringe).
'''


def insert(node, queue):
    queue.append(node)
    return queue


'''
Insert list of nodes into the fringe
'''


def insert_all(list, queue):
    for node in list:
        insert(node, queue)
    return queue


'''
Removes and returns the first element from fringe
'''


def remove_first(queue):
    return queue.pop(0)


'''
Successor function, mapping the nodes to its successors
'''


def successor_fn(state):  # Lookup list of successor states
    return STATE_SPACE[state]  # successor_fn( 'C' ) returns ['F', 'G']


# ('Farmer', 'Wolf', 'Goat', 'Cabbage')
INITIAL_STATE = ('W', 'W', 'W', 'W')
GOAL_STATE = ('E', 'E', 'E', 'E')
STATE_SPACE = {('W', 'W', 'W', 'W'): [('', '', '', ''), ('', '', '', ''), ('', '', '', '')],
               ('W', 'W', 'W', 'W'): [('', '', '', ''), ('', '', '', ''), ('', '', '', '')],
               ('W', 'W', 'W', 'W'): [('', '', '', ''), ('', '', '', ''), ('', '', '', '')],
               ('W', 'W', 'W', 'W'): [('', '', '', ''), ('', '', '', ''), ('', '', '', '')],
               ('W', 'W', 'W', 'W'): [('', '', '', ''), ('', '', '', ''), ('', '', '', '')],
               ('W', 'W', 'W', 'W'): [('', '', '', ''), ('', '', '', ''), ('', '', '', '')],
               ('W', 'W', 'W', 'W'): [('', '', '', ''), ('', '', '', ''), ('', '', '', '')],
               ('W', 'W', 'W', 'W'): [('', '', '', ''), ('', '', '', ''), ('', '', '', '')],
               ('W', 'W', 'W', 'W'): [('', '', '', ''), ('', '', '', ''), ('', '', '', '')],
               ('W', 'W', 'W', 'W'): [('', '', '', ''), ('', '', '', ''), ('', '', '', '')],
               ('W', 'W', 'W', 'W'): [('', '', '', ''), ('', '', '', ''), ('', '', '', '')],
               ('W', 'W', 'W', 'W'): [('', '', '', ''), ('', '', '', ''), ('', '', '', '')],
               ('W', 'W', 'W', 'W'): [('', '', '', ''), ('', '', '', ''), ('', '', '', '')],
               ('W', 'W', 'W', 'W'): [('', '', '', ''), ('', '', '', ''), ('', '', '', '')],
               ('W', 'W', 'W', 'W'): [('', '', '', ''), ('', '', '', ''), ('', '', '', '')],
               }

'''
Run tree search and display the nodes in the path to goal node
'''


def run():
    path = tree_search()
    print('Solution path:')
    for node in path:
        node.display()


if __name__ == '__main__':
    run()
