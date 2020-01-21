class Processor:
    def __init__(self, other=None, pk=0):
        if other is None:
            self.tasks = []
            self.time = 0
            self.pk = pk
        else:
            self.tasks = other.tasks.copy()
            self.time = other.time
            self.deviation = other.deviation
            self.pk = other.pk

    def __lt__(self, other):
        return self.time < other.time

    def __eq__(self, other):
        return self.pk == other.pk

    def __str__(self):
        return str(self.time) + " -> " + str(self.tasks)

    def __copy__(self):
        return Processor(self)

    def set_task(self, task):
        self.tasks.append(task)
        self.time += task

    def swap_task(self, old_task, new_task):
        if old_task != 0:
            self.tasks.remove(old_task)
        if new_task != 0:
            self.tasks.append(new_task)
        self.time = self.time - old_task + new_task


def show(processors):
    for j in range(len(processors)):
        print(str(j + 1) + ' : ' + str(processors[j]))
    print('\n\n')


def load_data(test):
    tasks = []
    with open(test, "r") as file:
        processors_amount = int(file.readline().split()[0])
        tasks_amount = int(file.readline().split()[0])
        for val in file.read().split():
            tasks.append(int(val))
    return tasks, processors_amount, tasks_amount
