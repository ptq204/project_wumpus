from sympy import Symbol, symbols
from sympy.logic.boolalg import ITE, And, Xor, Or, Not
from sympy.logic.inference import satisfiable
x, y = symbols('x,y')

m = [['S', '-', 'B', 'P'], ['W', 'BS', 'P', 'B'], ['S', '-', 'B', '-'], ['A', 'B', 'P', 'B']]
N = 4
#(4,4)
#(1,1)

freq_table = [[0 for i in range(N)] for j in range(N)]
safe_list = []

current = (3,0)
kb = True

def check(i, j):
  tmp = []
  pmt = []
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
  #print(kb_o)
  #print(kb_a)
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
  global safe_list, kb
  f = {}
  t = True
  for pos in possible:
    index = str(pos).split('_')[1]
    if(not (index in f)):
      f[index] = 1
    else:
      f[index] += 1
    if(f[index] == 2):
      w = symbols('W_'+index)
      p = symbols('P_'+index)
      kb = And(kb, And(w,p))
      safe_list.append((int(index[0]), int(index[1])))

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
    if(next_move[i] <= next_move[j]):
      c += 1
  return (c == len(next_move) - (i+1))

cnt = 0
kb = True
kb = And(kb, union(current[0],current[1]))

print(union(3,0))
while(True):
  i,j = current
  print(current)
  next_move = []
  up = (i-1,j)
  right = (i,j+1)
  left = (i,j-1)
  down = (i+1,j)
  if(up[0] >=0 and up[0] < N and up[1] >= 0 and up[1] <= N):
    next_move.append(up)
  if(right[0] >=0 and right[0] < N and right[1] >= 0 and right[1] <= N):
    next_move.append(right)
  if(left[0] >=0 and left[0] < N and left[1] >= 0 and left[1] <= N):
    next_move.append(left)
  if(down[0] >=0 and down[0] < N and down[1] >= 0 and down[1] <= N):
    next_move.append(down)
  if(isSafe(i, j)):
    kb = And(kb, union(i,j))
    print(kb)
    for d in range(len(next_move)):
      if(checkNextMove(d, next_move)):
        freq_table[next_move[d][0]][next_move[d][1]] += 1
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
      print(kb)
      result = satisfiable(And(kb, union(i,j)))
      print(result)
      possible = [k for k,v in result.items() if v == False]
      buildSafeList(possible)
      if((current[0]-1, current[1]) in safe_list):
        tmp = (current[0]-1, current[1])
        current = tmp
      elif((current[0], current[1]+1) in safe_list):
        tmp = (current[0], current[1]+1)
        current = tmp
      elif((current[0], current[1]-1) in safe_list):
        tmp = (current[0], current[1]-1)
        current = tmp
      elif((current[0]+1, current[1]) in safe_list):
        tmp = (current[0]+1, current[1])
        current = tmp
      print('move to: ' + str(current))
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
