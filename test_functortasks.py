from taskflow import task
from taskflow import engines
from taskflow.patterns import linear_flow

def exec(x):
    print(x*2)
    raise IOError
def rev(x,*args,**kwargs):
    print("In revert method")

func_task = task.FunctorTask(execute=exec,revert=rev,name="samplefunctor",inject={"x":2})

flow = linear_flow.Flow('send_message').add(func_task)
e = engines.load(flow)
e.run()