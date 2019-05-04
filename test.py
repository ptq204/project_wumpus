from sympy import Symbol, symbols
from sympy.logic.boolalg import ITE, And, Xor, Or, Not
from sympy.logic.inference import satisfiable
from backtostart import *
x, y = symbols('x,y')

#m = [['S', '-', 'B', 'P'], ['W', 'BS', 'P', 'B'], ['S', '-', 'B', '-'], ['A', 'B', 'P', 'B']]
#N = 4
#(4,4)
#(1,1)


#freq_table = [[0 for i in range(N)] for j in range(N)]
N = -1
m = [[]]
freq_table = [[]]

def loadMap():
  global N, m, freq_table
  f = open('map.txt')
  N = int(f.readline())
  m = [[j for j in line.split()] for line in f]
  print(m)
  freq_table = [[0 for i in range(N)] for j in range(N)]

current = (9,0)
prev = current
cnt = 0
kb = True
loadMap()
safe_list = []

#---------------------------SUA CHO NAY
visited = {}
before = {}

visited = initvisited(m)
before = initbefore(m)
cur_exit_length = 0
start = (9, 0)
#-----------------------

def check(i, j):
  tmp = []
  pmt = []
  pmt.append('W_' + str(i) + str(j))
  pmt.append('P_' + str(i) + str(j))
  if(len(m[i][j]) == 1):
    if(m[i][j] == 'S'):
      if(i-1 >= 0):
        tmp.append('W_' + str(i-1) + str(j))
        pmt.append('P_' + str(i-1) + str(j))
      if(j+1 < N):
        tmp.append('W_' + str(i) + str(j+1))
        pmt.append('P_' + str(i) + str(j+1))
      if(i+1 < N):
        tmp.append('W_' + str(i+1) + str(j))
        pmt.append('P_' + str(i+1) + str(j))
      if(j-1 >= 0):
        tmp.append('W_' + str(i) + str(j-1))
        pmt.append('P_' + str(i) + str(j-1))
    elif(m[i][j] == 'B'):
      if(i-1 >= 0):
        tmp.append('P_' + str(i-1) + str(j))
        pmt.append('W_' + str(i-1) + str(j))
      if(j+1 < N):
        tmp.append('P_' + str(i) + str(j+1))
        pmt.append('W_' + str(i) + str(j+1))
      if(i+1 < N):
        tmp.append('P_' + str(i+1) + str(j))
        pmt.append('W_' + str(i+1) + str(j))
      if(j-1 >= 0):
        tmp.append('P_' + str(i) + str(j-1))
        pmt.append('W_' + str(i) + str(j-1))
    elif(m[i][j] == '-'):
      if(i-1 >= 0):
        pmt.append('P_' + str(i-1) + str(j))
        pmt.append('W_' + str(i-1) + str(j))
      if(j+1 < N):
        pmt.append('P_' + str(i) + str(j+1))
        pmt.append('W_' + str(i) + str(j+1))
      if(i+1 < N):
        pmt.append('P_' + str(i+1) + str(j))
        pmt.append('W_' + str(i+1) + str(j))
      if(j-1 >= 0):
        pmt.append('P_' + str(i) + str(j-1))
        pmt.append('W_' + str(i) + str(j-1))
  if(len(m[i][j]) == 2):
    if(i-1 >= 0):
      tmp.append('W_' + str(i-1) + str(j))
      tmp.append('P_' + str(i-1) + str(j))
    if(j+1 < N):
      tmp.append('W_' + str(i) + str(j+1))
      tmp.append('P_' + str(i) + str(j+1))
    if(i+1 < N):
      tmp.append('W_' + str(i+1) + str(j))
      tmp.append('P_' + str(i+1) + str(j))
    if(j-1 >= 0):
      tmp.append('W_' + str(i) + str(j-1))
      tmp.append('P_' + str(i) + str(j-1))
  return (tmp, pmt)

def union(i,j):
  o = False
  a = True
  t = True
  kb_o, kb_a = check(i,j)
  for k in kb_o:
    x = symbols(k)
    o = Or(o,x)
  for k in kb_a:
    x = symbols(k)
    a = And(a,Not(x))
  if(len(kb_o) == 0):
    t = And(True, a)
  else:
    t = And(o, a)
  #print(satisfiable(t))
  return t

def isSafe(i,j):
  return ((m[i][j] == '-') or (i == 3 and j == 0))

def buildSafeList(possible):
  global kb
  safe = []
  f = {}
  for pos in possible:
    index = str(pos).split('_')[1]
    if(not (index in f)):
      f[index] = 1
    else:
      f[index] += 1
    if(f[index] == 2):
      w = symbols('W_'+index)
      p = symbols('P_'+index)
      kb = And(kb, And(Not(w),Not(p)))
      safe.append((int(index[0]), int(index[1])))
  return safe

def up(pos):
  if(pos[0] - 1 >= 0):
    tmp = (pos[0] - 1, pos[1])
    print(tmp)
  else:
    tmp = (-1,-1)
  return tmp

def down(pos):
  if(pos[0]+1 < N):
    return (pos[0]+1,pos[1])
  return (-1, -1)

def left(pos):
  if(pos[1]-1 >= 0):
    return (pos[0],pos[1]-1)
  return (-1, -1)

