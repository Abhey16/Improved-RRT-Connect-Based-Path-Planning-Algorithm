from ctypes import util
import os
import sys
import math
import copy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import time 
class Env:
    def __init__(self):
        self.x_range = (-5, 55)
        self.y_range = (-10, 10)
        self.obs_boundary = self.obs_boundary()
        self.obs_circle = self.obs_circle()
        self.obs_rectangle = self.obs_rectangle()

    @staticmethod
    def obs_boundary():
        obs_boundary = [
            [-6, -11, 1, 21],
            [-6, 10, 62, 1],
            [-6, -11, 62, 1],
            [55, -11, 1, 21]
        ]
        return obs_boundary

    @staticmethod
    def obs_rectangle():
        obs_rectangle = [
            [10, -2.5, 1.5, 12.5],
            [20, -10.0, 1.5, 12.5]
            ]
        return obs_rectangle

    @staticmethod
    def obs_circle():
        obs_cir = [
            [35, 1, 3]
        ]

        return obs_cir



class Plotting:
    def __init__(self, x_start, x_goal, x_mid):
        self.xI, self.xG = x_start, x_goal
        self.xM = x_mid
        self.env = Env()
        self.obs_bound = self.env.obs_boundary
        self.obs_circle = self.env.obs_circle
        self.obs_rectangle = self.env.obs_rectangle

    def animation_connect(self, V1, V2, V3, V4, path_t1, path_t2, name):
        self.plot_grid(name)
        self.plot_visited_connect(V1, V2, V3, V4)
        self.plot_path(path_t1,path_t2)
        # self.plot_path(path_t2)

    def plot_grid(self, name):
        fig, ax = plt.subplots()

        for (ox, oy, w, h) in self.obs_bound:
            ax.add_patch(
                patches.Rectangle(
                    (ox, oy), w, h,
                    edgecolor='black',
                    facecolor='black',
                    fill=True
                )
            )

        for (ox, oy, w, h) in self.obs_rectangle:
            ax.add_patch(
                patches.Rectangle(
                    (ox, oy), w, h,
                    edgecolor='black',
                    facecolor='gray',
                    fill=True
                )
            )

        for (ox, oy, r) in self.obs_circle:
            ax.add_patch(
                patches.Circle(
                    (ox, oy), r,
                    edgecolor='black',
                    facecolor='gray',
                    fill=True
                )
            )

        plt.plot(self.xI[0], self.xI[1], "bs", linewidth=3)
        plt.plot(self.xG[0], self.xG[1], "gs", linewidth=3)
        plt.plot(self.xM[0], self.xM[1], "ks", linewidth=3)

        plt.title(name)
        plt.axis("equal")

    
    @staticmethod
    def plot_visited_connect(V1, V2, V3, V4):
        len1, len2, len3, len4 = len(V1), len(V2), len(V3), len(V4)
        max_len = max(len1, len2, len3, len4)

        for k in range(max_len):
            if k < len1 and V1[k].parent:
                plt.plot([V1[k].x, V1[k].parent.x], [V1[k].y, V1[k].parent.y], "-g")
            if k < len2 and V2[k].parent:
                plt.plot([V2[k].x, V2[k].parent.x], [V2[k].y, V2[k].parent.y], "-g")
            if k < len3 and V3[k].parent:
                plt.plot([V3[k].x, V3[k].parent.x], [V3[k].y, V3[k].parent.y], "-g")
            if k < len4 and V4[k].parent:
                plt.plot([V4[k].x, V4[k].parent.x], [V4[k].y, V4[k].parent.y], "-g")

            plt.gcf().canvas.mpl_connect('key_release_event',
                                         lambda event: [exit(0) if event.key == 'escape' else None])

            if k % 2 == 0:
                plt.pause(0.001)

        plt.pause(0.01)


    @staticmethod
    def plot_path(path1,path2):
        if len(path1) != 0:
            plt.plot([x[0] for x in path1], [x[1] for x in path1], '-r', linewidth=2)
            plt.pause(0.01)

        if len(path2) != 0:
            plt.plot([x[0] for x in path2], [x[1] for x in path2], '-r', linewidth=2)
            plt.pause(0.01)

        plt.show()

