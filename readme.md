# ENPM661 - Planning - Project3Phase1 (Backward A*)
https://github.com/jsanch1614/ENPM661_Project3.1_Draft
## Team Members
Yossaphat Kulvatunyou   UID: 122362550     
yafeit Mihreteab    UID: 118357430
Joseph Sanchez  UID: 122354432



## Overview

This project implements a grid-based **A* search algorithm** with orientation for robot path planning.
The algorithm computes an optimal path from a start state to a goal state while avoiding obstacles with clearance.

The environment is visualized using **Pygame**, where:

* Obstacles are predefined
* Explored nodes are animated
* Final optimal path is displayed

---

## How to Run the Code

### 1. Install Dependencies

Make sure you have Python 3 installed, then install required libraries:

```
pip install numpy pygame
```

---

### 2. Run the Script

```
python backward_astar.py
```

---

### 3. Provide Inputs (IMPORTANT)

You will be prompted to enter:

#### Robot Parameters

* **Robot radius** (e.g., 5)
* **Clearance** (e.g., 5)

#### Start State

* x coordinate (0–599)
* y coordinate (0–249)
* theta (must be multiple of 30)

#### Goal State

* x coordinate (0–599)
* y coordinate (0–249)
* theta (must be multiple of 30)

#### Step Size

* Integer between **1 and 10**

---

### Coordinate Notes

* Coordinates are **Cartesian (origin at bottom-left)**
* Internally converted to **Pygame coordinates (origin at top-left)**

---

## Output

* The algorithm first computes the path
* Then visualization starts:

  * Cyan lines → explored nodes
  * Yellow line → optimal path
  * Green → start node
  * Red → goal node

---

## Dependencies / Libraries Used

* `numpy` – numerical computations and grid handling
* `math` – trigonometric calculations
* `time` – runtime measurement
* `heapq` – priority queue for A*
* `pygame` – visualization

---
## Notes

* The algorithm uses a **3D visited matrix** (x, y, theta)
* Motion primitives include 5 actions:

  * -60°, -30°, 0°, +30°, +60°
* Collision checking is performed along the motion path
* Obstacles are inflated using robot radius + clearance

---
