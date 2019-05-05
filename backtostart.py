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
    #print("da vao ham")
    queue = [current]
    state = queue.pop(0)
    i, j= state
    visited[i][j] = 1
    #print("sap toi r")
    while True:
        i, j = state
        if(i + 1 < n):
            #print("ok")
            #print(visited[i + 1][j])
            #print(f_table[i + 1][j])
            if (visited[i + 1][j] == 0 and f_table[i+1][j]!=0):
                #print("ok1")
                visited[i + 1][j] = 1
                queue.append((i + 1, j))
                before[i+1][j] = state
                #print("da vao 1")

        if(i - 1 >= 0):
            #print("ok")
            #print(visited[i - 1][j])
            #print(f_table[i - 1][j])
            if (visited[i-1][j] == 0 and f_table[i-1][j]!=0):
                #print("ok2")
                visited[i-1][j] = 1
                queue.append((i - 1, j))
                before[i-1][j] = state
                #print("da vao 2")

        if(j + 1 < n):
            if (visited[i][j+1] == 0 and f_table[i][j + 1]!=0):
                visited[i][j+1] = 1
                queue.append((i, j+1))
                before[i][j+1] = state
                #print("da vao 3")

        if(j - 1 >= 0):
            if (visited[i][j-1] == 0 and f_table[i][j - 1]!=0):
                visited[i][j-1] = 1
                queue.append((i, j-1))
                before[i][j-1] = state
                #print("da vao 4")

        if len(queue) == 0:
            break
        else:
            state = queue.pop(0)

        if state == start:
            break

def path(before, current, start):
    result = []
    if(before[start[0]][start[1]] == (-1, -1)):
        return result
    temp = start
    result.append(temp)
    while(before[temp[0]][temp[1]]!=current):
        result.append(before[temp[0]][temp[1]])
        temp = before[temp[temp[0]][temp[1]]]
    result.append(current)
    result.reverse()
    return result   

# def length_path(before, current, start):
#     result = []
#     if(before[start] == (-1, -1)):
#         return result
#     temp = start
#     result.append(temp)
#     while(before[temp]!=current):
#         result.append(before[temp])
#         temp = before[temp]
#     result.append(current)
#     result.reverse()
#     l = len(result)
#     return l   


#print(visited[5][6])