from sympy import Symbol, symbols
from sympy.logic.boolalg import ITE, And, Xor, Or, Not
from sympy.logic.inference import satisfiable
from backtostart import *

def check(i, j, m, N):
  tmp = [] # Or list
  pmt = [] # And list
  pmt.append('W_' + str(i) + str(j))
  pmt.append('P_' + str(i) + str(j))

  if(m[i][j] == 'S' or m[i][j] == 'SG' or m[i][j] == 'GS'):
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

  elif(m[i][j] == 'B' or m[i][j] == 'BG' or m[i][j] == 'GB'):
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

  elif(m[i][j] == 'BS' or m[i][j] == 'SB' or len(m[i][j]) == 3):
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

def union(i,j, m, N):
  o = False
  a = True
  t = True
  kb_o, kb_a = check(i,j, m, N)
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

def isSafe(i, j, start, m):
  return ((m[i][j] == '-') or (i == start[0] and j == start[1]))

def buildSafeList(possible, kb, safe_list):
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
      if(not (int(index[0]), int(index[1])) in safe_list):
        safe.append((int(index[0]), int(index[1])))
  return safe

def checkNextMove(i, next_move, freq_table):
  c = 0
  for j in range(i+1,len(next_move)):
    if(freq_table[next_move[i][0]][next_move[i][1]] <= freq_table[next_move[j][0]][next_move[j][1]]):
      c += 1
  return (c == len(next_move) - (i+1))

def findNextMoveOf(i,j,N):
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

def findPathOfGame(m, N, start):
  freq_table = [[0 for i in range(N)] for j in range(N)]
  freq_table[start[0]][start[1]] = 1000
  current = start
  prev = current
  cnt = 0
  kb = True
  safe_list = []
  move_path = [current]
  visited = [[0 for i in range(N)] for j in range(N)]
  before = [[(-1, -1) for i in range(N)] for j in range(N)]
  cur_exit_length = 0

  indx = 0
  while(cnt <= 150):

    i,j = current
    print(current)
    if(m[i][j] == 'W' or m[i][j] == 'P' or m[i][j] == 'WP' or m[i][j] == 'PW'):
      break
    if(current != prev):
      move_path.append(current)
      indx+=1
    
    moved = False
    # print('current: {}, prev: {}'.format(current, prev))
    next_move = findNextMoveOf(i,j,N)
    kb = And(kb, union(i, j, m, N))
    #print(next_move)
    if(isSafe(i, j, start, m)):
      #print(kb)
      for d in range(len(next_move)):
        if(checkNextMove(d, next_move, freq_table)):
          freq_table[next_move[d][0]][next_move[d][1]] += 1
          prev = current
          current = next_move[d]
          moved = True
          break

    else:
      #print(kb)
      result = satisfiable(kb)
      #print(result)
      possible = [k for k,v in result.items() if v == False]
      safe = buildSafeList(possible, kb, safe_list)
      print(safe)
      if(len(safe) == 0):
        current = prev
        indx -= 1
        prev = move_path[indx]
        #print('{} {}'.format(safe, current))
        moved = True
      else:
        #print(safe)
        safe_list += safe
        for d in range(len(next_move)):
          if(checkNextMove(d, next_move, freq_table) and (next_move[d][0], next_move[d][1]) in safe_list):
            freq_table[next_move[d][0]][next_move[d][1]] += 1
            prev = current
            current = next_move[d]
            moved = True
            break
        if(moved == False):
          current = prev
          indx -= 1
          prev = move_path[indx]
          moved = True
    #print('move to: ' + str(current))
    # print(freq_table)
    #-----------------SUA CHO NAY -------------------#
    if(moved == False or cnt == 150):
      # print(freq_table)
      BFS(current, start, visited, before, freq_table, N)
      print(satisfiable(kb))
      way_to_exit = path(before, current, start)
      if (len(way_to_exit) != 0):
        way_to_exit.pop(0)
      # print(way_to_exit)
      cur_exit_length = len(way_to_exit)
      # print(cur_exit_length)
      break
    #------------------------------------------------#
    cnt+=1
  return move_path + way_to_exit

'''def up(pos):
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
'''