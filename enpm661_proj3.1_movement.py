import numpy as np
import pandas as pd
import time
from collections import deque
from pynput import keyboard
from pynput.keyboard import Key
import pygame
import math
pygame.init() 

ppmm = 142 / 25.4 # 142 ppi of current display

height = int(ppmm*50) # 50mm box requirement
width = int(ppmm*180)


surface = pygame.display.set_mode((width, height))  # 50mm x 180mm
obstacle_color = (255, 192, 203)
char_color = (255, 80, 200)

# border
# these are the mathematical models of the letter geometry for the obstacle space
# J
J_rect = pygame.draw.rect(surface, obstacle_color, pygame.Rect(117, 39, 54, 122), width=30) # basic geometry of rectangle that forms "J"
J_arc = pygame.draw.arc(surface, obstacle_color, pygame.Rect(49, 89, 122, 122), start_angle=2.90, stop_angle=0, width=60) 
# S
S_arc = pygame.draw.arc(surface, obstacle_color, pygame.Rect(169, 39, 112, 112), start_angle=0.1, stop_angle=4.81239, width=60)
S_arc_2 = pygame.draw.arc(surface, obstacle_color, pygame.Rect(169, 94, 122, 122), start_angle=-3.24, stop_angle=1.97, width=60)
# 4 432
four_rect = pygame.draw.rect(surface, obstacle_color, pygame.Rect(274, 39, 54, 97), width=30)
four_rect2 = pygame.draw.rect(surface, obstacle_color, pygame.Rect(274, 89, 97, 54), width=30)
four_rect3 = pygame.draw.rect(surface, obstacle_color, pygame.Rect(324, 39, 54, 172), width=30)
# 4
four_rect4 = pygame.draw.rect(surface, obstacle_color, pygame.Rect(374, 39, 54, 97), width=30)
four_rect5 = pygame.draw.rect(surface, obstacle_color, pygame.Rect(374, 89, 97, 54), width=30)
four_rect6 = pygame.draw.rect(surface, obstacle_color, pygame.Rect(424, 39, 54, 172), width=30)
# 3
three_rect = pygame.draw.arc(surface, obstacle_color, pygame.Rect(464, 39, 112, 112), start_angle=4.71239, stop_angle=2.85619, width=60)
three_rect2 = pygame.draw.rect(surface, obstacle_color, pygame.Rect(494, 97, 62, 54), width=30)
three_rect3 = pygame.draw.arc(surface, obstacle_color, pygame.Rect(464, 99, 112, 112), start_angle=3.42699, stop_angle=1.5708, width=60)
# 2
two_rect = pygame.draw.rect(surface, obstacle_color, pygame.Rect(589, 39, 102, 54), width=30)
two_rect2 = pygame.draw.rect(surface, obstacle_color, pygame.Rect(649, 39, 54, 114), width=30)
two_rect3 = pygame.draw.rect(surface, obstacle_color, pygame.Rect(624, 99, 54, 54), width=30)
two_rect4 = pygame.draw.rect(surface, obstacle_color, pygame.Rect(599, 129, 54, 54), width=30)
two_rect5 = pygame.draw.rect(surface, obstacle_color, pygame.Rect(579, 159, 142, 54), width=30)


# characters
# J
J_rect = pygame.draw.rect(surface, char_color, pygame.Rect(128, 50, 32, 100), width=30)
J_arc = pygame.draw.arc(surface, char_color, pygame.Rect(60, 100, 100, 100), start_angle=3.1415, stop_angle=0, width=30)
# S
S_arc = pygame.draw.arc(surface, char_color, pygame.Rect(180, 50, 90, 90), start_angle=0.5, stop_angle=4.71239, width=30)
S_arc_2 = pygame.draw.arc(surface, char_color, pygame.Rect(180, 110, 90, 90), start_angle=-2.64, stop_angle=1.57, width=30)
# 4 432
four_rect = pygame.draw.rect(surface, char_color, pygame.Rect(285, 50, 32, 75), width=30)
four_rect2 = pygame.draw.rect(surface, char_color, pygame.Rect(285, 100, 75, 32), width=30)
four_rect3 = pygame.draw.rect(surface, char_color, pygame.Rect(335, 50, 32, 150), width=30)
# 4
four_rect4 = pygame.draw.rect(surface, char_color, pygame.Rect(385, 50, 32, 75), width=30)
four_rect5 = pygame.draw.rect(surface, char_color, pygame.Rect(385, 100, 75, 32), width=30)
four_rect6 = pygame.draw.rect(surface, char_color, pygame.Rect(435, 50, 32, 150), width=30)
# 3
three_rect = pygame.draw.arc(surface, char_color, pygame.Rect(475, 50, 90, 90), start_angle=4.71239, stop_angle=2.35619, width=30)
three_rect2 = pygame.draw.rect(surface, char_color, pygame.Rect(505, 108, 40, 32), width=30)
three_rect3 = pygame.draw.arc(surface, char_color, pygame.Rect(475, 110, 90, 90), start_angle=3.92699, stop_angle=1.5708, width=30)
# 2
two_rect = pygame.draw.rect(surface, char_color, pygame.Rect(600, 50, 80, 32), width=30)
two_rect2 = pygame.draw.rect(surface, char_color, pygame.Rect(660, 50, 32, 92), width=30)
two_rect3 = pygame.draw.rect(surface, char_color, pygame.Rect(635, 110, 32, 32), width=30)
two_rect4 = pygame.draw.rect(surface, char_color, pygame.Rect(610, 140, 32, 32), width=30)
two_rect5 = pygame.draw.rect(surface, char_color, pygame.Rect(590, 170, 120, 32), width=30)

