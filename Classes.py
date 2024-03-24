from rich.console import Console
from rich.table import Table

class RoundRobin:
    def __init__(self, timeQuantum, data, contextSwitch):
        self.timeQuantum = timeQuantum
        self.processes = self.setProcesses(data)
        self.contextSwitch = contextSwitch
        self.timeElapsed = 0
        self.queue = []
        self.runningProcessId = -1
        self.avgWaitTime = 0
        self.avgTRDTime = 0

    #run round robin sequence
    def runRR(self):

        #set queue to all process for traditional rr
        self.queue = self.setQueue(self.processes)

        #while a queue exists
        while self.queue:

            #increment clock when idle
            unarrivedCount = 0
            for process in self.queue:
                if process.arrivalTime > self.timeElapsed:
                    unarrivedCount += 1
            if unarrivedCount == len(self.queue):
                #print('time elapsed: 1')
                self.incrementClock(1)

            #begin looping through queue
            for i in range(0, len(self.queue)):
                process = self.queue[i]
    
                #if process hasn't arrived yet, continue
                if process.arrivalTime > self.timeElapsed:
                    continue

                #check if process is ready, set start time, set initial wait time
                if process.startTime < 0 :
                    process.setStartTime(self.timeElapsed)
                
                #check for partial time quantum
                if process.remainingServiceTime < self.timeQuantum:

                    #decrement remaining service time by difference of time quantum,
                    #print(f'p{process.id} starting at {self.timeElapsed}')
                    partialTimeQuantum = process.remainingServiceTime

                    process.decrementRemainingServiceTime(partialTimeQuantum)
                    self.incrementClock(partialTimeQuantum)

                    #print(f'p{process.id} ending at {self.timeElapsed}')
                    if process.remainingServiceTime == 0:
                        process.setEndTime(self.timeElapsed)

                #if more than or equal to full time quantum is remaining in process & process not completed, record time in RR
                if process.remainingServiceTime >= self.timeQuantum:
                    #print(f'p{process.id} starting at {self.timeElapsed}')
                    
                    process.decrementRemainingServiceTime(self.timeQuantum)
                    self.incrementClock(self.timeQuantum)

                    #check for process ended
                    if process.remainingServiceTime == 0:
                        process.setEndTime(self.timeElapsed)
                    #print(f'p{process.id} ending at {self.timeElapsed} process has {process.remainingServiceTime} remaining')

                if len(self.queue) > 1:
                        self.incrementClock(self.contextSwitch)
                        #print(f'context switch ending at {self.timeElapsed}')

                #pop from queue
                if process.remainingServiceTime == 0:
                    self.removeFromQueue(process.id)
                    break

        #finally, loop over processes to update their data
        for process in self.processes:
            process.calculateMetrics()

        #calculate avagerages
        self.setAvgerateWait()
        self.setAverageTRDTime()

        #output results
        #self.createTable()
        print(f'Trad RR - Avg Wait: {self.avgWaitTime} Avg TRD: {self.avgTRDTime}')

    def runSQRR(self):
        incomplete = True

        while incomplete:
            #set queue for arrived processes, sort based on ST / RST
            completedCount = 0

            #set queue & check for completion
            for process in self.processes:
                if process.arrivalTime <= self.timeElapsed and process.queued == False:
                    process.queued = True
                    self.queue.append(process)
                if process.remainingServiceTime == 0 and process.queued == True:
                    completedCount+=1
                if completedCount == len(self.processes):
                    incomplete = False
                    break


            #increment idle clock
            if len(self.queue) == 0:
                #print('empty queue: time incremented')
                self.incrementClock(1)

            #sort by servicetime
            self.queue.sort(key = lambda process : process.serviceTime)

            #set time quantum to average of service times, rounded down
            totalServiceTimes = 0
            for process in self.queue:
                totalServiceTimes += process.serviceTime
            self.updateTimeQuantum(totalServiceTimes // 2)

            #run processes in queue
            for process in self.queue:

                #determine computing time
                timeToRun = min(process.remainingServiceTime, self.timeQuantum)

                #switch context if necessary
                if self.runningProcessId > 0 and process.id != self.runningProcessId:
                    #print(f'context switched at {self.timeElapsed} to {self.timeElapsed + self.contextSwitch}')
                    self.incrementClock(self.contextSwitch)

                #update RST and clock
                if process.startTime < 0:
                    process.setStartTime(self.timeElapsed)
                    #print(f'start time set for p{process.id} at {self.timeElapsed}')
                #print(f'p{process.id} started at {self.timeElapsed} to run for {timeToRun}')
                self.runningProcessId = (process.id)
                process.decrementRemainingServiceTime(timeToRun)
                self.incrementClock(timeToRun)
                
                #set end time for process
                if process.remainingServiceTime == 0:
                    process.setEndTime(self.timeElapsed)
                    self.removeFromQueue(process.id)
                    #print(f'p{process.id} popped from queue at {self.timeElapsed}')         

        #execute processes in queue and exit
                    
        #finally, loop over processes to update their data
        for process in self.processes:
            process.calculateMetrics()

        #calculate avagerages
        self.setAvgerateWait()
        self.setAverageTRDTime()
        
        #output results
        #self.createTable()
        print(f'SQRR - Avg Wait: {self.avgWaitTime} Avg TRD: {self.avgTRDTime}')

    #set queue, RR.queue holds the processes as they run whereas RR.processes contains all processes throughout the RR lifecycle
    def setQueue(self, processes):
        queue = []
        for process in processes:
            queue.append(process)
        return queue

    def setProcesses(self, data):
        processes = []
        for process in data:
            processes.append(Process(process["id"], process["serviceTime"], process["arrivalTime"]))
        return processes

    def updateTimeQuantum(self, quantum):
        self.timeQuantum = quantum

    #enumerate queue, remove by id
    def removeFromQueue(self, id):
            for i, process in enumerate(self.queue):
                if process.id == id:
                    self.queue.pop(i)
                    break

    def incrementClock(self, time):
        self.timeElapsed += time

    def setAvgerateWait(self):
        waitSum = 0
        for process in self.processes:
            waitSum+= process.totalWaitTime
        avgWait = waitSum / len(self.processes)
        self.avgWaitTime = avgWait
    
    def setAverageTRDTime(self):
        trdSum = 0
        for process in self.processes:
            trdSum += process.turnAroundTime
        avgTrd  = trdSum / len(self.processes)
        self.avgTRDTime = avgTrd

    #create table using rich
    def createTable(self):
        table = Table(title=f'Round Robin - Context Switch: {self.contextSwitch} Time Quantum: {self.timeQuantum}')
        table.add_column("Process Id", justify="right")
        table.add_column("Service Time", justify="right")
        table.add_column("Arrival Time", justify="right")
        table.add_column("Start Time", justify="right")
        table.add_column("End Time", justify="right")
        table.add_column("Initial Wait Time", justify="right")
        table.add_column("Total Wait Time", justify="right")
        table.add_column("Turn Around Time", justify="right")

        for process in self.processes:
            table.add_row(
                f"{process.id}",
                f"{process.serviceTime}",
                f"{process.arrivalTime}",
                f"{process.startTime}",
                f"{process.endTime}", 
                f"{process.initialWaitTime}",
                f"{process.totalWaitTime}",
                f"{process.turnAroundTime}"
            )

        console = Console()
        console.print(table)
    
class Process:

    def __init__(self, id, serviceTime, arrivalTime):
        self.id = id

        #aka burst time
        self.serviceTime = serviceTime

        #time process gets to scheduler
        self.arrivalTime = arrivalTime

        #decremented value of service time
        self.remainingServiceTime = serviceTime

        #process may start at 0 so
        self.startTime = -1

        #start time - arrival time - how long process waited in queue
        self.initialWaitTime = 0

        #when process ended
        self.endTime = 0

        ##endtime - servicetime - arivaltime - how long did the process idle total
        self.totalWaitTime = 0

        #end time - arrival time, how long did the whole thing take?
        self.turnAroundTime = 0

        #sent to queue yet?
        self.queued = False

    #setters and calculations
    def setStartTime(self, time):
        self.startTime = time
    def setEndTime(self, time):
        self.endTime = time

    def decrementRemainingServiceTime(self, time):
        self.remainingServiceTime -= time

    def calculateMetrics(self):
        #start time - arrival time -  how long process waited in queue
        self.initialWaitTime = self.startTime - self.arrivalTime

        #endtime - servicetime - arivaltime - how long did the process idle total
        self.totalWaitTime = self.endTime - self.startTime - self.serviceTime + self.initialWaitTime

        #end time - arrival time, how long did the whole thing take?
        self.turnAroundTime = self.endTime - self.arrivalTime