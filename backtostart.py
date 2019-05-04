import numpy as np

N = 10
visited = [[0 for i in range(N)] for j in range(N)]

before = [[(-1, -1) for i in range(N)] for j in range(N)]

def BFS(current, start, visited, before, f_table):
    queue = [current]
    state = queue.pop(0)
    visited[state] = 1
    while True:
        if (visited[(state[0] + 1, state[1])] == 0 and f_table[state[0]+1][state[1]]!=0):
            visited[(state[0]+1, state[1])] = 1
            queue.append((state[0] + 1, state[1]))
            before[(state[0] + 1, state[1])] = state

        if (visited[(state[0] - 1, state[1])] == 0 and f_table[state[0]-1][state[1]]!=0):
            visited[(state[0]-1, state[1])] = 1
            queue.append((state[0] - 1, state[1]))
            before[(state[0] - 1, state[1])] = state

        if (visited[(state[0], state[1] + 1)] == 0 and f_table[state[0]][state[1] + 1]!=1):
            visited[(state[0], state[1]+1)] = 1
            queue.append((state[0], state[1]+1))
            before[(state[0], state[1]+1)] = state

        if (visited[(state[0], state[1] - 1)] == 0 and f_table[state[0]][state[1] - 1]!=1):
            visited[(state[0], state[1]-1)] = 1
            queue.append((state[0], state[1]-1))
            before[(state[0], state[1]-1)] = state

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