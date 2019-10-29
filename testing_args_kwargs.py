from taskflow import engines
from taskflow import exceptions
from taskflow.patterns import linear_flow
from taskflow import task
from taskflow import retry
import subprocess as sp


class ConnectToServer(task.Task):
    def execute(self, ph_no, *args,**kwargs):
        print(args,kwargs,ph_no)

    def revert(self,*args,**kwargs):
        print("Wrong IP!!")

class Dog(task.Task):
    def execute(self, food, **kwargs):
        print("Dog task")
        print(food,kwargs)


class BitsAndPiecesTask(task.Task):
    def execute(self):
        print("BitsAndPiecesTask")
        return 'BITs', 'PIECEs'



dog = Dog(requires=("water", "grass"),inject={'food': 'food','grass':'grass','water':'water'})
flow = linear_flow.Flow('send_message' ).add(ConnectToServer('name',rebind=('phone_number','test_list')))
flow.add(dog)
flow.add(BitsAndPiecesTask(provides=('bits', 'pieces')))
try:
    print("Loading...")
    e = engines.load(flow,store={'phone_number': '8105760129','test_list':[1,2,3,4]})
    print("Compiling...")
    e.compile()
    print("Preparing...")
    e.prepare()
    print("Running...")
    result = e.run()
except Exception as e:
    print(e)

print(e.storage.fetch('bits'))