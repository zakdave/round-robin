# Round Robin 

## Description

A novel Hybrid Sliding Quantum Round Robin CPU scheduling algorithm that I created while exploring the traditional Round Robin scheduling algorithm with Python.  

## Table of Contents
- [Traditional Results](#results)
- [Installation](#installation)
- [Usage](#usage)

## Traditional Results


Results for TQ: 10, context switch 10  TQ: context switch: 2

![Traditional Results output](./results/results.png)

Note: This implementation checks the arrival time of each process before it starts and does not maintain a rotating queue. A copy of the processes is created by the setQueue method and each iteration of the inner loop checks if the process has arrived yet. Further revisions can be made to implement a rotating queue. This implementation works great at reducing intial wait time, but may sacrifice turn around time. 

By itself, this is not very useful. Future revisions could look at comparing a remaining time to quantum + context ratio that can complete near complete processes. Although, I believe this may make the overall scheduling more efficent in theory, it would create too much overhead in practice. 

![Context 0](./results/gantt-0-context.PNG) ![Context 10](./results/gantt-10-context.PNG)

Round Robin serves as a FCFS algorithm by executing the inner loop of the of the queue. Different methods of implementation can create surprisingly different results. The first images shows a 0 context time, and a time quantum of 10. In Figure, p3 should switch to p4, however the loop breaks off and the queue restarts from the beginning. This behavior could be avoided by maintaining a circular queue on the Round Robin class. 

## Installation

Ensure you have Python installed. Install rich with pip to generate the table. 'pip install rich'

## Usage

Run 'python round-robin.py'



