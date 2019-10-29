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
from taskflow.patterns import unordered_flow as uf

from taskflow import task

class CallJohn(task.Task):
    def execute(self, john_number, *args, **kwargs):
        print("Calling John %s." % john_number)

    def revert(self, john_number, *args, **kwargs):
        print("Calling John %s and apologizing." % john_number)


class CallJim(task.Task):
    def execute(self, jim_number, *args, **kwargs):
        print("Calling jim %s." % jim_number)

    def revert(self, jim_number, *args, **kwargs):
        print("Calling Jim %s and apologizing." % jim_number)


class CallJoe(task.Task):
    def execute(self, joe_number, *args, **kwargs):
        raise IOError("Joe not home right now.")
        print("Calling joe %s." % joe_number)

    def revert(self, joe_number, *args, **kwargs):
        print("Calling Joe %s and apologizing." % joe_number)


class CallSuzzie(task.Task):
    def execute(self, suzzie_number, *args, **kwargs):
        raise IOError("Suzzie not home right now.")


# Create your flow and associated tasks (the work to be done).

u_flow = uf.Flow('simple-unordered').add(
    CallJim(inject={'jim_number': '8105760129'}),
    CallJoe(inject={'joe_number': '8660519397'}),
    CallSuzzie(inject={'suzzie_number': '9481075653'})
)

flow = lf.Flow('simple-linear').add(
    CallJohn(inject={'john_number': '8105760129'}),
    u_flow
)


try:
    # Now run that flow using the provided initial data (store below).
    taskflow.engines.run(flow, engine='parallel', executor='threaded', max_workers=2)
except Exception as e:
    print("Flow failed: %s" % e)