# ─────────────────────────────────────────────────────────────────────────────
# KEY HELPER: pump events so the window stays responsive while waiting for user input in the terminal
def pump():
    """Call this regularly to keep the pygame window alive."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

# ─────────────────────────────────────────────────────────────────────────────
# OBSTACLE CHECK 
def is_free_space(x, y):
    if not (0 < x < width and 0 < y < height): # check if point is within bounds of the surface
        return False
    return surface.get_at((int(x), int(y)))[:3] == (0, 0, 0) # check if point isn't an obstacle

# ─────────────────────────────────────────────────────────────────────────────
# USER INPUT
def get_valid_coord(label):
    while True:
        pump()   # keep window alive while waiting for input
        try:
            x     = int(input(f"[{label}] Enter x: "))
            y     = int(input(f"[{label}] Enter y: "))
            py = height - y # convert Cartesian y → pygame y (inverted)
            theta = int(input(f"[{label}] Enter theta (multiple of 30°): "))
        except ValueError:
            print(" Enter integers only.")
            continue
        if not (0 < x < width):
            print(f" x must be 1–{width-1}")
            continue
        if not (0 < py < height):
            print(f" y must be 1–{height-1}")
            continue
        if theta % 30 != 0:
            print(" Theta must be a multiple of 30.")
            continue
        
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
robot_radius = int(input("Enter robot radius: "))
clearance = int(input("Enter clearance: "))

step_size = 0
while not (1 <= step_size <= 10):
    pump()
    try:   
        step_size = int(input("\nStep size L (1–10): "))
    except ValueError: 
        pass
    if not (1 <= step_size <= 10):
        print("  ✗ Must be 1–10.")

print(f"\n✓ Start={start_state}  Goal={goal_state}  L={step_size}\n")

# ─────────────────────────────────────────────────────────────────────────────
# Movement functions
available_turns = [-60, -30, 0, 30, 60]

def apply_action(state, turn_deg, L):
    x, y, theta = state
    new_theta = (theta + turn_deg) % 360 # keep oreintation 0-359
    rad = math.radians(new_theta) # convert to radians for trig functions
    new_x = x + L * math.cos(rad)
    new_y = y - L * math.sin(rad)#   y-axis flipped in pygame

    # Collision checking each small steps along the path
    steps = max(1, int(L * 2))
    for t in range(steps + 1): # check points along the path at intervals of 0.5 units
        frac = t / steps # fraction of the way along the path
        ix = x + frac * (new_x - x) 
        iy = y + frac * (new_y - y)
        if not is_free_space(int(round(ix)), int(round(iy))): # mid-path obstacle
            return None

    snapped_theta = int(round(new_theta / 30)) * 30 % 360 # snap to nearest multiple of 30 degrees
    return (int(round(new_x)), int(round(new_y)), snapped_theta)

def action_minus_60(state, L):
    return apply_action(state, -60, L)

def action_minus_30(state, L):
    return apply_action(state, -30, L)

def action_0(state, L):
    return apply_action(state, 0, L)

def action_plus_30(state, L):
    return apply_action(state, 30, L)

def action_plus_60(state, L):
    return apply_action(state, 60, L)

actions = [action_minus_60, action_minus_30, action_0, action_plus_30, action_plus_60 ]

def get_neighbors(state, L):
    results = []
    for action in actions:
        ns = action(state, L)
        if ns is not None:
            results.append((ns, float(L)))
    return results

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
    