class Utils:
    def __init__(self):
        self.env = Env()

        self.delta = 0.5
        self.obs_circle = self.env.obs_circle
        self.obs_rectangle = self.env.obs_rectangle
        self.obs_boundary = self.env.obs_boundary

    def update_obs(self, obs_cir, obs_bound, obs_rec):
        self.obs_circle = obs_cir
        self.obs_boundary = obs_bound
        self.obs_rectangle = obs_rec

    def get_obs_vertex(self):
        delta = self.delta
        obs_list = []

        for (ox, oy, w, h) in self.obs_rectangle:
            vertex_list = [[ox - delta, oy - delta],
                           [ox + w + delta, oy - delta],
                           [ox + w + delta, oy + h + delta],
                           [ox - delta, oy + h + delta]]
            obs_list.append(vertex_list)

        return obs_list

    def is_intersect_rec(self, start, end, o, d, a, b):
        v1 = [o[0] - a[0], o[1] - a[1]]
        v2 = [b[0] - a[0], b[1] - a[1]]
        v3 = [-d[1], d[0]]

        div = np.dot(v2, v3)

        if div == 0:
            return False

        t1 = np.linalg.norm(np.cross(v2, v1)) / div
        t2 = np.dot(v1, v3) / div

        if t1 >= 0 and 0 <= t2 <= 1:
            shot = Node((o[0] + t1 * d[0], o[1] + t1 * d[1]))
            dist_obs = self.get_dist(start, shot)
            dist_seg = self.get_dist(start, end)
            if dist_obs <= dist_seg:
                return True

        return False

    def is_intersect_circle(self, o, d, a, r):
        d2 = np.dot(d, d)
        delta = self.delta

        if d2 == 0:
            return False

        t = np.dot([a[0] - o[0], a[1] - o[1]], d) / d2

        if 0 <= t <= 1:
            shot = Node((o[0] + t * d[0], o[1] + t * d[1]))
            if self.get_dist(shot, Node(a)) <= r + delta:
                return True

        return False

    def is_collision(self, start, end):
        if self.is_inside_obs(start) or self.is_inside_obs(end):
            return True

        o, d = self.get_ray(start, end)
        obs_vertex = self.get_obs_vertex()

        for (v1, v2, v3, v4) in obs_vertex:
            if self.is_intersect_rec(start, end, o, d, v1, v2):
                return True
            if self.is_intersect_rec(start, end, o, d, v2, v3):
                return True
            if self.is_intersect_rec(start, end, o, d, v3, v4):
                return True
            if self.is_intersect_rec(start, end, o, d, v4, v1):
                return True

        for (x, y, r) in self.obs_circle:
            if self.is_intersect_circle(o, d, [x, y], r):
                return True

        return False

    def is_inside_obs(self, node):
        delta = self.delta

        for (x, y, r) in self.obs_circle:
            if math.hypot(node.x - x, node.y - y) <= r + delta:
                return True

        for (x, y, w, h) in self.obs_rectangle:
            if 0 <= node.x - (x - delta) <= w + 2 * delta \
                    and 0 <= node.y - (y - delta) <= h + 2 * delta:
                return True

        for (x, y, w, h) in self.obs_boundary:
            if 0 <= node.x - (x - delta) <= w + 2 * delta \
                    and 0 <= node.y - (y - delta) <= h + 2 * delta:
                return True

        return False

    @staticmethod
    def get_ray(start, end):
        orig = [start.x, start.y]
        direc = [end.x - start.x, end.y - start.y]
        return orig, direc

    @staticmethod
    def get_dist(start, end):
        return math.hypot(end.x - start.x, end.y - start.y)



class Node:
    def __init__(self, n):
        self.x = n[0]
        self.y = n[1]
        self.parent = None


