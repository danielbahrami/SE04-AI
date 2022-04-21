class CSP:
    def __init__(self, variables, domains, neighbours, constraints):
        self.variables = variables
        self.domains = domains
        self.neighbours = neighbours
        self.constraints = constraints

    def backtracking_search(self):
        return self.recursive_backtracking({})

    def recursive_backtracking(self, assignment):
        if self.is_complete(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            if self.is_consistent(var, value, assignment):
                assignment[var] = value
                result = self.recursive_backtracking(assignment)
                if result is not None:
                    return result
                assignment.pop(var)
        return None

    def select_unassigned_variable(self, assignment):
        for variable in self.variables:
            if variable not in assignment:
                return variable

    def is_complete(self, assignment):
        for variable in self.variables:
            if variable not in assignment:
                return False
        return True

    def order_domain_values(self, variable, assignment):
        all_values = self.domains[variable][:]
        return all_values

    def is_consistent(self, variable, value, assignment):
        if not assignment:
            return True

        for constraint in self.constraints.values():
            for neighbour in self.neighbours[variable]:
                if neighbour not in assignment:
                    continue

                neighbour_value = assignment[neighbour]
                if not constraint(variable, value, neighbour, neighbour_value):
                    return False
        return True


def create_south_america_csp():
    ar, bo, br, ch, co, ec, fr, gu, pa, pe, su, ur, ve = 'Argentina', 'Bolivia', 'Brazil', 'Chile', 'Colombia',\
                                                         'Ecuador', 'French Guyana', 'Guyana', 'Paraguay', 'Peru',\
                                                         'Suriname', 'Uruguay', 'Venezuela'
    values = ['Red', 'Green', 'Blue', 'Yellow']
    variables = [ar, bo, br, ch, co, ec, fr, gu, pa, pe, su, ur, ve]
    domains = {
        ar: values[:],
        bo: values[:],
        br: values[:],
        ch: values[:],
        co: values[:],
        ec: values[:],
        fr: values[:],
        gu: values[:],
        pa: values[:],
        pe: values[:],
        su: values[:],
        ur: values[:],
        ve: values[:]
    }
    neighbours = {
        ar: [bo, ch, pa, ur],
        bo: [ar, br, ch, pa, pe],
        br: [ar, bo, co, fr, gu, pa, pe, su, ur, ve],
        ch: [ar, bo, pe],
        co: [br, ec, pe, ve],
        ec: [co, pe],
        fr: [br, su],
        gu: [br, su],
        pa: [ar, bo, br],
        pe: [bo, br, ch, co, ec],
        su: [br, fr, gu],
        ur: [ar, br],
        ve: [br, co, gu]
    }

    def constraint_function(first_variable, first_value, second_variable, second_value):
        return first_value != second_value

    constraints = {
        ar: constraint_function,
        bo: constraint_function,
        br: constraint_function,
        ch: constraint_function,
        co: constraint_function,
        ec: constraint_function,
        fr: constraint_function,
        gu: constraint_function,
        pa: constraint_function,
        pe: constraint_function,
        su: constraint_function,
        ur: constraint_function,
        ve: constraint_function
    }

    return CSP(variables, domains, neighbours, constraints)


if __name__ == '__main__':
    south_america = create_south_america_csp()
    result = south_america.backtracking_search()
    for area, color in sorted(result.items()):
        print("{}: {}".format(area, color))
