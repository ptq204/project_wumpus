import numpy as np

N = 10
visited = [[0 for i in range(N)] for j in range(N)]

before = [[(-1, -1) for i in range(N)] for j in range(N)]

def initbefore(graph):
    diction = {}
    for x in range (len(graph)):
        for y in range (len(graph[x])):
            diction[(x,y)] = (-1, -1) 
    return diction  

def initvisited(graph):
    diction = {}
    for x in range (len(graph)):
        for y in range (len(graph[x])):
            diction[(x,y)] = 0 
    return diction    

def BFS(current, start, visited, before, f_table, n):
    print("da vao 1")
    queue = [current]
    state = queue.pop(0)
    visited[state] = 1
    print("sap toi r")
    while True:
        if(state[0] + 1 < n):
            if (visited[(state[0] + 1, state[1])] == 0 and f_table[state[0]+1][state[1]]!=0):
                visited[(state[0]+1, state[1])] = 1
                queue.append((state[0] + 1, state[1]))
                before[(state[0] + 1, state[1])] = state
                print("da vao 1")

        if(state[0] - 1 >= 0):
            if (visited[(state[0] - 1, state[1])] == 0 and f_table[state[0]-1][state[1]]!=0):
                visited[(state[0]-1, state[1])] = 1
                queue.append((state[0] - 1, state[1]))
                before[(state[0] - 1, state[1])] = state
                print("da vao 2")

        if(state[1] + 1 < n):
            if (visited[(state[0], state[1] + 1)] == 0 and f_table[state[0]][state[1] + 1]!=0):
                visited[(state[0], state[1]+1)] = 1
                queue.append((state[0], state[1]+1))
                before[(state[0], state[1]+1)] = state
                print("da vao 3")

        if(state[1] - 1 >= 0):
            if (visited[(state[0], state[1] - 1)] == 0 and f_table[state[0]][state[1] - 1]!=0):
                visited[(state[0], state[1]-1)] = 1
                queue.append((state[0], state[1]-1))
                before[(state[0], state[1]-1)] = state
                print("da vao 4")

        if len(queue) == 0:
            break
        else:
            state = queue.pop(0)

        if state == start:
            break

def path(before, current, start):
    result = []
    if(before[start] == (-1, -1)):
        return result
    temp = start
    result.append(temp)
    while(before[temp]!=current):
        result.append(before[temp])
        temp = before[temp]
    result.append(current)
    result.reverse()
    return result   

def length_path(before, current, start):
    result = []
    if(before[start] == (-1, -1)):
        return result
    temp = start
    result.append(temp)
    while(before[temp]!=current):
        result.append(before[temp])
        temp = before[temp]
    result.append(current)
    result.reverse()
    l = len(result)
    return l   