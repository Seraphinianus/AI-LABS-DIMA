import csv
import random

# Hard coding the files for this assignment.
files=["rucsac-20.csv", "rucsac-200.csv"]

# Taking input for the dataset
try:
    filename = input("(0 for default 20-item knapsack)\n"+
                    "(1 for default 200-item knapsack)\n"+
                    "(Any other CSV dataset in the same directory)\n"+
                    "Filename : ")
except ValueError:
    print("Input can only be: 0, 1 or a non-empty filename")
    

if (filename == "0"): 
    filename=files[0] 
    weight_limit = 524
else:
    if (filename == "1"): 
        filename=files[1]
        weight_limit = 112648
    else:
        weight_limit = int(input("What's the weight limit? (-1 for default) (default: 100): "))

#runs = int(input("How many runs? (-1 for default) (default: 10): "))

# I know it's a bit rudimentary, but hard coded run number
runs=1000

# Declaring the filename manually

#filename = input("Filename of the knapsack data set (leave empty for default 'knapsack-30-items.csv'): ")
#if filename == "": filename = "knapsack-30-items.csv"

# Load data from CSV file (for csv configurated files)
with open(filename, newline='') as csvfile:
    data_reader = csv.reader(csvfile, delimiter=',')
    next(data_reader) # skips header row
    next(data_reader)
    data = [(int(row[1]), int(row[2])) for row in data_reader]

#-----------------------------------------------------------------
# Declaring the weight limit and runs manually inputted

#weight_limit = int(input("What's the weight limit? (-1 for default) (default: 100): "))
#if weight_limit < 0: weight_limit = 100
#runs = int(input("How many runs? (-1 for default) (default: 10): "))
#if runs < 0: runs = 10
#-----------------------------------------------------------------


# Define function to evaluate a solution (fitness)
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

# Evaluating the weight of the solution
def evaluate_weight(solution):
    total_weight = 0
    for i in range(len(solution)):
        if solution[i] == 1:
            total_weight += data[i][1]
    return total_weight

# Generating a random solution
def generate_random_solution():
    return [random.randint(0, 1) for _ in range(len(data))]

# Function for next steepest neighbour
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

# Function for getting the overall average of the runs
def compute_average(values):
    if not values:
        return 0
    return sum(values) / len(values)


# Logging into a file 
#======================================================================
logfilename = f"log_{filename}_weight-{weight_limit}_{runs}runs.txt"

def log_message(msg, logfilename):
    with open(logfilename, 'a') as logger:
            logger.write(msg)
            if msg == "":
                logger.truncate(0)
                
log_message("", logfilename) # For clearing the logging file before writing to it

#======================================================================

# Some output formatting and declaring initial state of those variables
print(f"Runs: {runs}")
print("---------------------------------------------------------------------------------\n")
values = []
best_solution = []


# Perform {runs} runs of the algorithm
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
        
        # Getting the BEST solution out of all the runs
        if (current_value > evaluate(best_solution)):best_solution = current_solution
        
        # This is for the overall average 
        if(current_value > 0):values.append(current_value)
    
    
    # Check if the best solution found in the run is valid
    if evaluate(current_solution) < 0:
        msg1 = f"Run {run+1}: Best solution is not valid"
        log_message(msg1+"\n", logfilename)
        #with open(f"log_{filename}_weight-{weight_limit}_{runs}runs.txt", 'a') as logger:
        #    logger.write(msg1+"\n")
        print(msg1)
    else:
        msg2 = f"Run {run+1}: Weight = {evaluate_weight(current_solution)}/{weight_limit}, Value = {evaluate(current_solution)} Solution = {current_solution}"
        log_message(msg2+"\n", logfilename)
        #with open(f"log_{filename}_weight-{weight_limit}_{runs}runs.txt", 'a') as logger:
        #    logger.write(msg2+"\n")
        print(msg2)
    

# Logging the remaining details about the runs, such as BEST solution, total average for all valid solution in the runs,
# number of runs and weight limit assigned

msg_breaker = "\n-------------------------------------------------------------------------------------------------------------------------------\n"
log_message(msg_breaker, logfilename)
#with open(f"log_{filename}_weight-{weight_limit}_{runs}runs.txt", 'a') as logger:
#            logger.write(msg_breaker+"\n")
print(msg_breaker) 
msg3 = f"BEST SOLUTION: Weight = {evaluate_weight(best_solution)}/{weight_limit}, Value = {evaluate(best_solution)} Solution = {best_solution}"
log_message(msg3, logfilename)
#with open(f"log_{filename}_weight-{weight_limit}_{runs}runs.txt", 'a') as logger:
#            logger.write(msg3+"\n")
print(msg3)
log_message(msg_breaker+"\n", logfilename)
print(msg_breaker)
msg4 = f"Average total value: {compute_average(values)}"
#with open(f"log_{filename}_weight-{weight_limit}_{runs}runs.txt", 'a') as logger:
#            logger.write(msg4+"\n")
log_message(msg4, logfilename)
print(msg4)
#with open(f"log_{filename}_weight-{weight_limit}_{runs}runs.txt", 'a') as logger:
#            logger.write("\n"+"Runs:"+str(runs)+"\n"+"Weight:"+str(weight_limit))
log_message("\n"+"Runs:"+str(runs)+"\n"+"Weight limit:"+str(weight_limit) + "\n", logfilename)

#print(values)

# Master Logger:
# This file is going to be dedicated to logging the assignment's purpose. That would be an average of atleast 10 runs of the algorithm.
# I will be doing this manually, getting the BEST solutions in 10 runs, specifying the amount of runs in every simulation,
# along with their average value, worst BEST value and Overall averages for each of the runs.
#
# The runs are going to be configured as follows: 
# First part: 20-item knapsack.
# -> 10 runs
# -> 1k runs
# -> 100k runs
# Second part: 200-item knapsack.
# -> 10 runs
# -> 1k runs
# -> 100k runs

msgFinal = f"Table format: {evaluate_weight(best_solution)}/{weight_limit}; {evaluate(best_solution)}; {best_solution}"
log_message(msgFinal, logfilename)