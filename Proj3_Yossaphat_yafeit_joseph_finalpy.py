# https://github.com/jsanch1614/ENPM661_Project3.1_Draft

import numpy as np
import pandas as pd
import math
import time
from collections import deque
from pynput import keyboard
from pynput.keyboard import Key
import pygame
import heapq
pygame.init() 


# Window requirement
height = 250 
width = 600

surface = pygame.display.set_mode((width, height))  # 250mm x 600mm
pygame.display.set_caption("A* Search Visualization")

# Character main color and border color
border_color = (255, 192, 203)
char_color = (255, 80, 200)

# visualization colors
visited_color = (0, 255, 0)
path_color = (255, 0, 255)
start_color = (0, 25, 255)
goal_color = (255, 0, 0)

# fill free space with black background
surface.fill((0, 0, 0))

# border of characters
# these are the mathematical models of the letter geometry for the obstacle space
# J
J_rect = pygame.draw.rect(surface, border_color, pygame.Rect(117*0.75, 39*0.75, 54*0.75, 122*0.75), width=30) # basic geometry of rectangle that forms "J"
border_colorJ_arc = pygame.draw.arc(surface, border_color, pygame.Rect(49*0.75, 89*0.75, 122*0.75, 122*0.75), start_angle=2.90, stop_angle=0, width=60) 
# S
S_arc = pygame.draw.arc(surface, border_color, pygame.Rect(169*0.75, 39*0.75, 112*0.75, 112*0.75), start_angle=0.1, stop_angle=4.81239, width=60)
S_arc_2 = pygame.draw.arc(surface, border_color, pygame.Rect(169*0.75, 94*0.75, 122*0.75, 122*0.75), start_angle=-3.24, stop_angle=1.97, width=60)
# 4 432
four_rect = pygame.draw.rect(surface, border_color, pygame.Rect(274*0.75, 39*0.75, 54*0.75, 97*0.75), width=30)
four_rect2 = pygame.draw.rect(surface, border_color, pygame.Rect(274*0.75, 89*0.75, 97*0.75, 54*0.75), width=30)
four_rect3 = pygame.draw.rect(surface, border_color, pygame.Rect(324*0.75, 39*0.75, 54*0.75, 172*0.75), width=30)
# 4
four_rect4 = pygame.draw.rect(surface, border_color, pygame.Rect(374*0.75, 39*0.75, 54*0.75, 97*0.75), width=30)
four_rect5 = pygame.draw.rect(surface, border_color, pygame.Rect(374*0.75, 89*0.75, 97*0.75, 54*0.75), width=30)
four_rect6 = pygame.draw.rect(surface, border_color, pygame.Rect(424*0.75, 39*0.75, 54*0.75, 172*0.75), width=30)
# 3
three_rect = pygame.draw.arc(surface, border_color, pygame.Rect(464*0.75, 39*0.75, 112*0.75, 112*0.75), start_angle=4.71239, stop_angle=2.85619, width=60)
three_rect2 = pygame.draw.rect(surface, border_color, pygame.Rect(494*0.75, 97*0.75, 62*0.75, 54*0.75), width=30)
three_rect3 = pygame.draw.arc(surface, border_color, pygame.Rect(464*0.75, 99*0.75, 112*0.75, 112*0.75), start_angle=3.42699, stop_angle=1.5708, width=60)
# 2
two_rect = pygame.draw.rect(surface, border_color, pygame.Rect(589*0.75, 39*0.75, 102*0.75, 54*0.75), width=30)
two_rect2 = pygame.draw.rect(surface, border_color, pygame.Rect(649*0.75, 39*0.75, 54*0.75, 114*0.75), width=30)
two_rect3 = pygame.draw.rect(surface, border_color, pygame.Rect(624*0.75, 99*0.75, 54*0.75, 54*0.75), width=30)
two_rect4 = pygame.draw.rect(surface, border_color, pygame.Rect(599*0.75, 129*0.75, 54*0.75, 54*0.75), width=30)
two_rect5 = pygame.draw.rect(surface, border_color, pygame.Rect(579*0.75, 159*0.75, 142*0.75, 54*0.75), width=30)

