class RR:
    def __init__(self, timeQuantum, processes, contextSwitch):
        self.timeQuantum = timeQuantum
        self.processes = processes
        self.contextSwitch = contextSwitch
        self.timeElapsed = 0

    #begin round robin sequence
    def begin(self):
        for i in range(0, len(self.processes)):
            #
            #if more than full time quantum is remaining in process
                #round robin time elapsed += quantum
                #process updates - start time -1 check, ..... what else?
            #if process finished
                #
            #if less than full time quantum is remaining in process
                #incrememnt time elapsed with time reamining in process
                #process updates - start time -1 check, ..... what else?
            #increment time on RR
            #-------------------------------------------------------

            process = self.processes[i]
            #if process hasn't arrived yet, continue
            if process.arrivalTime > self.timeElapsed:
                continue
            #check if process has begun yet
            if process.startTime < 0 :
                process.startTime = self.timeElapsed
            #if more than full time quantum is remaining in process & process not completed
            if process.serviceTime > 10 and process.serviceTime != 0:
                self.timeElapsed += self.timeQuantum
                process.incrementTurnAroundTime(self.timeQuantum)
                print(process.remainingServiceTime)
                process.decrementServiceTime(self.timeQuantum)
                print(process.remainingServiceTime)



    def printProcesses(self): 
        for i in range(0, len(self.processes)):
            process = self.processes[i]
            print(f"Process id: {process.id}")
            print(f"Process service  time: {process.serviceTime}")
            print(f"Process arrival: {process.arrivalTime}\n")
            print(f"Process start time: {process.startTime}")
            print(f"Process remaining service time: {process.remainingServiceTime}")

            print(f"-------------------------------------\n")
            

class Process:
    def __init__(self, id, serviceTime, arrivalTime):
        self.id = id
        self.serviceTime = serviceTime
        self.arrivalTime = arrivalTime
        self.remainingServiceTime = serviceTime
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
    def setEndTime(self, time):
        self.selfEndTime += time

    #increment / decrement funcs
    def incrementTotalWaitTime(self, time):
        self.totalWaitTime += time
    def incrementTurnAroundTime(self, time):
        self.turnAroundTime += time
    def decrementServiceTime(self, time):
        self.remainingServiceTime -= time
    
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
roundRobin = RR(10,processes,0)

roundRobin.begin()
roundRobin.printProcesses()