class ImprovedRrtConnect:
    def __init__(self, s_start, s_goal, step_len, goal_sample_rate, iter_max):
        self.s_start = Node(s_start)
        self.s_goal = Node(s_goal)
        self.step_len = step_len
        self.goal_sample_rate = goal_sample_rate
        self.iter_max = iter_max
        self.V1 = [self.s_start]
        self.V2 = [self.s_goal]
        self.mid = self.search_third_node(x_start, x_goal)
        self.V3 = [Node(self.search_third_node(x_start, x_goal))]
        self.V4 = [Node(self.search_third_node(x_start, x_goal))]
        self.num_nodes=1
        self.env = Env()
        self.plotting = Plotting(s_start, s_goal, self.mid)
        self.utils = Utils()

        self.x_range = self.env.x_range
        self.y_range = self.env.y_range
        self.obs_circle = self.env.obs_circle
        self.obs_rectangle = self.env.obs_rectangle
        self.obs_boundary = self.env.obs_boundary

    def search_third_node(self, x_start, x_goal):
        # Example implementation of searching for the third node
        x_mid_x = (x_start[0] + x_goal[0]) / 2
        x_mid_y = (x_start[1] + x_goal[1]) / 2
        return (x_mid_x, x_mid_y)


    def planning(self):
        flag_1 = False
        flag_2 = False
        for i in range(self.iter_max):
            node_rand = self.generate_random_node(self.s_goal, self.goal_sample_rate)
            node_near1 = self.nearest_neighbor(self.V1, node_rand)
            node_new1 = self.new_state(node_near1, node_rand)

            if flag_1 == False:
                if node_new1 and not self.utils.is_collision(node_near1, node_new1):
                    self.V1.append(node_new1)
                    self.num_nodes+=1
                    node_near_prim = self.nearest_neighbor(self.V3, node_new1)
                    node_new_prim = self.new_state(node_near_prim, node_new1)

                    if node_new_prim and not self.utils.is_collision(node_new_prim, node_near_prim):
                        self.V3.append(node_new_prim)

                        while True:
                            node_new_prim2 = self.new_state(node_new_prim, node_new1)
                            if node_new_prim2 and not self.utils.is_collision(node_new_prim2, node_new_prim):
                                self.V3.append(node_new_prim2)
                                node_new_prim = self.change_node(node_new_prim, node_new_prim2)
                            else:
                                break

                            if self.is_node_same(node_new_prim, node_new1):
                                flag_1 = True
                                break

            node_near2 = self.nearest_neighbor(self.V4, node_rand)
            node_new2 = self.new_state(node_near2, node_rand)

            if flag_2 == False:
                if node_new2 and not self.utils.is_collision(node_near2, node_new2):
                    self.V4.append(node_new2)
                    self.num_nodes+=1
                    node_near_prim1 = self.nearest_neighbor(self.V2, node_new2)
                    node_new_prim1 = self.new_state(node_near_prim1, node_new2)

                    if node_new_prim1 and not self.utils.is_collision(node_new_prim1, node_near_prim1):
                        self.V2.append(node_new_prim1)

                        while True:
                            node_new_prim4 = self.new_state(node_new_prim1, node_new2)
                            if node_new_prim4 and not self.utils.is_collision(node_new_prim4, node_new_prim1):
                                self.V2.append(node_new_prim4)
                                node_new_prim1 = self.change_node(node_new_prim1, node_new_prim4)
                            else:
                                break

                            if self.is_node_same(node_new_prim1, node_new2):
                                flag_2 = True
                                break

            # if self.is_node_same(node_new_prim1, node_new) and self.is_node_same(node_new_prim, node_new):
            if flag_1 == True and flag_2 == True:
                path_t1 = self.extract_path(self,node_new1, node_new_prim)
                path_t2 = self.extract_path(self,node_new2, node_new_prim1)
                print(f"number of iterations: {i}")
                return path_t1, path_t2

            if len(self.V3) < len(self.V1):
                list_mid1 = self.V3
                self.V3 = self.V1
                self.V1 = list_mid1

            if len(self.V2) < len(self.V4):
                list_mid2 = self.V2
                self.V2 = self.V4
                self.V4 = list_mid2
                

        return None

    @staticmethod
    def change_node(node_new_prim, node_new_prim2):
        node_new = Node((node_new_prim2.x, node_new_prim2.y))
        node_new.parent = node_new_prim

        return node_new

    @staticmethod
    def is_node_same(node_new_prim, node_new):
        if node_new_prim.x == node_new.x and \
                node_new_prim.y == node_new.y:
            return True

        # if node_new_prim1.x == node_new.x and \
        #         node_new_prim1.y == node_new.y:
        #     return True

        return False

    def generate_random_node(self, sample_goal, goal_sample_rate):
        delta = self.utils.delta

        if np.random.random() > goal_sample_rate:
            return Node((np.random.uniform(self.x_range[0] + delta, self.x_range[1] - delta),
                         np.random.uniform(self.y_range[0] + delta, self.y_range[1] - delta)))

        return sample_goal

    @staticmethod
    def nearest_neighbor(node_list, n):
        return node_list[int(np.argmin([math.hypot(nd.x - n.x, nd.y - n.y)
                                        for nd in node_list]))]

    def new_state(self, node_start, node_end):
        dist, theta = self.get_distance_and_angle(node_start, node_end)

        dist = min(self.step_len, dist)
        node_new = Node((node_start.x + dist * math.cos(theta),
                         node_start.y + dist * math.sin(theta)))
        node_new.parent = node_start

        return node_new

    @staticmethod
    def extract_path(self,node_new, node_new_prim):
        path1 = [(node_new.x, node_new.y)]
        node_now = node_new

        while node_now.parent is not None:
            node_now = node_now.parent
            path1.append((node_now.x, node_now.y))

        path2 = [(node_new_prim.x, node_new_prim.y)]
        node_now = node_new_prim

        while node_now.parent is not None:
            node_now = node_now.parent
            path2.append((node_now.x, node_now.y))

        
        tree_density = self.num_nodes
        print("Tree density",tree_density)
        return list(list(reversed(path1)) + path2)

    @staticmethod
    def get_distance_and_angle(node_start, node_end):
        dx = node_end.x - node_start.x
        dy = node_end.y - node_start.y
        return math.hypot(dx, dy), math.atan2(dy, dx)

