import time
from threading import Thread

from queue import Queue


class StateHandler:
    def __init__(self):
        self.access_queue = Queue()
        self.active_task = None

    # Access and modify the StateHandler's data in a thread-safe, FIFO manner
    def add_task(self, function, *args, **kwargs):
        task = Task(self, function, *args, **kwargs)
        self.access_queue.put(task)
        if not self.active_task:
            self.run_next_task()

    # Start the next thread waiting in the queue
    def run_next_task(self):
        if not self.active_task:
            if not self.access_queue.empty():
                self.active_task = self.access_queue.get()
                self.active_task.start()
            else:
                self.active_task = None


# All modifications of StateHandler data after initialization should be encapsulated as a task for thread-safety
# purposes. Doing so only allows one modification of StateHandler at a time without blocking the entire program as would
# happen with a Lock object (?)
class Task(Thread):
    def __init__(self, state_handler, function, *args, **kwargs):
        Thread.__init__(self)
        self.state_handler = state_handler
        self.function = function
        self.args = args
        self.kwargs = kwargs

    def run(self):
        self.function(*self.args, **self.kwargs)
        self.state_handler.active_task = None
        self.state_handler.run_next_task()


# Temporary debug functions
def foo():
    time.sleep(5)


def bar(a, b="1"):
    print(a, b)

