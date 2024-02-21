class RR:
    def __init__(self, timeQuantum, processes, contextSwitch):
        self.timeQuantum = timeQuantum
        self.processes = processes
        self.contextSwitch = contextSwitch
        self.timeElapsed = 0

    #begin round robin sequence
    def begin(self):
        for i in range(0, len(processes)):
            #if more than full time quantum is remaining in process
                #round robin time elapsed += quantum
                #process updates - start time -1 check, ..... what else?
            #if process finished
                #
            #if less than full time quantum is remaining in process
                #incrememnt time elapsed with time reamining in process
                #process updates - start time -1 check, ..... what else?
            #increment time on RR

            #processes correctly instantiated?
            print(processes[i].id)
    def testStartTimes():
        for i in range(0, len(processes)):
            print(processes[i].startTime)

class Process:
    def __init__(self, id, serviceTime, arrivalTime):
        self.id = id
        self.serviceTime = serviceTime
        self.arrivalTime = arrivalTime
        self.startTime = -1
        self.initialWaitTime = 0
        self.endTime = 0
        self.totalWaitTime = 0
        self.turnAroundTime = 0

    #setters
    def setStartTime(self, time):
        self.startTime = time
    def setInitialWaitTime(self, time):
        self.initialWaitTime = time
    
    #incremental counts
    def setEndTime(self, time):
        self.selfEndTime += time
    def incrementTotalWaitTime(self, time):
        self.totalWaitTime += time
    def incrementTurnAroundTime(self, time):
        self.turnAroundTime += time
    
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
roundRobin = RR(0,processes,0)
#
roundRobin.begin()
