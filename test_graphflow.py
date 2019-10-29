from taskflow import task
from taskflow import engines
from taskflow.patterns import graph_flow
from taskflow.patterns import linear_flow

def allow(history):
    print(history)
    return False

class Call(task.Task):
    def execute(self, number):
        print("Calling %s %s." % (self.name,number))
        if number == 100:
            raise Exception("Wrong number!")
        else:
            print("Hello %s" %self.name)

    def revert(self, number, **kwargs):
        print("Wrong number, apologizing.")


t1 = Call("Abhishek",inject={"number":"8105760129"})
t2 = Call("Akshay",inject={"number":"8660519397"})
t3 = Call("Appa",inject={"number":"9449412077"})
t4 = Call("Amma",inject={"number":"9481075653"})
t5 = Call("Abhi Jio",inject={"number":"8660519397"})
t6 = Call("Jyothi Jio",inject={"number":"9123412345"})
t7= Call("Appa Jio",inject={"number":"9123412345"})

g_f = graph_flow.Flow("test_graphflow")
flow = linear_flow.Flow('test_lf').add(t7)

g_f.add(t1,t2,t3,t4,t5,t6,flow)
g_f.link(t1,t2)
g_f.link(t1,t3)
g_f.link(t2,t4)
g_f.link(t3,t4,decider=allow,decider_depth='FLOW')
g_f.link(t4,t5)
g_f.link(t5,t6)
g_f.link(t6,flow)

e = engines.load(g_f)
e.run()



#Targeted Flow

print("\n #####Example for Targeted Graph Flow#####\n")
targetedg_f = graph_flow.TargetedFlow("test_targetedgraphflow")
targetedg_f.add(t1,t2,t3,t4,t5)
targetedg_f.link(t1,t2)
targetedg_f.link(t2,t3)
targetedg_f.link(t2,t4)
targetedg_f.link(t4,t5)
targetedg_f.set_target(t5)
e = engines.load(targetedg_f)
#e = engines.load(targetedg_f,engine='workers')

e.run()
print("Done")