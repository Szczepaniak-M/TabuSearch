from algorithms.Processor import Processor, load_data


def greedy_algorithm(test):
    processors = []
    tasks, processor_amount, tasks_amount = load_data(test)
    for i in range(processor_amount):
        processors.append(Processor(pk=i))
    tasks.sort(reverse=True)
    while tasks:
        min(processors).set_task(tasks.pop(0))
    timer = max(processors).time
    return timer, processors
