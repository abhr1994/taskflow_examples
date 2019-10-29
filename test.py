from taskflow import engines
from taskflow import exceptions
from taskflow.patterns import linear_flow
from taskflow import task
import random


class CallOnPhone(task.Task):
    default_provides = 'was_dialed'

    def execute(self, phone_number):
        print("Calling %s" %phone_number)
        if random.choice([1, 0]) == 0:
            return True
        else:
            a = 1/0

    def revert(self,phone_number,result,flow_failures):
        if result:
            print("Hanging up on %s" % phone_number)


test = linear_flow.Flow("testing-taskflow")
abc = CallOnPhone("first_task",inject={'phone_number': '8105760129'})
test.add(abc)

try:
    print("Loading...")
    e = engines.load(test,engine='parallel', executor='threaded')
    print("Compiling...")
    e.compile()
    print("Preparing...")
    e.prepare()
    print("Running...")
    e.run()
    print("Done: %s" % e.statistics)
except Exception as e:
    print(e)



