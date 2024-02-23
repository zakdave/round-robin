from Classes import RoundRobin

data = [
    {"id": 1,"servetime": 75,"arrivaltime":0},
    {"id": 2,"servetime": 40,"arrivaltime":10},
    {"id": 3,"servetime": 25,"arrivaltime":10},
    {"id": 4,"servetime": 20,"arrivaltime":80}, 
    {"id": 5,"servetime": 45,"arrivaltime":85}
]

#instantiate w/ time quantum 0, processes and 0 context switch
roundRobin = RoundRobin(10, data, 0)
roundRobin.run()
roundRobin = RoundRobin(10, data, 2)
roundRobin.run()

