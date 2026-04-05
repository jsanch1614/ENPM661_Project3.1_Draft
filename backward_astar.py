import numpy as np
import math
import time
import heapq
import pygame

pygame.init()

# ─────────────────────────────────────────────────────────────────────────────
# MAP SIZE  (600 x 250 as required by the project)
width  = 600
height = 250

surface = pygame.display.set_mode((width, height))
pygame.display.set_caption("A* Search Visualization")

obstacle_color = (255, 192, 203)
char_color     = (255, 80,  200)

# visualization colors
visited_color = (0,   200, 200)   # cyan for explored edges
path_color    = (255, 255,   0)   # yellow for optimal path
start_color   = (0,   255,   0)   # green
goal_color    = (255, 0,   0)   # orange

# fill free space with black background
surface.fill((0, 0, 0))

# ─────────────────────────────────────────────────────────────────────────────
# OBSTACLE CREATION  (kept exactly as original – professor approved)
# J
J_rect = pygame.draw.rect(surface, obstacle_color, pygame.Rect(117*0.75, 39*0.75, 54*0.75, 122*0.75), width=30) # basic geometry of rectangle that forms "J"
J_arc = pygame.draw.arc(surface, obstacle_color, pygame.Rect(49*0.75, 89*0.75, 122*0.75, 122*0.75), start_angle=2.90, stop_angle=0, width=60) 
# S
S_arc = pygame.draw.arc(surface, obstacle_color, pygame.Rect(169*0.75, 39*0.75, 112*0.75, 112*0.75), start_angle=0.1, stop_angle=4.81239, width=60)
S_arc_2 = pygame.draw.arc(surface, obstacle_color, pygame.Rect(169*0.75, 94*0.75, 122*0.75, 122*0.75), start_angle=-3.24, stop_angle=1.97, width=60)
# 4 432
four_rect = pygame.draw.rect(surface, obstacle_color, pygame.Rect(274*0.75, 39*0.75, 54*0.75, 97*0.75), width=30)
four_rect2 = pygame.draw.rect(surface, obstacle_color, pygame.Rect(274*0.75, 89*0.75, 97*0.75, 54*0.75), width=30)
four_rect3 = pygame.draw.rect(surface, obstacle_color, pygame.Rect(324*0.75, 39*0.75, 54*0.75, 172*0.75), width=30)
# 4
four_rect4 = pygame.draw.rect(surface, obstacle_color, pygame.Rect(374*0.75, 39*0.75, 54*0.75, 97*0.75), width=30)
four_rect5 = pygame.draw.rect(surface, obstacle_color, pygame.Rect(374*0.75, 89*0.75, 97*0.75, 54*0.75), width=30)
four_rect6 = pygame.draw.rect(surface, obstacle_color, pygame.Rect(424*0.75, 39*0.75, 54*0.75, 172*0.75), width=30)
# 3
three_rect = pygame.draw.arc(surface, obstacle_color, pygame.Rect(464*0.75, 39*0.75, 112*0.75, 112*0.75), start_angle=4.71239, stop_angle=2.85619, width=60)
three_rect2 = pygame.draw.rect(surface, obstacle_color, pygame.Rect(494*0.75, 97*0.75, 62*0.75, 54*0.75), width=30)
three_rect3 = pygame.draw.arc(surface, obstacle_color, pygame.Rect(464*0.75, 99*0.75, 112*0.75, 112*0.75), start_angle=3.42699, stop_angle=1.5708, width=60)
# 2
two_rect = pygame.draw.rect(surface, obstacle_color, pygame.Rect(589*0.75, 39*0.75, 102*0.75, 54*0.75), width=30)
two_rect2 = pygame.draw.rect(surface, obstacle_color, pygame.Rect(649*0.75, 39*0.75, 54*0.75, 114*0.75), width=30)
two_rect3 = pygame.draw.rect(surface, obstacle_color, pygame.Rect(624*0.75, 99*0.75, 54*0.75, 54*0.75), width=30)
two_rect4 = pygame.draw.rect(surface, obstacle_color, pygame.Rect(599*0.75, 129*0.75, 54*0.75, 54*0.75), width=30)
two_rect5 = pygame.draw.rect(surface, obstacle_color, pygame.Rect(579*0.75, 159*0.75, 142*0.75, 54*0.75), width=30)

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


