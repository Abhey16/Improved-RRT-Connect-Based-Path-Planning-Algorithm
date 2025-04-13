# Improved-RRT-Connect-for-Mobile-Robots

This repository contains the implementation of **IRRT-Connect**, an improved version of the RRT-Connect path planning algorithm, developed for **ENPM661 - Planning for Autonomous Robots (Project 5)** at the University of Maryland.

The IRRT-Connect algorithm enhances the efficiency of mobile robot path planning in complex environments by introducing additional tree expansion strategies and goal-directed biasing mechanisms.

---

## Authors:

    Name: Ishan Kharat (ishanmk@umd.edu)   UID: 120427145

    Name: Abhey Sharma (abheys16@umd.edu)  UID: 120110306

---

## Project Overview

Traditional path planning algorithms like RRT and RRT-Connect often suffer from slow convergence and suboptimal paths, especially in cluttered or complex environments. IRRT-Connect addresses these limitations through:

- **Third Node Generation**: A midpoint (or a valid nearby point via dichotomy search) between the start and goal, allowing for the expansion of **four** trees instead of two.
- **Target Biasing**: Increased guidance toward the goal during node expansion, improving convergence.
- **Enhanced Planning Efficiency**: Reduction in iterations, planning time, and path length compared to standard RRT, RRT*, and RRT-Connect.

## Results

| Algorithm     | Avg. Time | Avg. Iterations | Avg. Path Length |
|---------------|-----------|-----------------|------------------|
| RRT           | 503       | 490             | 485              |
| RRT*          | 13.1      | 13.9            | 13.1             |
| RRT-Connect   | 754       | 747             | 745              |
| **IRRT-Connect** | **13.1**  | **13.9**          | **13.1**            |

- 🔄 **Iterations Reduced by 24%**
- ⏱️ **Planning Time Reduced by 42%**
- 📉 **Path Length Reduced by 11%**


![Figure_1](https://github.com/user-attachments/assets/caeb47f7-ea77-4711-bb1e-e00baff82a1b)

## How to Run the Code:

    git clone https://github.com/IshanMahesh/Improved-RRT-Connect-for-Mobile-Robots.git

### Part 1

#### Run the command below:

    cd Improved-RRT-Connect-for-Mobile-Robots
    python3 Improved_rrt_connect.py


## User Input
    1) Start node:(0,0) , Goal node:(50,0)
    2) Start node:(9,9) , Goal node:(54,9)
    3) Start node:(0,0) , Goal node:(24,-9)

## Range of obstacle Map
    x direction: (-5,55)

    y direction: (-10,10)

## Algorithms Provided:
1)Improved-RRT Connect


2)RRT Connect


3)RRT-Star


4)RRT


