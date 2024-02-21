from Classes import RoundRobin
from Classes import Process

#set up variables
processes = []
data = [
    {"id": 1,"servetime": 75,"arrivaltime":0},
    {"id": 2,"servetime": 40,"arrivaltime":10},
    {"id": 3,"servetime": 25,"arrivaltime":10},
    {"id": 4,"servetime": 20,"arrivaltime":80}, 
    {"id": 5,"servetime": 45,"arrivaltime":85}
]

#instantiate processes
for process in data:
    processes.append(Process(process["id"], process["servetime"], process["arrivaltime"]))

#instantiate w/ time quantum 0, processes and 0 context switch
roundRobin = RoundRobin(10,processes,0)

roundRobin.begin()
roundRobin.printProcesses()
