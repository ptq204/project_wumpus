from sympy import Symbol, symbols
from sympy.logic.boolalg import ITE, And, Xor, Or, Not
from sympy.logic.inference import satisfiable
x, y = symbols('x,y')

m = [['S', '-', 'B', 'P'], ['W', 'BS', 'P', 'B'], ['S', '-', 'B', '-'], ['A', 'B', 'P', 'B']]
M = 4
N = 4
#(4,4)
#(1,1)

def check(i, j, current):
  tmp = []
  pmt = []
  if(len(m[i][j]) == 1):
    if(m[i][j] == 'S'):
      if(i-1 >= 0 and (i-1 != current[0] or j != current[1])):
        tmp.append('W_' + str(i-1) + str(j))
        pmt.append('P_' + str(i-1) + str(j))
      if(j+1 < N and (i != current[0] or j+1 != current[1])):
        tmp.append('W_' + str(i) + str(j+1))
        pmt.append('P_' + str(i) + str(j+1))
      if(i+1 < M and (i+1 != current[0] or j != current[1])):
        tmp.append('W_' + str(i+1) + str(j))
        pmt.append('P_' + str(i+1) + str(j))
      if(j-1 >= 0 and (i != current[0] or j-1 != current[1])):
        tmp.append('W_' + str(i) + str(j-1))
        pmt.append('P_' + str(i) + str(j-1))
    elif(m[i][j] == 'B'):
      if(i-1 >= 0 and (i-1 != current[0] or j != current[1])):
        tmp.append('P_' + str(i-1) + str(j))
        pmt.append('W_' + str(i-1) + str(j))
      if(j+1 < N and (i != current[0] or j+1 != current[1])):
        tmp.append('P_' + str(i) + str(j+1))
        pmt.append('W_' + str(i) + str(j+1))
      if(i+1 < M and (i+1 != current[0] or j != current[1])):
        tmp.append('P_' + str(i+1) + str(j))
        pmt.append('W_' + str(i+1) + str(j))
      if(j-1 >= 0 and (i != current[0] or j-1 != current[1])):
        tmp.append('P_' + str(i) + str(j-1))
        pmt.append('W_' + str(i) + str(j-1))
  if(len(m[i][j]) == 2):
    if(i-1 >= 0 and (i-1 != current[0] or j != current[1])):
      tmp.append('W_' + str(i-1) + str(j))
      tmp.append('P_' + str(i-1) + str(j))
    if(j+1 < N and (i != current[0] or j+1 != current[1])):
      tmp.append('W_' + str(i) + str(j+1))
      tmp.append('P_' + str(i) + str(j+1))
    if(i+1 < M and (i+1 != current[0] or j != current[1])):
      tmp.append('W_' + str(i+1) + str(j))
      tmp.append('P_' + str(i+1) + str(j))
    if(j-1 >= 0 and (i != current[0] or j-1 != current[1])):
      tmp.append('W_' + str(i) + str(j-1))
      tmp.append('P_' + str(i) + str(j-1))
  return (tmp, pmt)

current = (3,0)

def union(i,j,current):
  kb = []
  o = False
  a = True
  t = True
  kb_o, kb_a = check(i,j,current)
  for k in kb_o:
    x = symbols(k)
    o = Or(o,x)
  for k in kb_a:
    x = symbols(k)
    a = And(a,Not(x))
  t = And(o, a)
  return t

c = union(2,0,current)
print(c)
d = union(3,1,current)
print(d)

result = satisfiable(And(c,d))
for label in result:
  if(result[label] == True):
    print(label)
'''print((y & x).subs({x: True, y: True}))
a,b,c,d,e,f,g,h = symbols('a,b,c,d,e,f,g,h')
print(And(a, b, c, d).subs({a: True, b: False, c: True, d: False, e: True, f: True, g: True, h: True}))'''
