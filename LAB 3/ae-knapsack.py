import random

def start():
    filename = input("Filename: ")
    f = open(filename, "r")
    data = read_data(f)

    n_exp = 100
    n = 10

    print(f"No. of experiments: {n_exp}")
    print(f"No. of iterations per experiment: {n}")

    best_solution = []
    best_solution_quality = 0
    sum = 0
    for i in range(n_exp):
        solution = run(n, data[0], data[1])
        quality = total_value(solution, data[0])
        sum += quality
        print(string_solution(solution, total_weight(solution, data[0]), quality, data[1]))
        if quality > best_solution_quality:
            best_solution_quality = quality
            best_solution = solution

    print("---")
    print("BEST SOLUTION")
    print(string_solution(best_solution, total_weight(best_solution, data[0]), best_solution_quality, data[1]))
    print(f"Average quality {round(sum/n_exp)}")
    print("---")

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

def run(n, data, max):
    population = []
    for i in range(100):
        population.append(generate_random_valid_solution(data, max))

    for i in range(1, n):
        selected_parents = select_parents_rhoullete(population, data)
        children = generate_children_cross_over_single_point(selected_parents, data, max)
        # children = generate_children_cross_over_multiple_points(selected_parents, data, max)
        mutated_children = generate_mutated_children(selected_parents, data, max, 100)
        pool = selected_parents + children + mutated_children
        qpool = []
        for individual in pool:
            q = total_value(individual, data)
            qpool.append((individual, q))

        qpool.sort(key=lambda i: i[1], reverse=True)

        population = []
        for j in range(100):
            population.append(qpool[j][0])

    best_solution = []
    best_quality = 0

    for individual in population:
        quality = total_value(individual, data)
        if quality > best_quality:
            best_quality = quality
            best_solution = individual

    return best_solution

def select_parents_rhoullete(population, data):
    total_quality = 0
    qualities = []
    for individual in population:
        quality = total_value(individual, data)
        total_quality += quality
        qualities.append(quality)

    probabilities = [quality / total_quality for quality in qualities]
    cumulative_probabilities = []
    for i in range(100):
        qi = 0
        for j in range(i):
            qi += probabilities[j]
        cumulative_probabilities.append(qi)

    return random.choices(population, cum_weights=cumulative_probabilities, k=100)

def generate_children_cross_over_single_point(parents, data, max):
    children = []
    for i in range(100):
        ps = random.sample(parents, 2)
        k = len(ps[0])
        r = random.randint(1, k-2)
        child1 = ps[0][:r] + ps[1][r:]
        child2 = ps[1][:r] + ps[0][r:]
        if is_valid(total_weight(child1, data), max):
            children.append(child1)
        if is_valid(total_weight(child2, data), max):
            children.append(child2)

    return children

def generate_children_cross_over_multiple_points(parents, data, max):
    children = []
    for i in range(100):
        ps = random.sample(parents, 2)
        k = len(ps[0])
        r1 = random.randint(1, k-3)
        r2 = random.randint(r1, k-1)
        child1 = ps[0][:r1] + ps[1][r1:r2] + ps[0][r2:]
        child2 = ps[1][:r1] + ps[0][r1:r2] + ps[1][r2:]
        if is_valid(total_weight(child1, data), max):
            children.append(child1)
        if is_valid(total_weight(child2, data), max):
            children.append(child2)

    return children

def generate_mutated_children(parents, data, max, n):
    children = []
    pm = random.uniform(0, 1)
    for parent in parents:
        offspring = generate_offspring(parent, pm, data, max)
        if offspring is not None:
            children.append(offspring)
    
    return children

def generate_offspring(parent, pm, data, max):
    child = parent.copy()
    for i in range(len(parent)):
        r = random.uniform(0, 1)
        if r < pm:
            child[i] = 0 if child[i] else 1
    if is_valid(total_weight(child, data), max):
        return child

###

def generate_random_valid_solution(data, max):
    while True:
        solution = []
        for i in range(len(data)):
            k = random.choice([0, 1])
            solution.append(k)
        if is_valid(total_weight(solution, data), max):
            return solution

def is_valid(weight, max):
    if weight <= max:
        return True
    else:
        return False
    
def total_weight(solution, data):
    sum = 0
    for item in data:
        if solution[item[0] - 1]:
            sum = sum + item[1]

    return sum

def total_value(solution, data):
    sum = 0
    for item in data:
        if solution[item[0] - 1]:
            sum = sum + item[2]

    return sum

def string_solution(solution, weight, quality, max):
    return f"Solution: {solution} - quality: {quality}, weight: {weight}/{max}"

###

start()
