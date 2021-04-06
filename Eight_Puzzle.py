# Đây là Mã Thử nghiệm cho trò chơi tự phá, giải Xếp hình 9 ô gạch: Bằng thuật toán IDS
# Có tham khảo, sử dụng 1 phần code mẫu của thầy: Trần Nhật Quang, Khoa Công Nghệ Thông Tin, Trường đại học Sư Phạm Kỹ thuật TPHCM, link:https://drive.google.com/file/d/1ETiq6jE12yHC6CXmrIniGPabz7FQTh_-/view?usp=sharing

import sys
import random as rd
from random import choice
from collections import deque
import time
import itertools

class Node:
    def __init__(self, state, parent = None, action = None, path_cost = 0):    
        self.state = state # trạng thái hiện tại của hình cần xếp
        self.parent = parent # trạng thái trước đó
        self.action = action # bước đi ~ 'UP', 'DOWN', 'LEFT', 'RIGHT'
        self.path_cost = path_cost
        self.depth = 0 # độ sâu hiện tại
        if parent:
            self.depth = parent.depth + 1

    def Expand(self, problem): # Tập các node con được sinh ra
        """Trả về danh sách các Node con được sinh ra với các Action-bước đi tương ứng"""
        return [self.Child_Node(problem, action) for action in problem.action(self.state)]

    def Child_Node(self, problem, action): # Khởi tạo node con kế tiếp
        """Trả về một ChildNode-Nút con mới tạo ra khi thực hiện Action"""
        next_state = problem.Result(self.state, action)
        next_node = Node(next_state, self, action, problem.path_cost(self.path_cost, self.state, action, next_state))
        return next_node

    def solution(self): # chuỗi action
        """Xuất ra danh sách thứ tự các action dẫn đến trạng thái node hiện tại"""
        return [node.action for node in self.path()[1:]]

    def path(self): # đường đi
        """Xuất ra danh sách các node đã đi qua để dẫn đến trạng thái node hiện tại"""
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))


def BFS(problemm):
    global node
    frontier = list([node]) # FIFO
    explored = list()       # contains the explored statuses
    
    while frontier:
        node = frontier.pop(0)                          #FIFO
        if node.state not in explored:  
            explored.append(node.state)                 #explored node
        for action in problem.action(node.state):   
            child = node.Child_Node(problem, action)    #explain node
            if(child not in explored or child not in frontier):
                if(problem.goal_test(child.state)):
                    return child
                frontier.append(child)

def DFS(problemm):
    global node
    frontier = list([node]) # LIFO
    explored = list()       # contains the explored statuses
    
    while frontier:
        node = frontier.pop()                           #LIFO
        if node.state not in explored:  
            explored.append(node.state)                 #explored node
        for action in problem.action(node.state):   
            child = node.Child_Node(problem, action)    #explain node
            if(child not in explored or child not in frontier):
                if(problem.goal_test(child.state)):
                    return child
                frontier.append(child)

def Uniform_Cost_Search(problem):
    global node
    frontier = list([node]) # Priority queue
    explored = list()       # contains the explored statuses
    
    while frontier:
        print(len(frontier))
        node = frontier.pop(frontier.index(min(frontier, #Priority queue
                key=lambda path_cost : node.path_cost))) #choose the lowest cost
        if(problem.goal_test(node.state)):
            return node
        if node.state not in explored:
            explored.append(node.state)                     #explored node 
        for action in problem.action(node.state):
            child = node.Child_Node(problem, action)        #explained node
            if(child not in explored or child not in frontier):
                frontier.append(child)                      #add to frontier
            elif(child in frontier):
                for i in frontier:
                    if i == child and child.path < i.path:
                        frontier[i] = child                 #replace with lower value




def Depth_Limit_Search(node, problem, limit):
    frontier = list([node])     # LIFO
    explored = list()           # contains the explored statuses
    explored_depth = list()     # contains the depth of the explored statuses

    while frontier: 
        node = frontier.pop()
        if node.state not in explored:
            explored.append(node.state)
            explored_depth.append(node.depth)
        if problem.goal_test(node.state):
            return node
        else:
            for child in node.Expand(problem):
                if child.depth <= limit:          # 1. Current depth does not exceed Limit       
                    if child not in frontier:                   # 2. not in frotier
                        if child.state not in explored:         # 3. not in explored
                            if problem.goal_test(child.state):
                                return child
                            else: frontier.append(child)        # push child in frontier
                        elif explored_depth[explored.index(child.state)] > child.depth: 
                            explored_depth[explored.index(child.state)] = child.depth
                            if problem.goal_test(child.state):
                                return child
                            else: frontier.append(child)        # push child in frontier
                else: break
    return None

def IDLS(problem, node):
    depthlimit = 0
    # Use itertools to run the endless loop
    for depthlimit in itertools.count():
        result = Depth_Limit_Search(node, problem, limit=depthlimit)
        if result != None:
            break
    return result

class EightPuzzleProblem:
    def __init__(self, initial, goal = (0, 1, 2, 3, 4, 5, 6, 7, 8)):
        self.initial = initial # trạng thái ban đầu
        self.goal = goal # trạng thái đích

    def action (self, state): # các action có thể thực hiện
        """Trả về chuỗi các Action có thể thực hiện ở trạng thái State hiện tại"""
        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index_blank_square = self.find_blank_square(state)

        # Xóa bớt các nước đi bị hạn chế
        if index_blank_square % 3 == 0:
            possible_actions.remove('LEFT')
        if index_blank_square < 3:
            possible_actions.remove('UP')
        if index_blank_square % 3 == 2:
            possible_actions.remove('RIGHT')
        if index_blank_square > 5:
            possible_actions.remove('DOWN')

        return possible_actions

    def path_cost(self, c, state1, action, state2):
        return c + 1

    def goal_test(self, state):
        """Trả về giá trị True nếu State-trạng thái hiện tại trùng với Goal-trạng thái đích"""
        return state == self.goal

    def find_blank_square(self, state):
        """Trả về vị trí của ô trống-số 0 trong State"""
        return state.index(0)

    def Result(self, state, action):
        """Ở State hiện tại thực hiện Action để đạt được State mới
        Trả về Trạng thái mới-new_state"""
        blank = self.find_blank_square(state)
        new_state = list(state)

        delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank] # tráo đổi 2 trạng thái (di chuyển ô trắng)
        return tuple(new_state)

def random(problem, random_level):
    """Trả về một Node có state bất kì"""
    x = rd.randint(20,random_level)
    node = Node(problem.goal)
    exlored = set()
    exlored.add(node.state)
    while x > 0:
        temp = choice(node.Expand(problem))
        while temp.state in exlored:
            temp = choice(node.Expand(problem))
        node = temp
        exlored.add(node)
        x = x - 1
    return node

def solve(initialState):
    #initial = tuple([int(input()),int(input()),int(input()),int(input()),int(input()),int(input()),int(input()),int(input()),int(input())]
    problem = EightPuzzleProblem(initial=None, goal=(0, 1, 2, 3, 4, 5, 6, 7, 8))
    problem.initial = initialState 

    node = Node(problem.initial)

    start = time.time()
    result = IDLS(problem, node)
    # another way
#    result = BFS(problem)
    end = time.time()

    yield result.solution()
    yield end-start


if __name__ =='__main__':
    problem = EightPuzzleProblem(initial=(1,8,2,3,0,5,4,7,6), goal=(0, 1, 2, 3, 4, 5, 6, 7, 8))
    node = Node(problem.initial)
    result = IDLS(problem, node)
    print(result.solution())   


#print(solve((1,8,2,3,0,5,4,7,6)))