# Show the map once after drawing obstacles
pygame.display.flip()
# ─────────────────────────────────────────────────────────────────────────────
# EVENT PUMP – keeps window alive while terminal waits for input
def pump():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit


obstacle_map = np.zeros((height, width), dtype=bool)

robot_radius = -1
while robot_radius < 0:
    pump()
    try:
        robot_radius = float(input("\nEnter robot radius (mm, e.g. 5): "))
        if robot_radius < 0:
            raise ValueError
    except ValueError:
        print("  Must be a non-negative number.")
        robot_radius = -1

clearance = -1
while clearance < 0:
    pump()
    try:
        clearance = float(input("Enter clearance (mm, e.g. 5): "))
        if clearance < 0:
            raise ValueError
    except ValueError:
        print("  Must be a non-negative number.")
        clearance = -1
        
# Combine robot radius and clearance → total safety margin
# This defines how much we "grow" obstacles outward
total_clearance = int(robot_radius + clearance)

print("Creating map with obstacle clearance ...")

# Loop through every pixel on the map
for x in range(width):
    for y in range(height):

        # Check if current pixel belongs to an obstacle
        if surface.get_at((x, y))[:3] not in [obstacle_color, char_color]:
            continue   # skip free space pixels

        # For each obstacle pixel, expand it outward by total_clearance in all directions
        for dx in range(-total_clearance, total_clearance + 1):
            for dy in range(-total_clearance, total_clearance + 1):

                # Compute new pixel location around obstacle
                nx, ny = x + dx, y + dy

                # Make sure new pixel is still inside map boundaries
                if 0 <= nx < width and 0 <= ny < height:

                    # Mark expanded region as obstacle
                    obstacle_map[ny, nx] = True
            

# ─────────────────────────────────────────────────────────────────────────────
# OBSTACLE CHECK  (reads pixel color from the pre-drawn surface)
def is_free_space(x, y):
    if not (0 <= x < width and 0 <= y < height):
        return False
    return not obstacle_map[int(y), int(x)]

# ─────────────────────────────────────────────────────────────────────────────
# USER INPUT – re-prompts on invalid entries
def get_valid_coord(label):
    """Prompt until a valid (x, y_pygame, theta) state is entered."""
    while True:
        pump()
        try:
            x     = int(input(f"[{label}] Enter x (Cartesian, 0-{width-1}): "))
            y_in  = int(input(f"[{label}] Enter y (Cartesian, 0-{height-1}): "))
            theta = int(input(f"[{label}] Enter theta (multiple of 30 deg): "))
        except ValueError:
            print("  Enter integers only.")
            continue

        if not (0 <= x < width):
            print(f"  x must be 0-{width-1}")
            continue
        if not (0 <= y_in < height):
            print(f"  y must be 0-{height-1}")
            continue
        if theta % 30 != 0:
            print("  Theta must be a multiple of 30.")
            continue

        # Convert Cartesian y -> pygame y (flip vertically)
        py = height - 1 - y_in
        theta = theta % 360

        if not is_free_space(x, py):
            print("  Point is inside an obstacle or clearance zone. Try again.")
            continue

        return (x, py, theta)


# ─────────────────────────────────────────────────────────────────────────────
# COLLECT ALL INPUTS
print("=" * 55)
print("  ENPM661 Spring 2026 - Project 3 Phase 1 - A*")
print("Coordinates are Cartesian (origin bottom-left).")
print()

print("Enter START state:")
start_state = get_valid_coord("START")

print("\nEnter GOAL state:")
goal_state = get_valid_coord("GOAL")

step_size = 0
while not (1 <= step_size <= 10):
    pump()
    try:
        step_size = int(input("Step size L (1-10): "))
    except ValueError:
        pass
    if not (1 <= step_size <= 10):
        print("  Must be an integer 1-10.")

