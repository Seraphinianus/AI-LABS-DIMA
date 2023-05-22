import math
import random

def start():
    filename = input("Filename: ")
    f = open(filename, "r")
    data = read_data(f)

    n_exp = 100
    n = 10

    print(f"No. of experiments: {n_exp}")
    print(f"No. of iterations per experiment: {n}")

    best_solutions = []
    for i in range(n_exp):
        solution = run(n, data)
        best_solutions.append(solution)
        dst = distance(solution, data)
        print(string_solution(solution, dst))

    best = best_solutions[0]
    bestd = distance(best, data)
    sum = 0
    for sol in best_solutions:
        dst = distance(sol, data)
        sum += dst
        if dst < bestd:
            best = sol
            bestd = dst
        print(string_solution(sol, dst))
        
    print("---")
    print("BEST SOLUTION")
    print(string_solution(best, bestd))
    print(f"Average distance - {round(sum/n_exp)}")
    print("---")

def read_data(file):
    for i in range(6):
        file.readline()

    data = []

    line = file.readline()
    while True:
        stripped_line = " ".join(line.split())
        if stripped_line == 'EOF':
            break
        item = tuple(map(int, stripped_line.split(" ")))
        data.append(item)
        line = file.readline()

    return data

###

# The program is going to be run n times for 101 individuals in each generation. 
# For each generation, the program is going to select the parents based on a roulette selection method
# It will then generate children using crossover and mutation operators, and then selects the next
# population based on the fitness of the individuals of the current population.
# The best solution found across all the runs of the genetic algorithm is returned,
# after which the program outputs information about this best solution, including the distance between 
# the solution and the data points, as well as the average distance across all 10 runs of the genetic alg.

# 1. Crossover Operator: In this step, the genetic algorithm selects two parents from the population 
# based on their fitness value. The algorithm then selects a crossover point at random and exchanges 
# genetic material between the two parents to create a new child.
# 2. Mutation Operator: After crossover, the algorithm applies a mutation operator to the 
# new child's chromosome to introduce small changes. This step helps to explore new areas of 
# the search space and avoid getting stuck in local optima.

# These Operators randomly operate on the children of a parent inside a population such that 
# there is diverse genetic material and this may lead to improved fitness values.
# The algorithm eventually converges to a good enough solution!

def run(n, data):
    population = []
    for i in range(101):
        population.append(generate_random_solution(data))

    for i in range(1, n):
        selected_parents = select_parents_rhoullete(population, data)
        children = generate_children_cross_over_order(selected_parents)
        # children = generate_children_cross_over_partially(selected_parents)
        mutated_children = generate_mutated_children_scramble(selected_parents)
        pool = selected_parents + children + mutated_children
        qpool = []
        for individual in pool:
            q = distance(individual, data)
            qpool.append((individual, q))

        qpool.sort(key=lambda i: i[1])

        population = []
        for j in range(101):
            population.append(qpool[j][0])

    best_solution = population[0]
    best_distance = distance(population[0], data)

    for individual in population:
        dst = distance(individual, data)
        if dst < best_distance:
            best_distance = dst
            best_solution = individual

    return best_solution

def select_parents_rhoullete(population, data):
    total_distance = 0
    distances = []
    for individual in population:
        dst = distance(individual, data)
        total_distance += dst
        distances.append(dst)

    probabilities = [distance / total_distance for distance in distances]
    cumulative_probabilities = []
    for i in range(101):
        qi = 0
        for j in range(i):
            qi += probabilities[j]
        cumulative_probabilities.append(qi)

    return random.choices(population, cum_weights=cumulative_probabilities, k=101)

def generate_children_cross_over_order(parents):
    children = []
    size = len(parents[0])
    for i in range(101):
        ps = random.sample(parents, 2)
        r1 = random.randint(1, size-2)
        r2 = random.randint(r1, size-1)

        centerp1 = ps[0][r1:r2]
        centerp2 = ps[1][r1:r2]

        orderp1 = ps[0][r2:] + ps[0][:r2]
        orderp2 = ps[1][r2:] + ps[0][:r2]

        orderp1_wcen = []
        for x in orderp1:
            if x in centerp1:
                continue
            else:
                orderp1_wcen.append(x)

        orderp2_wcen = []
        for x in orderp2:
            if x in centerp2:
                continue
            else:
                orderp2_wcen.append(x)

        child1 = orderp1[0:r1] + centerp1 + orderp1[r2:]
        child2 = orderp2[0:r1] + centerp2 + orderp2[r2:]

        children.append(child1)
        children.append(child2)

    return children

def generate_children_cross_over_partially(parents):
    children = []
    size = len(parents[0])
    for i in range(101):
        ps = random.sample(parents, 2)
        r1 = random.randint(1, size-2)
        r2 = random.randint(r1, size-1)

        def one_offspring(p1, p2):
            offspring = [0] * size
            offspring[r1:r2] = p2[r1:r2]
            outsiders = [0] * size
            outsiders[0:r1] = p1[0:r1]
            outsiders[r2:] = p1[r2:]

            mapping = p1[r1:r2]
            
            for j in range(size):
                el = outsiders[j]
                if el == 0:
                    continue

                if el in offspring:
                    continue

                offspring[j] = el

            for j in range(size):
                if offspring[j] == 0:
                    if mapping:
                        offspring[j] = mapping.pop()
                    else:
                        break

            p2k = 0
            for j in range(size):
                if offspring[j] == 0:
                    for k in range(p2k, size):
                        nel = offspring[k]
                        if nel not in offspring:
                            offspring[j] = nel
                            p2k = k + 1
                            break
                        else:
                            continue

            return offspring

        child1 = one_offspring(ps[0], ps[1])
        child2 = one_offspring(ps[1], ps[0])

        children.append(child1)
        children.append(child2)

    return children

def generate_mutated_children_scramble(parents):
    children = []
    size = len(parents[0])
    for i in range(101):
        i = random.randint(0, size-1)
        j = random.randint(i+1, size)
        subset = parents[i][i:j+1]
        random.shuffle(subset)
        child = parents[i].copy()
        si = 0
        for k in range(i, j):
            child[k] = subset[si]
            si += 1
        
        children.append(child)

    return children

###

def generate_random_solution(data):
    solution = []
    for i in range(len(data)):
        solution.append(data[i][0])
    random.shuffle(solution)

    return solution

def distance(solution, data):
    sum = 0
    for i in range(len(solution)):
        if i == len(solution) - 1:
            sum += distance_between(solution[len(solution) - 1], solution[0], data)
        else:
            sum += distance_between(solution[i], solution[i+1], data)
    
    return round(sum, 2)

def distance_between(A, B, data):
    return math.sqrt(pow(data[B-1][1]-data[A-1][1], 2) + pow(data[B-1][2]-data[A-1][2], 2))

def string_solution(solution, distance):
    return f"{solution} - distance: {distance}"

start()