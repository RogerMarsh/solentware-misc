# callthreadqueue.py
# Copyright 2013 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""This module provides the CallThreadQueue class which runs methods from
a queue in a dedicated thread and rejects requests to run methods while
the thread is running a method.

"""
import queue
import threading


class CallThreadQueue(object):
    """Provide a queue and a thread which runs methods placed on the queue.

    The maximum size of the queue is one.
    
    """

    def __init__(self):
        """Create the queue andstart the thread."""
        super(CallThreadQueue, self).__init__()
        self.queue = queue.Queue(maxsize=1)
        threading.Thread(target=self.__call_method, daemon=True).start()

    def __call_method(self):
        """Get method from queue, run it, and then wait for next method."""
        while True:
            try:
                method, args, kwargs = self.queue.get()
            except:
                self.queue.task_done()
                self.queue = None
                break
            method(*args, **kwargs)
            self.queue.task_done()

    def put_method(self, method, args=(), kwargs={}):
        """Append the method and it's arguments to the queue.

        method - the method to be run.
        args - passed to method as *args.
        kwargs - passed to method as **kwargs.

        The entry is a tuple:

        (method, args, kwargs).
        """
        self.queue.put((method, args, kwargs))
