from Classes import RoundRobin

data = [
    {"id": 1,"serviceTime": 75,"arrivalTime":0},
    {"id": 2,"serviceTime": 40,"arrivalTime":10},
    {"id": 3,"serviceTime": 25,"arrivalTime":10},
    {"id": 4,"serviceTime": 20,"arrivalTime":80}, 
    {"id": 5,"serviceTime": 45,"arrivalTime":85}
]

roundRobin = RoundRobin(10, data, 0)
roundRobin.runRR()

roundRobin = RoundRobin(10, data, 10)
roundRobin.runRR()



