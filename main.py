from algorithms.Processor import show
from algorithms.greedy_algorithm import greedy_algorithm
from algorithms.tabu_search import tabu_search
from instances.instance_generator import make_optimum_instance, make_random_instance

# test_file = 'instances/m25.txt'
# iterations = 35000
# tabu_length = 5

# test_file = 'instances/m50.txt'
# iterations = 20000
# tabu_length = 5

# test_file = 'instances/m50n1000.txt'
# iterations = 20000
# tabu_length = 5

# test_file = 'instances/m50n200.txt'
# iterations = 30000
# tabu_length = 5

# test_file = 'instances/m10n200.txt'
# iterations = 20000
# tabu_length = 1

# make_random_instance(400, 100, 1000)  # task_amount, processors_amount, max_task_time
# test_file = 'instances/random_instance.txt'
# iterations = 70000
# tabu_length = 5

print('Optimum result: ' + str(make_optimum_instance(400, 100, 1000)))  # task_amount, processors_amount, max_task_time
test_file = 'instances/optimum_instance.txt'
iterations = 70000
tabu_length = 5

result_time, processors = greedy_algorithm(test_file)
print('Result of LTP algorithm: ' + str(result_time) + '\n')
show(processors)

result_time, processors = tabu_search(test_file, iterations, tabu_length)
print('Result of Tabu Search: ' + str(result_time))
show(processors)
