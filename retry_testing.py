import logging
import os
import sys


logging.basicConfig(level=logging.ERROR)

top_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                       os.pardir,
                                       os.pardir))
sys.path.insert(0, top_dir)

import taskflow.engines
from taskflow.patterns import linear_flow as lf
from taskflow import retry
from taskflow import task

class Sampletask(task.Task):
    def execute(self):
        print("Executing sample task ")
    def revert(self, *args, **kwargs):
        print("Reverting sample task ")


class CallJim(task.Task):
    def execute(self, jim_number):
        print("Calling jim %s." % jim_number)
        if jim_number != 555:
            raise Exception("Wrong number!")
        else:
            print("Hello Jim!")

    def revert(self, jim_number, **kwargs):
        print("Wrong number, apologizing.")

class MyRetry(retry.ForEachBase):

    default_provides = 'value'

    def on_failure(self, values, history, *args, **kwargs):
        print('In on_failure method of retry')
        print(list(history))
        return retry.RETRY

    def execute(self, values, history, *args, **kwargs):
        print('In execute method of retry')
        print(list(history))
        return self._get_next_value(values, history)

    def revert(self, history, *args, **kwargs):
        print('In revert method of retry')
        print(list(history))


flow = lf.Flow('retrying-linear',
               retry=MyRetry(rebind=['phone_directory'],provides='jim_number')).add(Sampletask(),CallJim())

taskflow.engines.run(flow, store={'phone_directory': [333, 444, 555, 666]})
