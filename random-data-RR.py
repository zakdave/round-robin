from Classes import RoundRobin
import random

def generateData(serviceRange, arrivalRange):
    servTimes = []
    interArr = []
    

    #generate 99 interarrival times, 100 service times with one loop
    for i in range(100):
        servTimes.append(random.randint(serviceRange[0],serviceRange[1]))
        if i == 99 : continue 
        interArr.append(random.randint(arrivalRange[0],arrivalRange[1]))
    
    #create arrival time
    arrivals = [0] #intialize with 0
    for time in interArr:
        arrivals.append(arrivals[-1] + time) #append to back of the loop

    return dict(serviceTimes = servTimes, arrivalTimes = arrivals)

#service range 4-8, arrivalRange 5-10
times = generateData([4,8], [5,10])

#format data to pass to RR
data = []
for index, arrivalTime in enumerate(times["arrivalTimes"]):
    process = {}
    process["id"] = index+1
    process["arrivalTime"] = arrivalTime
    process["serviceTime"] = times["serviceTimes"][index]
    data.append(process)

#given quantum 2, cs 0
roundRobin = RoundRobin(2, data, 2)
roundRobin.runRR()

#run new sqrr
sqrr = RoundRobin(-1, data, 2)
sqrr.runSQRR()