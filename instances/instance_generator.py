import random


def make_random_instance(task_amount=0, processors_amount=0, max_task_time=50):
    if task_amount == 0:
        task_amount = random.randint(1, 1000)
    if processors_amount == 0:
        processors_amount = round(random.randint(5, 20) / 100 * task_amount)

    with open("instances/random_instance.txt", "w") as file:
        file.write(str(processors_amount) + '\n')
        file.write(str(task_amount) + '\n')
        for i in range(task_amount):
            file.write(str(random.randint(5, max_task_time)) + '\n')


def make_instance_optimum(task_amount, processors_amount, max_task_time, file_name="instances/optimum_instance.txt"):
    tasks = []
    times = []
    for i in range(processors_amount):
        tasks.append([])
        times.append(0)
    for i in range(task_amount):
        tasks[i % processors_amount].append(random.randint(5, max_task_time))
    max_time = 0
    for i in range(processors_amount):
        for j in range(len(tasks[i])):
            times[i] += tasks[i][j]
        if times[i] > max_time:
            max_time = times[i]
    max_time += 1
    for i in range(processors_amount):
        tasks[i].append((max_time - times[i]))

    with open(file_name, "w") as file:
        file.write(str(processors_amount) + '\n')
        file.write(str(task_amount) + '\n')
        for i in range(processors_amount):
            for j in range(len(tasks[i])):
                file.write(str(tasks[i][j]) + '\n')
    return max_time
