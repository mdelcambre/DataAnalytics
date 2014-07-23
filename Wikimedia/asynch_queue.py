"""
Implements the asynchronous queuing library in python as part of the Wikimedia
coding task. The task is summarized below. Pseudo-code not provided in doc
string

Your task is to write an asynchronous queuing library. You can write this
task in the language of your choice.

The code that illustrates the description of the task should be understood like
pseudo-code.
The task should occupy you about 3 hours; try to use as few additional high
level libraries as possible. Keep things simple and concentrate on fulfilling
the API contract, the queue should not need a storage layer.

The following signatures explain the semantics you must fulfill, but feel free
to add additional features that you feel are pragmatic, elegant, or awesome
opportunities to show off.

Queue Class with the following methods.

size()                  # returns the size of the queue
isRunning()             # returns if the queue is current executing
inFlight()              # returns the number of tasks executing
addTask(task)           # adds a task to the queue
addCallback(callback)   # adds a call back to be run when the queue has finished
start()                 # starts execution of the queue


Notes and comments from Mark Delcambre about the code:

It is noted that there is a limitation in CPython that does not allow for true
concurrency, due to the global lock. There are library implementations to get
around this implementation by calling subprocesses. However threading is still
very powerful for many tasks. Additionally if the function that is being called
executes a shell command, then this would allow for true concurrency.

The implementation of this tries to closely follow the pseudo-code requirements.
There are a couple of oddities with the callback function being passed to the
task. Since I am using a handler thread, this callback is not specifically
needed. Indeed because of this implementation there is a bug. If the tasks runs
successfully (no exception thrown) but does not call the callback function, the
queue will never stop running. This is one of the cases I perceive a benefit of
the handler thread, it can keep the queue running smoothly if the task
misbehaves.

If I had more time (and this were to be more developed), there are a couple of
features I would like to add.
The most obvious is keeping track of the results
of each task (exit code, exceptions thrown, etc.). I suspect that I would add a
ID to each task to track them better through the queue if this kind of logging
were to be implemented.
It might be nice to be able to stop the queue, simplest way is to use a flag
and check in the queue looper thread. Killing tasks that are already running
may require a different approach.


Currently the queue looper thread loops until all tasks have finished to run
the callback. This, intentionally, allows tasks to be added to the queue is
empty but a task is still running.
The queue handler thread could be rewritten to run until the queue is empty and
then quit. If you still want to be able to have new queue items added to an
empty queue, this could be handled easily by the task callback function with
simple logic.
"""

import threading        # for threading the tasks that currently being run
# There is a Queue library which I believe implements this already... :)


__author__ = "Mark Delcambre"
__copyright__ = "Copyright 2014, Mark Delcambre"
__license__ = "GPL"
__version__ = "0.1"

__email__ = "mark@delcambre.com"
__status__ = "Prototype"



class Queue():
    """Implements a asynchronous queue class.
    Tasks can be added to a queue and then the queue can be executed. The queue
    will loop through the queue and run a specified number of tasks at a time.
    Tasks must take the single argument of a callback function"""

    def __init__(self,threads):
        """Initializes the queue object. Takes the argument of how many tasks
        be run simultaneously, must be greater than 1."""

        # Check that the number of threads is a natural number.
        if int(threads) > 0:
            self.threads = threads
        else:
            raise Exception("Number of threads must be a natural number (>=1)")

        # initialize a few tracking variables used by the class
        self.tasks = list()
        self.running = False
        self.threads_active = 0
        self.qcallback = lambda: None # initialize the call back function

    def size(self):
        'Returns the number of items is the queue waiting to be run'
        return len(self.tasks)

    def isRunning(self):
        "Returns a boolean for if the queue is currently running"
        return self.running

    def addTask(self, task):
        """Adds a task to the queue, takes a callable function as argument. Task
        must take a callback function as the only argument"""

        # Check if the task is callable, otherwise through an exception
        if hasattr(task, '__call__'):
            # Adding to the front of the list allows pop to be used.
            # could use the python deque structure
            self.tasks.insert(0,task)
            return self
        else:
            raise Exception("Expected callable function to be passed in.")

    def inFlight(self):
            'Returns the number of running tasks'
            return self.threads_active

    def addCallback(self,callback):
        'Sets the callback function for when the queue finishes'

        # As before, check that the callback is a function
        if hasattr(callback, '__call__'):
            self.qcallback = callback
        else:
            raise Exception("Expected callable callback function")

    def task_finished(self):
        'Callback function when a function ends'
        self.threads_active -= 1 # Task finished, decrement threads by 1

    def run_task(self,task):
        'Runs the task at hand, handles if the task errors out.'

        # Using a try/except block to catch if the tasks throws an exception
        try:
            task(self.task_finished)
        except:
            #This allows us to handle errors differently from successfully
            # completed tasks in the future.
            self.task_finished()

    def run_queue(self):
        'Runs the actual queue. Should not be called directly'
        # loop while we still have tasks to run or there are still tasks running
        while self.threads_active > 0 or len(self.tasks) > 0:
            if self.threads_active >= self.threads or len(self.tasks) == 0:
                continue
            self.threads_active += 1
            # There is a chance that the thread will finish between while 
            temp_thread = threading.Thread(target=self.run_task, \
                                           args=(self.tasks.pop(),))
            temp_thread.start()

        # All threads have finished and no more in queue, stop running and run
        # queue callback
        self.running = False
        self.qcallback()

    def start(self):
        """Starts executing items in the queue."""

        if len(self.tasks) == 0 or self.running == True:
            return self
        queue_thread = threading.Thread(target=self.run_queue, args=())
        queue_thread.start()
        self.running = True


