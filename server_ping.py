from taskflow import engines
from taskflow import exceptions
from taskflow.patterns import linear_flow
from taskflow import task
from taskflow import retry
import subprocess as sp


class ConnectToServer(task.Task):
    def execute(self, ip):
        print("Connecting to %s" % ip)
        status, result = sp.getstatusoutput("ping -c1 -W2 "+str(ip))
        if status == 0:
            print("Connection to %s succesfull!!!" %ip)
        else:
            raise Exception("Wrong IP!")

    def revert(self,ip,**kwargs):
        print("Wrong IP!!")



flow = linear_flow.Flow('send_message',retry=retry.ParameterizedForEach(rebind={'values': 'server_ips'},provides='ip')).add(ConnectToServer())

try:
    print("Loading...")
    e = engines.load(flow,store={'server_ips':['192.168.1.1', '192.168.1.2', '172.30.1.60', '192.168.1.3']})
    print("Compiling...")
    e.compile()
    print("Preparing...")
    e.prepare()
    print("Running...")
    e.run()
except Exception as e:
    print(e)

