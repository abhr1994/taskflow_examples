import logging
import os
import sys

logging.basicConfig(level=logging.ERROR)

self_dir = os.path.abspath(os.path.dirname(__file__))
top_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                       os.pardir,
                                       os.pardir))
sys.path.insert(0, top_dir)
sys.path.insert(0, self_dir)

from taskflow import engines
from taskflow.patterns import linear_flow as lf
from taskflow import task

# INTRO: in this example we create a dummy flow with a dummy task, and run
# it using a in-memory backend and pre/post run we dump out the contents
# of the in-memory backends tree structure (which can be quite useful to
# look at for debugging or other analysis).


class PrintTask(task.Task):
    def execute(self):
        print("Running '%s'" % self.name)

# Make a little flow and run it...
f = lf.Flow('root')
for alpha in ['a', 'b', 'c']:
    f.add(PrintTask(alpha))

e = engines.load(f)
e.compile()
e.prepare()

# After prepare the storage layer + backend can now be accessed safely...
backend = e.storage.backend

print("----------")
print("Before run")
print("----------")
print(backend.memory.pformat())
print("----------")

e.run()

print("---------")
print("After run")
print("---------")
for path in backend.memory.ls_r(backend.memory.root_path, absolute=True):
    value = backend.memory[path]
    if value:
        print("%s -> %s" % (path, value))
    else:
        print("%s" % (path))