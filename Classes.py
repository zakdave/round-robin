class RoundRobin:
    def __init__(self, timeQuantum, data, contextSwitch):
        self.timeQuantum = timeQuantum
        self.processes = self.intializeProcesses(data)
        self.contextSwitch = contextSwitch
        self.timeElapsed = 0
        
        self.queue = []

    #run round robin sequence
    def run(self):
        #initialize queue
        self.setQueue()

        while len(self.queue) > 0:
            queueLength = len(self.queue)
            for i in range(0, queueLength):

                process = self.queue[i]
    
                #if process hasn't arrived yet, continue
                if process.arrivalTime > self.timeElapsed:
                    continue

                #check if process is ready, set start time, set initial wait time
                if process.startTime < 0 :
                    process.setStartTime(self.timeElapsed)

                
                #check for partial time quantum
                if process.remainingServiceTime < self.timeQuantum and process.remainingServiceTime >= 0:
                    #decrement remaining service time by difference of time quantum, record time in RR
                    process.decrementRemainingServiceTime(self.timeQuantum - process.remainingServiceTime)
                    self.incrementTimeElapsed(self.timeQuantum - process.remainingServiceTime)


                #if more than or equal to full time quantum is remaining in process & process not completed, record time in RR
                if process.remainingServiceTime >= self.timeQuantum and process.remainingServiceTime >= 0:
                    process.decrementRemainingServiceTime(self.timeQuantum)
                    self.incrementTimeElapsed(self.timeQuantum)
                
                
                #process ended? pop from queue
                if process.remainingServiceTime == 0:
                    process.setEndTime(self.timeElapsed)
                    self.removeFromQueue(process.id)
                    break

        #finally, loop over processes to update their data
        for process in self.processes:
            process.calculateMetrics()


    #set queue, queue is processes as they are ran, processes are beginning processes
    def setQueue(self):
        for process in self.processes:
            self.queue.append(process)

    def intializeProcesses(self, data):
        processes = []
        for process in data:
            processes.append(Process(process["id"], process["servetime"], process["arrivaltime"]))
        return processes

    #enumerate queue, remove by id
    def removeFromQueue(self, id):
            for i, process in enumerate(self.queue):
                if process.id == id:
                    self.queue.pop(i)
                    break
    
    def incrementTimeElapsed(self, time):
        self.timeElapsed += time

    def printProcesses(self): 
        for i in range(0, len(self.processes)):
            process = self.processes[i]
            print(f"Process id: {process.id}")
            print(f"Process service  time: {process.serviceTime}")
            print(f"Process arrival: {process.arrivalTime}\n")
            print(f"Process start time: {process.startTime}")
            print(f"Process initial wait time: {process.initialWaitTime}")
            print(f"Process end time: {process.endTime}")
            print(f"Process totalWaitTime: {process.totalWaitTime}")
            print(f"Process turnAroundTime: {process.turnAroundTime}")
            print(f"-------------------------------------\n")

    def createTable():
        #use pandas or prettytable to loop through data and output data for all processes 
        return
    
class Process:
    def __init__(self, id, serviceTime, arrivalTime):
        self.id = id

        #length of process running time
        self.serviceTime = serviceTime

        #time process gets to scheduler
        self.arrivalTime = arrivalTime

        #decremented value of service time
        self.remainingServiceTime = serviceTime

        #negative for readable if statement, shouldn't be 0
        self.startTime = -1

        #start time - arrival time - how long process waited in queue
        self.initialWaitTime = 0

        #when process ended
        self.endTime = 0

        ##endtime - servicetime - arivaltime - how long did the process idle total
        self.totalWaitTime = 0

        #end time - arrival time, how long did the whole thing take?
        self.turnAroundTime = 0

    #setters and calculations
    def setStartTime(self, time):
        self.startTime = time
    def setInitialWaitTime(self, time):
        self.initialWaitTime = time
    def setEndTime(self, time):
        self.endTime = time

    def decrementRemainingServiceTime(self, time):
        self.remainingServiceTime -= time

    def calculateMetrics(self):
        #start time - arrival time -  how long process waited in queue
        self.initialWaitTime = self.startTime - self.arrivalTime

        #endtime - servicetime - arivaltime - how long did the process idle total
        self.totalWaitTime = self.endTime - self.serviceTime - self.arrivalTime

        #end time - arrival time, how long did the whole thing take?
        self.turnAroundTime = self.endTime - self.arrivalTime