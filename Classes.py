from rich.console import Console
from rich.table import Table

class RoundRobin:
    def __init__(self, timeQuantum, data, contextSwitch):
        self.timeQuantum = timeQuantum
        self.processes = self.setProcesses(data)
        self.contextSwitch = contextSwitch
        self.timeElapsed = 0
        self.queue = self.setQueue(self.processes)

    #run round robin sequence
    def run(self):

        while len(self.queue) > 0:
            for i in range(0, len(self.queue)):

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
                    self.incrementByQuantum(self.timeQuantum - process.remainingServiceTime)
                    self.incrementByContext()


                #if more than or equal to full time quantum is remaining in process & process not completed, record time in RR
                if process.remainingServiceTime >= self.timeQuantum:
                    process.decrementRemainingServiceTime(self.timeQuantum)
                    self.incrementByQuantum(self.timeQuantum)
                    self.incrementByContext()
                
                #pop from queue
                if process.remainingServiceTime == 0:
                    process.setEndTime(self.timeElapsed)
                    self.removeFromQueue(process.id)

                    #increment time by context if not last process in queue
                    if len(self.queue) > 1:
                            self.incrementByContext()
                            break
                    break

        #finally, loop over processes to update their data
        for process in self.processes:
            process.calculateMetrics()
        #output results
        self.createTable()


    #set queue, RR.queue holds the processes as they run whereas RR.processes contains all processes throughout the RR lifecycle
    def setQueue(self, processes):
        queue = []
        for process in processes:
            queue.append(process)
        return queue

    def setProcesses(self, data):
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
    
    def incrementByQuantum(self, time):
        self.timeElapsed += time
    
    def incrementByContext(self):
        self.timeElapsed += self.contextSwitch

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

    def createTable(self):
        table = Table(title="CSC440 - Round Robin")
        table.add_column("Process Id", justify="right")
        table.add_column("Start Time", justify="right")
        table.add_column("Initial Wait Time", justify="right")
        table.add_column("End Time", justify="right")
        table.add_column("Total Wait Time", justify="right")
        table.add_column("Turn Around Time", justify="right")
        for process in self.processes:
            table.add_row(
                f"{process.id}",
                f"{process.startTime}",
                f"{process.initialWaitTime}", 
                f"{process.endTime}", 
                f"{process.totalWaitTime}",
                f"{process.turnAroundTime}"
            )

        console = Console()
        console.print(table)
    
class Process:
    def __init__(self, id, serviceTime, arrivalTime):
        self.id = id

        #length of process running time
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
        self.totalWaitTime = self.endTime - self.serviceTime - self.arrivalTime

        #end time - arrival time, how long did the whole thing take?
        self.turnAroundTime = self.endTime - self.arrivalTime