# characters
# J
J_rect = pygame.draw.rect(surface, char_color, pygame.Rect(128*0.75, 50*0.75, 32*0.75, 100*0.75), width=30)
J_arc = pygame.draw.arc(surface, char_color, pygame.Rect(60*0.75, 100*0.75, 100*0.75, 100*0.75), start_angle=3.1415, stop_angle=0, width=30)
# S
S_arc = pygame.draw.arc(surface, char_color, pygame.Rect(180*0.75, 50*0.75, 90*0.75, 90*0.75), start_angle=0.5, stop_angle=4.71239, width=30)
S_arc_2 = pygame.draw.arc(surface, char_color, pygame.Rect(180*0.75, 110*0.75, 90*0.75, 90*0.75), start_angle=-2.64, stop_angle=1.57, width=30)
# 4 432
four_rect = pygame.draw.rect(surface, char_color, pygame.Rect(285*0.75, 50*0.75, 32*0.75, 75*0.75), width=30)
four_rect2 = pygame.draw.rect(surface, char_color, pygame.Rect(285*0.75, 100*0.75, 75*0.75, 32*0.75), width=30)
four_rect3 = pygame.draw.rect(surface, char_color, pygame.Rect(335*0.75, 50*0.75, 32*0.75, 150*0.75), width=30)
# 4
four_rect4 = pygame.draw.rect(surface, char_color, pygame.Rect(385*0.75, 50*0.75, 32*0.75, 75*0.75), width=30)
four_rect5 = pygame.draw.rect(surface, char_color, pygame.Rect(385*0.75, 100*0.75, 75*0.75, 32*0.75), width=30)
four_rect6 = pygame.draw.rect(surface, char_color, pygame.Rect(435*0.75, 50*0.75, 32*0.75, 150*0.75), width=30)
# 3
three_rect = pygame.draw.arc(surface, char_color, pygame.Rect(475*0.75, 50*0.75, 90*0.75, 90*0.75), start_angle=4.71239, stop_angle=2.35619, width=30)
three_rect2 = pygame.draw.rect(surface, char_color, pygame.Rect(505*0.75, 108*0.75, 40*0.75, 32*0.75), width=30)
three_rect3 = pygame.draw.arc(surface, char_color, pygame.Rect(475*0.75, 110*0.75, 90*0.75, 90*0.75), start_angle=3.92699, stop_angle=1.5708, width=30)
# 2
two_rect = pygame.draw.rect(surface, char_color, pygame.Rect(600*0.75, 50*0.75, 80*0.75, 32*0.75), width=30)
two_rect2 = pygame.draw.rect(surface, char_color, pygame.Rect(660*0.75, 50*0.75, 32*0.75, 92*0.75), width=30)
two_rect3 = pygame.draw.rect(surface, char_color, pygame.Rect(635*0.75, 110*0.75, 32*0.75, 32*0.75), width=30)
two_rect4 = pygame.draw.rect(surface, char_color, pygame.Rect(610*0.75, 140*0.75, 32*0.75, 32*0.75), width=30)
two_rect5 = pygame.draw.rect(surface, char_color, pygame.Rect(590*0.75, 170*0.75, 120*0.75, 32*0.75), width=30)

# show the map after drawing obstaclesd
pygame.display.flip()
 

