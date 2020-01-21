import copy

from algorithms.Processor import Processor, load_data
from math import ceil
from random import randrange


def tabu_search(test_file, iterations, tabu_length):
    # read data
    tasks, processors_amount, tasks_amount = load_data(test_file)
    random_ltp_length = ceil(tasks_amount * 0.05)

    # determine optimum
    size = 0
    for i in tasks:
        size += i
    optimum = max(ceil(size / processors_amount), max(tasks))

    # variable initialization
    optimum_processors = []
    short_tabu = []
    long_tabu = []
    max_time = size
    prev_iteration_max_time = size
    same_max_time_counter = 0

    # initialise processors using randomized LTP algorithm
    processors = init_schedule(tasks, processors_amount, random_ltp_length)
    iteration_max_time = max(processors).time
    if iteration_max_time == optimum:  # if we find optimum during randomized LTP algorithm
        return optimum, optimum_processors
    elif iteration_max_time < max_time:  # better solution but not optimum
        optimum_processors = copy.deepcopy(processors)
        max_time = iteration_max_time

    for i in range(iterations):
        processors.sort()

        # find processor with shortest time
        index = 0
        while True:
            if processors[index] not in long_tabu and processors[index] not in short_tabu:
                short_time_processor = processors[index]
                break
            else:
                index += 1

        # find processor with longest time
        index = -1
        while True:
            if processors[index] not in long_tabu and processors[index] not in short_tabu:
                long_time_processor = processors[index]
                break
            else:
                index -= 1

        # swap tasks and update same_max_time_counter
        same_max_time_counter = swap(short_time_processor, long_time_processor, optimum, same_max_time_counter)

        # update tabu lists
        short_tabu.append(short_time_processor)
        long_tabu.append(long_time_processor)
        if tabu_length < len(short_tabu):
            short_tabu.pop(0)

        if 2 * tabu_length < len(long_tabu):
            long_tabu.pop(0)
        iteration_max_time = max(processors).time

        if iteration_max_time == optimum:  # if we find optimum during iterations
            return optimum, optimum_processors
        elif iteration_max_time < max_time:  # if we find better solution but not optimum
            optimum_processors = copy.deepcopy(processors)
            max_time = iteration_max_time
            same_max_time_counter = 0
        elif iteration_max_time == prev_iteration_max_time:  # if we find the same solution as previous
            same_max_time_counter += 1

        prev_iteration_max_time = iteration_max_time

    return max_time, optimum_processors


# randomized LTP algorithm
def init_schedule(tasks, processor_amount, random_ltp_length):
    processors = []
    tasks_copy = tasks.copy()
    for i in range(processor_amount):
        processors.append(Processor(pk=i))

    tasks_copy.sort(reverse=True)
    while tasks_copy:
        if len(tasks_copy) >= random_ltp_length:
            index = randrange(0, random_ltp_length, 1)
        else:
            index = randrange(0, len(tasks_copy), 1)
        min(processors).set_task(tasks_copy.pop(index))
    return processors


# function to swapping tasks between processors
def swap(short_time_processor, long_time_processor, optimum, same_max_time_counter):
    return_counter = same_max_time_counter
    if same_max_time_counter < 200:  # if algorithm is not in local minimum do the best swap
        short_task, long_task = choose_task(short_time_processor, long_time_processor, optimum)
    else:  # if algorithm is in local minimum too long then do random swap
        short_task, long_task = random_choose_task(short_time_processor, long_time_processor, optimum)
        return_counter = 0
    short_time_processor.swap_task(short_task, long_task)
    long_time_processor.swap_task(long_task, short_task)
    return return_counter


# function to choose the best tasks to swap from given processors
def choose_task(short_time_processor, long_time_processor, optimum):
    # adding tasks with time equals 0
    short_tasks = short_time_processor.tasks.copy()
    short_tasks.append(0)
    long_tasks = long_time_processor.tasks.copy()
    long_tasks.append(0)

    chosen_short_task = 0
    chosen_long_task = 0
    # counting deviation from optimum
    deviation_short_time_processor = abs(optimum - short_time_processor.time)
    deviation_long_time_processor = abs(optimum - long_time_processor.time)

    # looking for tasks which swapping make the smallest sum of deviation
    for short_task in short_tasks:
        for long_task in long_tasks:
            current_deviation_short_time_processor = abs(optimum - (short_time_processor.time - short_task + long_task))
            current_deviation_long_time_processor = abs(optimum - (long_time_processor.time + short_task - long_task))
            if deviation_short_time_processor + deviation_long_time_processor > \
                    current_deviation_short_time_processor + current_deviation_long_time_processor:
                chosen_short_task = short_task
                chosen_long_task = long_task
                deviation_short_time_processor = current_deviation_short_time_processor
                deviation_long_time_processor = current_deviation_long_time_processor
    return chosen_short_task, chosen_long_task


# function to choose random tasks to swap from given processors (to leave local minimum)
def random_choose_task(short_time_processor, long_time_processor, optimum):
    # adding tasks with time equals 0
    short_tasks = short_time_processor.tasks.copy()
    short_tasks.append(0)
    long_tasks = long_time_processor.tasks.copy()
    long_tasks.append(0)

    # time on each processor after random swap cannot be worse than the worst case using LPT algorithm
    max_time = optimum * 4 / 3
    current_time = max_time + 1
    chosen_short_task = 0
    chosen_long_task = 0
    while current_time > max_time:
        index_short_task = randrange(0, len(short_tasks), 1)
        chosen_short_task = short_tasks[index_short_task]
        index_long_task = randrange(0, len(long_tasks), 1)
        chosen_long_task = long_tasks[index_long_task]
        current_time = max(short_time_processor.time - chosen_short_task + chosen_long_task,
                           long_time_processor.time + chosen_short_task - chosen_long_task)
    return chosen_short_task, chosen_long_task