total_clearance = int(robot_radius + clearance)
L = step_size

print("\nCoordinate register for pygame visualization")
print(f"Start={start_state}  Goal={goal_state}  L={L}")
print(f"Robot radius={robot_radius} mm  Clearance={clearance} mm\n")


# ─────────────────────────────────────────────────────────────────────────────
POSITION_RESOLUTION = 0.5   # how finely we divide x and y
ANGLE_RESOLUTION    = 30    # degrees per orientation bin

# Compute grid dimensions
GRID_ROWS   = int(height / POSITION_RESOLUTION)
GRID_COLS   = int(width  / POSITION_RESOLUTION)
GRID_ANGLES = int(360    / ANGLE_RESOLUTION)

# 3D visited matrix: (y, x, theta)
visited_matrix = np.zeros((GRID_ROWS, GRID_COLS, GRID_ANGLES), dtype=bool)


# Convert continuous state (x, y, theta) into discrete grid
def get_visited_index(x, y, theta):
    col = int(x / POSITION_RESOLUTION)
    row = int(y / POSITION_RESOLUTION)
    ang = int(theta / ANGLE_RESOLUTION) % GRID_ANGLES

    # clamp (prevents crash)
    row = min(max(row, 0), GRID_ROWS - 1)
    col = min(max(col, 0), GRID_COLS - 1)

    return row, col, ang

# ─────────────────────────────────────────────────────────────────────────────
# 5 ACTION FUNCTIONS  (one for each required movement direction)
def apply_action(current_state, turn_deg, L):
    """
    Turn by turn_deg then move forward by L.
    Checks all intermediate points for collisions.
    Returns new (x, y_pygame, theta) or None if blocked.
    """
    x, y, theta = current_state
    new_theta = (theta + turn_deg) % 360
    rad = math.radians(new_theta)
    new_x = x + L * math.cos(rad)
    new_y = y - L * math.sin(rad)   # pygame y-axis is flipped

     # Check path for collision (intermediate points)
    num_checks = max(1, int(step_size))

    for i in range(num_checks + 1):
        frac = i / num_checks
        ix = x + frac * (new_x - x)
        iy = y + frac * (new_y - y)
        if not is_free_space(int(round(ix)), int(round(iy))):
            return None

    snapped_theta = int(round(new_theta / 30)) * 30 % 360
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

actions = [action_minus_60, action_minus_30, action_0, action_plus_30, action_plus_60]


def get_neighbors(state, L):
    results = []
    for action in actions:
        ns = action(state, L)
        if ns is not None:
            results.append((ns, float(L)))
    return results


# ─────────────────────────────────────────────────────────────────────────────
# GOAL CHECK FUNCTION
goal_dist_threshold  = 1.5   # units (as recommended)
goal_thetha_threshold = 30    # degrees

# Return True if state is within threshold of goal
def is_goal_reached(state, goal):
    dx = state[0] - goal[0]
    dy = state[1] - goal[1]
    dist = math.sqrt(dx*dx + dy*dy)
    dtheta = abs(state[2] - goal[2]) % 360
    dtheta = min(dtheta, 360 - dtheta)
    return dist <= goal_dist_threshold and dtheta <= goal_thetha_threshold


# ─────────────────────────────────────────────────────────────────────────────
# HEURISTIC  (Euclidean distance)
def heuristic(state, goal):
    dx = state[0] - goal[0]
    dy = state[1] - goal[1]
    return math.sqrt(dx*dx + dy*dy)


# ─────────────────────────────────────────────────────────────────────────────
# BACKTRACK FUNCTION  – traces child->parent from goal back to start
# Return list of states from start to goal
def backtrack(goal_node, start_node, parent_map):
    path = []
    current = goal_node
    while current is not None:
        path.append(current)
        if current == start_node:
            break
        current = parent_map.get(current)
    path.reverse()
    return path


# ─────────────────────────────────────────────────────────────────────────────
# A* SEARCH  (heapq priority queue, visited matrix for duplicate detection)
print("Running A* search ...")
start_time = time.time()

