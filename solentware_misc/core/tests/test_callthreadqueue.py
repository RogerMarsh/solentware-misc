# test_callthreadqueue.py
# Copyright 2021 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""callthreadqueue tests"""

import unittest

from .. import callthreadqueue


class CallThreadQueue(unittest.TestCase):
    def setUp(self):
        pass  # self.callthreadqueue = callthreadqueue.CallThreadQueue()

    def tearDown(self):
        pass

    def test_001___init___001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"__init__\(\) takes 1 positional argument ",
                    "but 2 were given$",
                )
            ),
            callthreadqueue.CallThreadQueue,
            *(None,),
        )

    def test_002___call_method_001(self):
        threadqueue = callthreadqueue.CallThreadQueue()
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"__call_method\(\) takes 1 positional argument ",
                    "but 2 were given$",
                )
            ),
            threadqueue.__call_method,
            *(None,),
        )

    def test_002___call_method_002(self):
        threadqueue = callthreadqueue.CallThreadQueue()
        threadqueue.queue.put((None))

    def test_002___call_method_003(self):
        def m():
            x = 0

        threadqueue = callthreadqueue.CallThreadQueue()
        threadqueue.queue.put((m, (), {}))

    def test_003_put_method_001(self):
        threadqueue = callthreadqueue.CallThreadQueue()
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"put_method\(\) missing 1 required positional argument: ",
                    "'method'$",
                )
            ),
            threadqueue.put_method,
        )

    def test_003_put_method_002(self):
        threadqueue = callthreadqueue.CallThreadQueue()
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"put_method\(\) got an unexpected keyword argument ",
                    "'badkey'$",
                )
            ),
            threadqueue.put_method,
            *(None,),
            **dict(args=(), kwargs={}, badkey=None),
        )

    def test_003_put_method_003(self):
        def m():
            x = 0

        threadqueue = callthreadqueue.CallThreadQueue()
        threadqueue.put_method(m)


if __name__ == "__main__":
    runner = unittest.TextTestRunner
    loader = unittest.defaultTestLoader.loadTestsFromTestCase
    runner().run(loader(CallThreadQueue))
