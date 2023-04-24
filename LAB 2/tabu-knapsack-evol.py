import random

# Main start function where we provide the program with the desired data and start the Tabu process.
# Here the program is going to be instantiated n_exp times.
# n is the amount of iterations per experiment and k represents the number of iterations of Tabu Search
def start():
    filename = input("Input filename: ")
    f = open(filename, "r")
    data = read_data(f)

    n_exp = 10
    n = 1000
    k = 10

    print(f"{n_exp} experiments ran.")
    print(f"With {n} iterations.")
    print(f"Each having {k} Tabu Search iterations.")

    best_solutions = []
    for i in range(n_exp):
        solution = run(n, k, data[0], data[1])
        best_solutions.append(solution)

    best = best_solutions[0]
    bestq = total_value(best, data[0])
    sum = 0
    count = 0
    for sol in best_solutions:
        quality = total_value(sol, data[0])
        weight = total_weight(sol, data[0])
        sum += quality
        count += 1
        if quality > bestq:
            best = sol
            bestq = quality
        print(string_solution(sol, weight, quality, data[1]))

    print("======================================================")
    print("BEST SOLUTION")
    print(string_solution(best, total_weight(best, data[0]), bestq, data[1]))
    print(f"Average quality {round(sum/count)}")
    print("======================================================")

# Here we read the data from the CSV file in the preferred format, while building the items in a weight-value configuration.
def read_data(file):
    n = int(file.readline())

    data = []

    for i in range(n):
        line = file.readline()
        stripped_line = " ".join(line.split())
        item = tuple(map(int, stripped_line.split(" ")))
        data.append(item)

    max = int(file.readline())

    return (data, max)

###

# This is the main algorithm, we start with a random valid solution and then we iterate through all the possible
# neighbours while maintaining a tabu list to ensure that we don't get stuck in a cycle. At the end, it will return the best solution found.
def run(n, k, data, max):
    s0 = generate_random_valid_solution(data, max)
    best = s0
    bcandidate = s0
    M = []
    Mf = []
    M.append(s0)
    Mf.append(k)

    for i in range(n):
        neighbours = generate_neighbours_of_solution(bcandidate, data, max)

        if not neighbours:
            continue

        bcandidate = neighbours[0]
        for j in range(len(neighbours)):
            isTabu = False
            for item in M:
                if neighbours[j] == item:
                    isTabu = True
                    break

            if isTabu:
                continue

            if total_value(neighbours[j], data) > total_value(bcandidate, data):
                bcandidate = neighbours[j]

        if total_value(bcandidate, data) > total_value(best, data):
            best = bcandidate

        to_remove = []
        for j in range(len(Mf)):
            Mf[j] = Mf[j] - 1
            if Mf[j] == 0:
                to_remove.append(j)
                M.pop(j)
        for j in to_remove:
            Mf.pop(j)

        M.append(bcandidate)
        Mf.append(k)

    return best

###

# This generates all valid neighbours to the input solution, switching one bit at a time and then returns a list of all the neighbours.
def generate_neighbours_of_solution(solution, data, max):
    neighbours = []
    for i in range(len(solution)):
        neighbour = solution.copy()
        bit = neighbour[i]
        neighbour[i] = 0 if bit else 1
        if is_valid(total_weight(neighbour, data), max):
            neighbours.append(neighbour)
    
    return neighbours

# Method to generate a random valid solution that also takes into account the maximum weight, making the return valid.
def generate_random_valid_solution(data, max):
    while True:
        solution = []
        for i in range(len(data)):
            k = random.choice([0, 1])
            solution.append(k)
        if is_valid(total_weight(solution, data), max):
            return solution

# Method to check if a solution is valid, pretty self-explanatory lol.
def is_valid(weight, max):
    if weight <= max:
        return True
    else:
        return False
    
# Utilitary method to calculate the weight of an inputted solution.
def total_weight(solution, data):
    sum = 0
    for item in data:
        if solution[item[0] - 1]:
            sum = sum + item[1]

    return sum

# This method calculates the total values of a solution by summing up everything inside that solution.
def total_value(solution, data):
    sum = 0
    for item in data:
        if solution[item[0] - 1]:
            sum = sum + item[2]

    return sum

# Basic formatting to ensure quality logging.
def string_solution(solution, weight, quality, max):
    return f"Solution: {solution} - quality: {quality}, weight: {weight}/{max}"

###

start()