def cost_function(path):
    # Define a cost function
    cost = 0
    for i in range(len(path)-1):
    # Compute the Euclidean distance between two adjacent waypoints
        dist = np.linalg.norm(np.array(path[i+1]) - np.array(path[i]))
        # Add the distance to the total cost
        cost += dist
    return cost

def input_coordinates():

    #check if start and goal nodes are valid
    while True:
        start_node_str = input("Enter the coordinates of starting node (x,y):")
        goal_node_str = input("Enter the coordinates of Goal node (x,y):")
        
        start_node = tuple(map(int, start_node_str.split(',')))
        goal_node = tuple(map(int, goal_node_str.split(',')))      

        #Check if the start and goal node are valid
        # if is_valid(start_node[0],start_node[1]):
        if Utils().is_inside_obs(Node(start_node)) == False:

            if Utils().is_inside_obs(Node(goal_node)) == False:
                break
            else:
                print("Invalid goal node. Please enter valid coordinates.")
                continue
        else:
            print("Invalid start node. Please enter valid coordinates.")
            continue

    return start_node,goal_node


# input start and goal node coordinates
x_start,x_goal = input_coordinates()

rrt_conn = ImprovedRrtConnect(x_start, x_goal, 0.8, 0.05, 2000)
start_time=time.time()
path_t1 , path_t2 = rrt_conn.planning()


path1=np.array(path_t1)
path2=np.array(path_t2)

path1 = np.flip(path1, axis=0)
path1 = path1.tolist()
path2 = np.flip(path2, axis=0)
path2 = path2.tolist()

cost1=cost_function(path1)
cost2=cost_function(path2)
cost = cost1 + cost2

print("Path Cost\n",cost)
end_time=time.time()
computation_time=end_time-start_time
print("Computation time:",computation_time,"seconds")
rrt_conn.plotting.animation_connect(rrt_conn.V1, rrt_conn.V2, rrt_conn.V3, rrt_conn.V4, path1, path2, "IMPROVEDRRT_CONNECT")
