from taskflow import task
from taskflow import engines
from taskflow.patterns import linear_flow


######### Map Functor Task Example #########
def exec(x):
    return x*2

map_func = task.MapFunctorTask(functor=exec,requires=['a','b','c'],provides=('output_map'))
flow = linear_flow.Flow('test_mapfunctor').add(map_func)
e = engines.load(flow,store={'a':1,'b':2,'c':3})
e.run()
print(e.storage.fetch('output_map'))


######### Reduce Functor Task Example #########

reduce_func = task.ReduceFunctorTask(functor=lambda a,b:a+b,requires=['a','b','c'],provides=('output_reduce'))
flow = linear_flow.Flow('test_reducefunctor').add(reduce_func)
e = engines.load(flow,store={'a':1,'b':2,'c':3})
e.run()

print(e.storage.fetch('output_reduce'))