# ─────────────────────────────────────────────────────────────────────────────
# KEY HELPER: pump events so the window stays responsive while waiting for user input in the terminal
def pump():
    """Call this regularly to keep the pygame window alive."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit


# Size and clearance for the robot were provided
robot_radius = 5
clearance = 5
total_clearance = robot_radius + clearance
# ─────────────────────────────────────────────────────────────────────────────
# OBSTACLE CHECK 

def is_free_space(x, y):
    x = int(round(x))
    y = int(round(y))

    # Boundary inflation
    if x < total_clearance or x >= width - total_clearance:
        return False
    if y < total_clearance or y >= height - total_clearance:
        return False

    for dx in range(-total_clearance, total_clearance + 1):
        for dy in range(-total_clearance, total_clearance + 1):
            if dx*dx + dy*dy <= total_clearance*total_clearance:
                nx = x + dx
                ny = y + dy

                color = surface.get_at((nx, ny))[:3]
                if color == border_color or color == char_color:
                    return False

    return True

# ─────────────────────────────────────────────────────────────────────────────
# USER INPUT
def get_valid_coord(label):
    while True:
        pump()   # keep window alive while waiting for input
        try:
            x     = int(input(f"[{label}] Enter x: "))
            y     = int(input(f"[{label}] Enter y: "))
            py = y 
            theta = int(input(f"[{label}] Enter theta (multiple of 30°): "))
        except ValueError:
            print(" Enter integers only.")
            continue
        if not (0 < x < width):
            print(f" x must be 1-{width-1}")
            continue
        if not (0 < py < height):
            print(f" y must be 1-{height-1}")
            continue
        if theta % 30 != 0:
            print(" Theta must be a multiple of 30.")
            continue
        print("Checking point:", x, py, "theta:", theta)
        if not is_free_space(x, py):
            print(" Point is inside an obstacle.")
            continue
        
        # convert user (Cartesian) → pygame
        return (x, py, theta % 360)


# ─────────────────────────────────────────────────────────────────────────────
# Get user inputs - start, goal, robot radius, clearance, step size
print("Enter START state:")
start_state = get_valid_coord("START")

print("\nEnter GOAL state:")
goal_state  = get_valid_coord("GOAL")


step_size = 0
while not (1 <= step_size <= 10):
    pump()
    try:   
        step_size = int(input("\nStep size (1-10): "))
    except ValueError: 
        pass
    if not (1 <= step_size <= 10):
        print(" Must be 1-10.")

print(f"\n Start={start_state}  Goal={goal_state}  L={step_size}\n")
# L = step_size

# ─────────────────────────────────────────────────────────────────────────────
# Movement functions
available_turns = [-60, -30, 0, 30, 60]

def apply_action(state, turn_deg, step_size):
    x, y, theta = state
    new_theta = (theta + turn_deg) % 360 # keep orientation 0-359
    rad = math.radians(new_theta) # convert to radians for trig functions
    new_x = x + step_size * math.cos(rad)
    new_y = y - step_size * math.sin(rad)#   y-axis flipped in pygame

    # Collision checking each small steps along the path
    steps = max(1, int(step_size * 2))
    for t in range(steps + 1): # check points along the path at intervals of 0.5 units
        frac = t / steps # fraction of the way along the path
        ix = x + frac * (new_x - x) 
        iy = y + frac * (new_y - y)
        if not is_free_space(int(round(ix)), int(round(iy))): # mid-path obstacle
            return None # invalid move if path hits obstacle

    snapped_theta = int(round(new_theta / 30)) * 30 % 360 # snap to nearest multiple of 30 degrees
    return (int(round(new_x)), int(round(new_y)), snapped_theta)

# Applies the actions from the action angles list to get actions
def action_minus_60(state, step_size):
    return apply_action(state, -60, step_size)

def action_minus_30(state, step_size):
    return apply_action(state, -30, step_size)

def action_0(state, step_size):
    return apply_action(state, 0, step_size)

def action_plus_30(state, step_size):
    return apply_action(state, 30, step_size)

def action_plus_60(state, step_size):
    return apply_action(state, 60, step_size)

# Action list
actions = [action_minus_60, action_minus_30, action_0, action_plus_30, action_plus_60 ]

# Gets neighbors from the action list
def get_neighbors(state, step_size):
    results = []
    for action in actions:
        ns = action(state, step_size)
        if ns is not None:
            results.append((ns, float(step_size)))
    return results


# this function uses the projection equation to get the vector of the projection from the start state to the current state
# this is then subtracted to get the distance to the start state
# this is done so that the algorithm will detect the robot passing through the start state threshold to account for 
# slight overshooting with the max of 10 step length
def is_goal_reached(state, goal_state, pos_threshold=3, theta_threshold=60): # goal state is the start state in the case of backwards A*
    dx = state[0] - goal_state[0]
    dy = state[1] - goal_state[1]

    dot_state_goal = np.sum((goal_state[0] * state[0]) + (goal_state[1] * state[1])) # np.dot(goal_state, state)

    proj = dot_state_goal / ((np.sqrt((state[0])**2 + (state[1])**2))**2)

    vect_proj_x = state[0] * proj
    vect_proj_y = state[1] * proj

    dist_from_proj_x = goal_state[0] - vect_proj_x
    dist_from_proj_y = goal_state[1] - vect_proj_y

    mag_dist_proj = (np.sqrt((dist_from_proj_x)**2 + (dist_from_proj_y)**2)) # calculating distance from "goal" to state vector to determine if we passed it

    # dist = math.sqrt(dx*dx + dy*dy)

    dtheta = abs(state[2] - goal_state[2]) % 360
    dtheta = min(dtheta, 360 - dtheta)
    
    return mag_dist_proj <= (pos_threshold+1 + (robot_radius)) and dtheta <= theta_threshold

def angle_diff(a, b):
    diff = abs(a - b) % 360
    return min(diff, 360 - diff)

def is_duplicate_node(n1, n2):   # checks if duplicated node : 1. distance < 0.5 units, 2. angle difference < 30 degrees
    thetha_threshold = 30
    euclidean_threshold = 0.5
    
     # distance check btw positions
    dx = n1[0] - n2[0]
    dy = n1[1] - n2[1]
    euclidean_threshold = math.sqrt(dx*dx + dy*dy)
    # angle check btw orientations
    diff = abs(n1[2]- n2[2]) % 360
    thetha_threshold = min(diff, 360 - diff) # angle wrap around check ex:0,350 = 10 degree difference, not 350
    return euclidean_threshold < 0.5 and thetha_threshold < 30

def state_to_key(state):
    x, y, theta = state
    x_key = round(x * 2) / 2.0
    y_key = round(y * 2) / 2.0
    theta_key = (round(theta / 30) * 30) % 360
    return (x_key, y_key, theta_key)
#----------------------------------------------------------------

explored_edges = []
closedList = []
parents = {}
children = {}
child_to_parent = {}
child_to_parent_index = {}

start_state_x = start_state[0]
start_state_y = start_state[1]

goal_state_x = goal_state[0]
goal_state_y = goal_state[1]

node_to_f_score = {goal_state: np.sqrt((start_state_x - goal_state_x)**2 + (start_state_y - goal_state_y)**2)}
node_to_g_score = {goal_state: 0}


# in this function the updated states are compared to the closed list for confirmed movement
# if the attempted move is the same as the current position of in the closed list then the position is not updated
def getPossibleMoves(new_node_x, row, col, counter, step_size):
    neighbors = get_neighbors(new_node_x, step_size)
    
    if not neighbors:
        return
    # store current node
    parents[counter] = new_node_x    

    # current node g score
    if new_node_x not in node_to_g_score:
        node_to_g_score[new_node_x] = 0
    g_x = node_to_g_score[new_node_x]

    # loop through however many valid neighbors exist
    for neighbor, move_cost in neighbors:
        if neighbor in closedList:
            continue

        neighbor_key = state_to_key(neighbor)
        if neighbor_key in visited_states:
            continue

        # tentative path cost of neighbor through current node
        tentative_g = g_x + move_cost

        # if neighbor is new or found with lower cost, update it
        if neighbor not in openList or tentative_g < node_to_g_score[neighbor]:
            node_to_g_score[neighbor] = tentative_g

            h = np.sqrt((start_state_x - neighbor[0])**2 + (start_state_y - neighbor[1])**2)
            scaled_tent_g = (tentative_g + h)*10 # to include another decimal in tie breaking

            # Rounding to introduce tie breaking that favors the most recent entry
            node_to_f_score[neighbor] = int(scaled_tent_g)

            # print("neighbor: ", neighbor[0], neighbor[1])
            # print("Heuristic (the distance from start to neighbor): ", h)
            # print("Tentative g score for neighbor: ", tentative_g)
            
            child_to_parent[neighbor] = new_node_x
            child_to_parent_index[neighbor] = counter
            
            visited_states.append(neighbor_key)

            # In the event of a tie, the heap will look to the counter for the smallest value which will be the most recent entry of the two
            heapq.heappush(open_heap, ((node_to_f_score[neighbor]), -counter, tentative_g, neighbor)) # saving to heap

            explored_edges.append(( # recording states explored
                (new_node_x[0], new_node_x[1]),
                (neighbor[0], neighbor[1])
            ))

            if neighbor not in openList:
                openList.append(neighbor)
    return

# 3D visited matrix: (y, x, theta)
# this is a matrix of the 2d map space plus the rotation making a 3d space
# when an explored state is given to the visited matrix, the state becomes true when querying later
# this makes the check for explored states much faster
visited_matrix = np.zeros((int(width), int(height), 360), dtype=bool)

initial_dist = round( np.sqrt((start_state_x - goal_state_x)**2 + (start_state_y - goal_state_y)**2))

open_heap = []
heapq.heappush(open_heap, (initial_dist, 0.0, 0.0, goal_state))


openList = deque([goal_state]) # open list begins with start state to initialize the loop
closedList = set()
visited_states = [] # set()
# visited_states.add(state_to_key(goal_state))
visited_states.append(goal_state)

counter = 0
end = 0

start_time = time.time()

# this is the main loop
# the first current state is popped from the heap
# it is then compared to the start node and either stops for end of program or passes current state to movement functions
while node_to_f_score:
    pump()

    if counter % 20000 == 0:
        print("Iterations: ", counter)
        print("node to f score before check goal: ", node_to_f_score)

    # pops lowest. Heaps became prefferable over ques for speed and ease of use (automatically pops min value)
    f_cost, n_counter, g_cost, current_node = heapq.heappop(open_heap)
    # print("\n Current node: ", current_node)
    

    row, col, angle_idx = current_node

    # Skip if already visited
    if visited_matrix[row, col, angle_idx]:
        continue

    # Mark as visited (closed set)
    visited_matrix[row, col, angle_idx] = True

    del node_to_f_score[current_node]    

    if is_goal_reached(current_node, start_state) == True:
        goal_reached_state = current_node
        end = 1
        print(f"Goal reached: {current_node}")
        break

    # Explore neighbors
    neighbors = get_neighbors(current_node, step_size)

    # visited_states.add(state_to_key(current_node))
    visited_states.append(current_node)


     
    a, b = current_node[0], current_node[1]
    # print("check_goal before get possible moves: ", current_node)
    getPossibleMoves(current_node, a, b, counter, step_size)
    
    #################################################
    # # visualize visited node on pygame
    x, y, _ = current_node
    pygame.draw.circle(surface, visited_color, (x, y), 1)

    # update window every few nodes so it does not slow too much
    if counter % 30 == 0:
        pygame.display.update()
        pump()
    #################################################
    
    if counter % 20000 == 0:
        print("Iterations: ", counter)
        print("Length of openList: ", len(openList))
        print("CLosed List: \n", len(closedList))

    counter += 1

# If the start_state is found this receives the output of 1 to end the loop and print final outputs
if end == 1:
    print("SUCCESS \n SUCCESS \n SUCCESS \n SUCCESS")
else:
    print("Search ended without reaching the goal.")


# print("end: ", end)
# print("child to parent: ", child_to_parent)

# the shortest path is discovered using the child to parent dict from before
# the dict is reversed to account for the start of the search beginning at the end of the dict
if end == 1:
    shortest_path = [current_node]
    current = current_node

    while current != goal_state:
        current = child_to_parent[current]
        shortest_path.append(current)
        
print("--- %s seconds ---" % (time.time() - start_time)) # time for full search and shortest path is recorded for analysis


############################################
# Animation
ppmm = 142 / 25.4 # 142 ppi of current display

height = 250 # int(ppmm*50)
width = 600 # int(ppmm*180)


surface = pygame.display.set_mode((width, height))  
border_color = (255, 192, 203)
char_color = (255, 80, 100)


# characters visualization
# in this case, the pink border of the letters acted as the total shape of the letters, leaving a 5mm gap between robot and the pink edges

# J
J_rect = pygame.draw.rect(surface, char_color, pygame.Rect(128*0.75, 50*0.75, 32*0.75, 100*0.75), width=30)
J_arc = pygame.draw.arc(surface, char_color, pygame.Rect(60*0.75, 100*0.75, 100*0.75, 100*0.75), start_angle=3.1415, stop_angle=0, width=30)
# S
S_arc = pygame.draw.arc(surface, char_color, pygame.Rect(180*0.75, 50*0.75, 90*0.75, 90*0.75), start_angle=0.5, stop_angle=4.71239, width=30)
S_arc_2 = pygame.draw.arc(surface, char_color, pygame.Rect(180*0.75, 110*0.75, 90*0.75, 90*0.75), start_angle=-2.64, stop_angle=1.57, width=30)
# 4 432
four_rect = pygame.draw.rect(surface, char_color, pygame.Rect(285*0.75, 50*0.75, 32*0.75, 75*0.75), width=30)
four_rect2 = pygame.draw.rect(surface, char_color, pygame.Rect(285*0.75, 100*0.75, 75*0.75, 32*0.75), width=30)
four_rect3 = pygame.draw.rect(surface, char_color, pygame.Rect(335*0.75, 50*0.75, 32*0.75, 150*0.75), width=30)
# 4
four_rect4 = pygame.draw.rect(surface, char_color, pygame.Rect(385*0.75, 50*0.75, 32*0.75, 75*0.75), width=30)
four_rect5 = pygame.draw.rect(surface, char_color, pygame.Rect(385*0.75, 100*0.75, 75*0.75, 32*0.75), width=30)
four_rect6 = pygame.draw.rect(surface, char_color, pygame.Rect(435*0.75, 50*0.75, 32*0.75, 150*0.75), width=30)
# 3
three_rect = pygame.draw.arc(surface, char_color, pygame.Rect(475*0.75, 50*0.75, 90*0.75, 90*0.75), start_angle=4.71239, stop_angle=2.35619, width=30)
three_rect2 = pygame.draw.rect(surface, char_color, pygame.Rect(505*0.75, 108*0.75, 40*0.75, 32*0.75), width=30)
three_rect3 = pygame.draw.arc(surface, char_color, pygame.Rect(475*0.75, 110*0.75, 90*0.75, 90*0.75), start_angle=3.92699, stop_angle=1.5708, width=30)
# 2
two_rect = pygame.draw.rect(surface, char_color, pygame.Rect(600*0.75, 50*0.75, 80*0.75, 32*0.75), width=30)
two_rect2 = pygame.draw.rect(surface, char_color, pygame.Rect(660*0.75, 50*0.75, 32*0.75, 92*0.75), width=30)
two_rect3 = pygame.draw.rect(surface, char_color, pygame.Rect(635*0.75, 110*0.75, 32*0.75, 32*0.75), width=30)
two_rect4 = pygame.draw.rect(surface, char_color, pygame.Rect(610*0.75, 140*0.75, 32*0.75, 32*0.75), width=30)
two_rect5 = pygame.draw.rect(surface, char_color, pygame.Rect(590*0.75, 170*0.75, 120*0.75, 32*0.75), width=30)


for i, (p1, p2) in enumerate(explored_edges):
    # pump() 
    pygame.draw.line(surface, visited_color, p1, p2, 1)

    if i % 30 == 0:   # update every 30 steps
        pygame.time.delay(30)

        pygame.display.update()


# conversion for shortest path animation
def tuple_to_list(state):
    return list(state) 


# This loop converts the tuples from the shortest_path list to lists for easier handling in the animation loop
shortest_path_list = []
for i, p1 in enumerate(shortest_path):
    
    # print(p1[0])
    p1_list = tuple_to_list(p1)
    shortest_path_list.append(p1_list)

# Converts the state_state to a list for easier handling
start_state_list = tuple_to_list(start_state)

# this will play an animation of the shortest path
# a better animation has been recorded in the mp4

# shortest path animation loop
for i, p1 in enumerate(shortest_path):
    
    print(p1[1])

    shortest_path_color = (255, 0, 255)

    # Assigns the x and y values for line coordinates
    last_node_x = shortest_path_list[i-1][0]
    last_node_y = shortest_path_list[i-1][1]

    # If the loop is at the beginning, it will use the start_state_list x and y for the first point of the line
    if i == 0:
        last_node_x = start_state_list[0]
        last_node_y = start_state_list[1]
    
    # This line will use the last state and the current state in the list to create a line, showing the shortest path
    pygame.draw.line(surface, shortest_path_color, (last_node_x, last_node_y), (shortest_path_list[i][0], shortest_path_list[i][1]), width=4)
    
    # Adds the start and goal state as dots
    pygame.draw.circle(surface, start_color, (start_state[0], start_state[1]), 5)
    pygame.draw.circle(surface, goal_color, (goal_state[0], goal_state[1]), 5)
    pygame.time.delay(30)

    pygame.display.flip() 

    
# pygame.display.flip() 
pygame.time.wait(10000)  # Pause for 10 seconds
pygame.quit()

