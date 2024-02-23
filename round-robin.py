from Classes import RoundRobin

data = [
    {"id": 1,"servetime": 75,"arrivaltime":0},
    {"id": 2,"servetime": 40,"arrivaltime":10},
    {"id": 3,"servetime": 25,"arrivaltime":10},
    {"id": 4,"servetime": 20,"arrivaltime":80}, 
    {"id": 5,"servetime": 45,"arrivaltime":85}
]



roundRobin = RoundRobin(10, data, 2)
roundRobin.run()

