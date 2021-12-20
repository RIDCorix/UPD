import abc

class Tool(metaclass=abc.ABCMeta):
    def __init__(self, *args, **kwargs):
        self.init_tasks = []
        self.settings = {}

    def init_task(self, task_function):
        self.init_tasks.append(task_function)


class ToolSettings:
    def __init__():
        pass