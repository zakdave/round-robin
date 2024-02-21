class RoundRobin:
    def __init__(self, timeQuantum, processes, contextSwitch):
        self.timeQuantum = timeQuantum
        self.processes = processes
        self.contextSwitch = contextSwitch
        self.timeElapsed = 0
        self.queue = []

    #begin round robin sequence
    def begin(self):
        #initialize queue
        self.setQueue()

        while len(self.queue) > 0:
            queueLength = len(self.queue)
            for i in range(0, queueLength):
                
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

                process = self.queue[i]

                
                #if process hasn't arrived yet, continue
                if process.arrivalTime > self.timeElapsed:
                    continue

                #check if process is ready, set start time
                if process.startTime < 0 :
                    process.startTime = self.timeElapsed
                
                #check for partial time quantum
                if process.remainingServiceTime < self.timeQuantum and process.remainingServiceTime >= 0:
                    #decrement remaining service time by difference of time quantum
                    process.decrementServiceTime(self.timeQuantum - process.remainingServiceTime)


                #if more than full time quantum is remaining in process & process not completed
                if process.remainingServiceTime >= self.timeQuantum and process.remainingServiceTime >= 0:
                    self.timeElapsed += self.timeQuantum
                    process.decrementServiceTime(self.timeQuantum)
                #check for partial time quantum
                
                #process ended? pop from queue
                if process.remainingServiceTime == 0:
                    self.removeFromQueue(process.id)
                    break




    #set queue, queue is processes as they are ran, processes are beginning processes
    def setQueue(self):
        for process in self.processes:
            self.queue.append(process)

    #enumerate queue, remove by id
    def removeFromQueue(self, id):
            for i, process in enumerate(self.queue):
                if process.id == id:
                    self.queue.pop(i)
                    break

                

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
            

class Process:
    def __init__(self, id, serviceTime, arrivalTime):
        self.id = id

        #length of process running time
        self.serviceTime = serviceTime

        #time process gets to scheduler
        self.arrivalTime = arrivalTime

        #decremented value of service time
        self.remainingServiceTime = serviceTime

        #negative for readable if statement, can't be 0
        self.startTime = -1

        #start time - wait time, how long process waited in queue
        self.initialWaitTime = 0

        #when process ended
        self.endTime = 0

        #how long did the process wait before being finished
        # endtime - servicetime - arivaltime
        self.totalWaitTime = 0

        #end time - arrival time, should be calculated at the end
        self.turnAroundTime = 0

    #setters
    def setStartTime(self, time):
        self.startTime = time
    def setInitialWaitTime(self, time):
        self.initialWaitTime = time
    def setEndTime(self, time):
        self.selfEndTime = time

    #increment / decrement funcs
    def incrementTotalWaitTime(self, time):
        self.totalWaitTime += time
    def incrementTurnAroundTime(self, time):
        self.turnAroundTime += time
    def decrementServiceTime(self, time):
        self.remainingServiceTime -= time