def right(pos):
  if(pos[1]+1 < N):
    return (pos[0],pos[1]+1)
  return (-1, -1)

def checkNextMove(i, next_move):
  c = 0
  for j in range(i+1,len(next_move)):
    print((next_move[i][0], next_move[i][1]))
    if(freq_table[next_move[i][0]][next_move[i][1]] <= freq_table[next_move[j][0]][next_move[j][1]]):
      c += 1
  return (c == len(next_move) - (i+1))

def findNextMoveOf(i,j):
  next_move = []
  up = (i-1,j)
  right = (i,j+1)
  left = (i,j-1)
  down = (i+1,j)
  if(up[0] >=0 and up[0] < N and up[1] >= 0 and up[1] < N):
    next_move.append(up)
  if(right[0] >=0 and right[0] < N and right[1] >= 0 and right[1] < N):
    next_move.append(right)
  if(left[0] >=0 and left[0] < N and left[1] >= 0 and left[1] < N):
    next_move.append(left)
  if(down[0] >=0 and down[0] < N and down[1] >= 0 and down[1] < N):
    next_move.append(down)
  return next_move

'''-----------------------------------------------------------------------'''

kb = And(kb, union(current[0],current[1]))

while(cnt + cur_exit_length <= 150):
  i,j = current
  print(current)
  next_move = findNextMoveOf(i,j)
  #print(next_move)
  if(isSafe(i, j)):
    kb = And(kb, union(i,j))
    #print(kb)
    for d in range(len(next_move)):
      if(checkNextMove(d, next_move)):
        freq_table[next_move[d][0]][next_move[d][1]] += 1
        prev = current
        current = next_move[d]
        kb = And(kb, union(next_move[d][0], next_move[d][1]))
        break
    '''if(i-1 >= 0 and freq_table[up[0]][up[1]] <= freq_table[right[0]][right[1]] and freq_table[up[0]][up[1]] <= freq_table[left[0]][left[1]] and freq_table[up[0]][up[1]] <= freq_table[down[0]][down[1]]):
      freq_table[i-1][j] += 1
      current = up
      kb = And(kb, union(i-1,j))
      
    elif(j+1 < N and freq_table[right[0]][right[1]] <= freq_table[left[0]][left[1]] and freq_table[right[0]][right[1]] <= freq_table[down[0]][down[1]]):
      freq_table[i][j+1] += 1
      current = right
      kb = And(kb, union(i,j+1))
      
    elif(j-1 >= 0 and freq_table[left[0]][left[1]] <= freq_table[down[0]][down[1]]):
      freq_table[i][j-1] += 1
      current = left
      kb = And(kb, union(i,j-1))
    
    else:
      freq_table[i+1][j] += 1
      current = down
      kb = And(kb, union(i+1,j))'''

    '''result = satisfiable(kb)
    possible = [k for k,v in result.items() if v == False]
    safe_list = buildSafeList(possible)'''
 
  else:
      kb = And(kb, union(i,j))
      #print(kb)
      result = satisfiable(And(kb, union(i,j)))
      #print(result)
      possible = [k for k,v in result.items() if v == False]
      safe = buildSafeList(possible)
      if(len(safe) == 0):
        current = prev
      else:
        print(safe)
        '''if((current[0]-1, current[1]) in safe_list):
          tmp = (current[0]-1, current[1])
          freq_table[current[0]-1][current[1]] += 1
          current = tmp
        elif((current[0], current[1]+1) in safe_list):
          tmp = (current[0], current[1]+1)
          freq_table[current[0]][current[1]+1] += 1
          current = tmp
        elif((current[0], current[1]-1) in safe_list):
          tmp = (current[0], current[1]-1)
          freq_table[current[0]][current[1]-1] += 1
          current = tmp
        elif((current[0]+1, current[1]) in safe_list):
          tmp = (current[0]+1, current[1])
          freq_table[current[0]+1][current[1]] += 1
          current = tmp'''
        safe_list += safe
        for d in range(len(next_move)):
          if(checkNextMove(d, next_move) and (next_move[d][0], next_move[d][1]) in safe_list):
            freq_table[next_move[d][0]][next_move[d][1]] += 1
            prev = current
            current = next_move[d]
            kb = And(kb, union(next_move[d][0], next_move[d][1]))
            break
  #print('move to: ' + str(current))
  # print(freq_table)
  #-----------------SUA CHO NAY -------------------#
  BFS(current, start, visited, before, freq_table, N)
  way_to_exit = path(before, current, start)
  print(way_to_exit)
  cur_exit_length = len(way_to_exit)
  print(cur_exit_length)
  #------------------------------------------------#
  cnt+=1
'''
    if(j+1 < M):
      result = And(result, union(i,j+1,current))
    if(j-1 >= 0):
      result = And(result, union(i,j-1,current))
    if(i+1 < N):
      result = And(result, union(i+1,j,current))'''
  
'''print((y & x).subs({x: True, y: True}))
a,b,c,d,e,f,g,h = symbols('a,b,c,d,e,f,g,h')
print(And(a, b, c, d).subs({a: True, b: False, c: True, d: False, e: True, f: True, g: True, h: True}))'''
