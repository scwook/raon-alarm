import pvaccess

c = pvaccess.Channel('scwook:ai1')

def echo(x):
    print('Val', x)

c.subscribe('echo', echo)
c.startMonitor()
