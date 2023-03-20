import csv
import random

filename="knapsack-100-items.csv"
weight_limit=200
runs=100

# Declaring the filename manually

#filename = input("Filename of the knapsack data set (leave empty for default 'knapsack-30-items.csv'): ")
#if filename == "": filename = "knapsack-30-items.csv"

# Load data from CSV file (for csv configurated files)
with open(filename, newline='') as csvfile:
    data_reader = csv.reader(csvfile, delimiter=',')
    next(data_reader) # skips header row
    data = [(int(row[0]), int(row[1])) for row in data_reader]

# Declaring the weight limit and runs manually inputted

#weight_limit = int(input("What's the weight limit? (-1 for default) (default: 100): "))
#if weight_limit < 0: weight_limit = 100
#runs = int(input("How many runs? (-1 for default) (default: 10): "))
#if runs < 0: runs = 10

# Define function to evaluate a solution
def evaluate(solution):
    total_value = 0
    total_weight = 0
    for i in range(len(solution)):
        if solution[i] == 1:
            total_value += data[i][0]
            total_weight += data[i][1]
    if total_weight > weight_limit:
        return -total_value
    else:
        return total_value

def evaluate_weight(solution):
    total_value = 0
    total_weight = 0
    for i in range(len(solution)):
        if solution[i] == 1:
            total_value += data[i][0]
            total_weight += data[i][1]
    
    return total_weight

# Define function to generate a random solution
def generate_random_solution():
    return [random.randint(0, 1) for _ in range(len(data))]

# Define function to find the next steepest neighbor
def find_next_steepest_neighbor(solution, current_value):
    best_value = current_value
    best_neighbor = None
    for i in range(len(solution)):
        neighbor = solution.copy()
        neighbor[i] = 1 - neighbor[i]
        neighbor_value = evaluate(neighbor)
        if neighbor_value > best_value:
            best_value = neighbor_value
            best_neighbor = neighbor
    return best_neighbor, best_value

def compute_average(values):
    if not values:
        return 0
    return sum(values) / len(values)

# runs = 100

print(f"Runs: {runs}")
print("---------------------------------------------------------------------------------\n")
values = []
best_solution = []

# Perform 100 runs of the algorithm
for run in range(runs):
    # Generate a random initial solution
    current_solution = generate_random_solution()
    current_value = evaluate(current_solution)
    
    # Iterate until no further improvement is possible
    while True:
        # Find the next steepest neighbor
        next_solution, next_value = find_next_steepest_neighbor(current_solution, current_value)
        
        # If no better neighbor is found, terminate
        if next_value == current_value:
            break
        
        # Otherwise, move to the next solution
        current_solution = next_solution
        current_value = next_value
        if (current_value > evaluate(best_solution)):best_solution = current_solution
        if(current_value > 0):values.append(current_value)
    
    # Check if the best solution found in the run is valid
    if evaluate(current_solution) < 0:
        msg1 = f"Run {run+1}: Best solution is not valid"
        with open(f"log_{filename}_weight-{weight_limit}_{runs}runs.txt", 'a') as logger:
            logger.write(msg1+"\n")
        print(msg1)
    else:
        msg2 = f"Run {run+1}: Weight = {evaluate_weight(current_solution)}/{weight_limit}, Value = {evaluate(current_solution)} Solution = {current_solution}"
        with open(f"log_{filename}_weight-{weight_limit}_{runs}runs.txt", 'a') as logger:
            logger.write(msg2+"\n")
        print(msg2)
    

msg_breaker = "---------------------------------------------------------------------------------\n"
with open(f"log_{filename}_weight-{weight_limit}_{runs}runs.txt", 'a') as logger:
            logger.write(msg_breaker+"\n")
print(msg_breaker)
msg3 = f"BEST SOLUTION: Weight = {evaluate_weight(best_solution)}/{weight_limit}, Value = {evaluate(best_solution)} Solution = {best_solution}"
with open(f"log_{filename}_weight-{weight_limit}_{runs}runs.txt", 'a') as logger:
            logger.write(msg3+"\n")
print(msg3)
print(msg_breaker)
msg4 = f"Average total value: {compute_average(values)}"
with open(f"log_{filename}_weight-{weight_limit}_{runs}runs.txt", 'a') as logger:
            logger.write(msg4+"\n")
print(msg4)
with open(f"log_{filename}_weight-{weight_limit}_{runs}runs.txt", 'a') as logger:
            logger.write("\n"+"Runs:"+str(runs)+"\n"+"Weight:"+str(weight_limit))

#print(values)