child_to_parent = {start_state: None}
g_score = {start_state: 0.0}

# Mark start as visited

# heap entries: (f_cost, g_cost, state)
open_heap = []
heapq.heappush(open_heap, (heuristic(start_state, goal_state), 0.0, start_state))

# Store all exploration edges for post-search animation
explored_edges = []   # list of ((x1,y1), (x2,y2)) in pygame coords

end = 0
goal_reached_state = None
counter = 0

while open_heap:
    pump()

    # Get node with lowest cost
    f_cost, g_cost, current_node = heapq.heappop(open_heap)

    # Convert to visited index
    row, col, angle_idx = get_visited_index(*current_node)

    # Skip if already visited
    if visited_matrix[row, col, angle_idx]:
        continue

    # Mark as visited (closed set)
    visited_matrix[row, col, angle_idx] = True

    # Check if goal reached
    if is_goal_reached(current_node, goal_state):
        goal_reached_state = current_node
        end = 1
        print(f"Goal reached: {current_node}")
        break

    # Explore neighbors
    neighbors = get_neighbors(current_node, L)

    for neighbor_node, cost in neighbors:
        n_row, n_col, n_angle_idx = get_visited_index(*neighbor_node)

        # Skip if already visited
        if visited_matrix[n_row, n_col, n_angle_idx]:
            continue

        # Compute new cost
        new_g_cost = g_cost + cost

        # Check if this path is better
        if neighbor_node not in g_score or new_g_cost < g_score[neighbor_node]:
            g_score[neighbor_node] = new_g_cost

            # Compute total cost
            f_cost_new = new_g_cost + heuristic(neighbor_node, goal_state)

            # Add to priority queue
            heapq.heappush(open_heap, (f_cost_new, new_g_cost, neighbor_node))

            # Track parent for path reconstruction
            child_to_parent[neighbor_node] = current_node

            # Save for visualization
            explored_edges.append((
                (current_node[0], current_node[1]),
                (neighbor_node[0], neighbor_node[1])
            ))

    # Progress counter
    counter += 1

    if counter % 20000 == 0:
        print(f"Iterations: {counter}, Open list size: {len(open_heap)}")

elapsed = time.time() - start_time
print(f"\nSearch completed in {elapsed:.3f} s")
print(f"Total nodes explored: {counter}")

# ─────────────────────────────────────────────────────────────────────────────
# RECONSTRUCT OPTIMAL PATH
shortest_path = []
if end == 1:
    shortest_path = backtrack(goal_reached_state, start_state, child_to_parent)
    print(f"Optimal path length: {len(shortest_path)} nodes")
else:
    print("No path found.")


# ─────────────────────────────────────────────────────────────────────────────
# VISUALIZATION  – starts only AFTER search and path are complete (required)
print("\nStarting visualization ...")

# --- Phase 1: animate node exploration ---
for i, (p1, p2) in enumerate(explored_edges):
    pump()
    pygame.draw.line(surface, visited_color, p1, p2, 1)

    if i % 30 == 0:   # update every 30 steps
        pygame.display.update()

# --- Phase 2: draw optimal path ---
if shortest_path and len(shortest_path) > 1:
    for i in range(len(shortest_path) - 1):
        pump()
        x1, y1, _ = shortest_path[i]
        x2, y2, _ = shortest_path[i + 1]
        pygame.draw.line(surface, path_color, (x1, y1), (x2, y2), 2)
        pygame.display.update()
        pygame.time.delay(15)

# --- Draw start / goal markers on top ---
pygame.draw.circle(surface, start_color,
                   (start_state[0], start_state[1]), 5)
goal_draw = goal_reached_state if goal_reached_state else goal_state
pygame.draw.circle(surface, goal_color,
                   (goal_draw[0], goal_draw[1]), 5)
pygame.display.update()

print(f"Total runtime: {time.time() - start_time:.3f} s")
print("Close the pygame window to exit.")

# Keep window open until user closes it
while True:
    pump()
    pygame.time.delay(30)
