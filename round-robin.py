class RR:
    def __init__(self, timeQuantum, processes):
        self.timeQuantum = timeQuantum
        self.processes = []


    #function for round robin logic
    def createRoundRobin():
        print("Round robin created. Process id of first process passed: " + str(processes[0].id))

class Process:
    def __init__(self, id, serviceTime, arrivalTime):
        self.id = id
        self.serviceTime = serviceTime
        self.arrivalTime = arrivalTime
        self.startTime = 0
        self.initialWaitTime = 0
        self.selfEndTime = 0
        self.totalWaitTime = 0
        self.turnAroundTime = 0

    #set start time
    def setStartTime(time):
        startTime = time




processes = []
firstProcess = Process(1, 75, 0)
processes.append(firstProcess)


roundRobin = RR(0,[processes])

RR.createRoundRobin()