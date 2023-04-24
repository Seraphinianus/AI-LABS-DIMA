import csv
import numpy as np
import random


def read_csv(file):
    weights = []
    values = []
    with open(file, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader)  # Skip the first two rows
        next(reader)
        num_items = 0
        for row in reader:
            weights.append(int(row[1]))
            values.append(int(row[2]))
            num_items += 1
    return weights, values, num_items


def fitness(solution, weights, values, weight_limit):
    total_weight = 0
    total_value = 0
    for i in range(len(solution)):
        if solution[i] == 1:
            total_weight += weights[i]
            total_value += values[i]
    if total_weight > weight_limit:
        return -1
    return total_value



def generate_neighbors(solution, tabu_list):
    neighbors = []
    for i in range(len(solution)):
        for j in range(i + 1, len(solution)):
            neighbor = solution.copy()
            neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
            if (i, j) not in tabu_list and (j, i) not in tabu_list:
                neighbors.append(neighbor)
    return neighbors


def knapsack(weights, values, weight_limit, tabu_size, num_iterations, num_items):
    curr_solution = list(range(num_items))
    random.shuffle(curr_solution)
    tabu_list = []
    best_solution = curr_solution
    best_fitness = fitness(curr_solution, weights, values, weight_limit)
    for i in range(num_iterations):
        neighbors = generate_neighbors(curr_solution, tabu_list)
        neighbor_fitness = [fitness(s, weights, values, weight_limit) for s in neighbors]
        best_neighbor = neighbors[np.argmax(neighbor_fitness)]
        best_neighbor_fitness = np.max(neighbor_fitness)
        if best_neighbor_fitness > best_fitness:
            best_solution = best_neighbor
            best_fitness = best_neighbor_fitness
        tabu_list.append((curr_solution.index(best_neighbor[0]), curr_solution.index(best_neighbor[1])))
        if len(tabu_list) > tabu_size:
            tabu_list.pop(0)
        curr_solution = best_neighbor
    return best_solution, best_fitness


def main():
    file = 'rucsac-20.csv'
    weights, values, num_items = read_csv(file)
    weight_limit = 524
    tabu_size = 10
    num_iterations = 1000
    solution, fitness = knapsack(weights, values, weight_limit, tabu_size, num_iterations, num_items)
    print(f"Solution: {solution}\nFitness: {fitness}")


if __name__ == '__main__':
    main()
