from logic import *
import pygame
from pygame.locals import *
from maze import *
from backtostart import *
from material import *

class Game:

  def __init__(self):
    pygame.init()
    self.screen = pygame.display.set_mode((700,700), 0, 32)
    self.screen.fill(white)
    self.fpsClock = pygame.time.Clock()
    self.board = Maze()
    self.loadMap()
    self.font = pygame.font.Font('freesansbold.ttf', 20) 

  def loadMap(self):
    self.board.loadMap("map.txt")
    
  def drawAgent(self, i, j):
    #pygame.draw.rect(self.screen, red, (x*20, y*20, square_width, square_height), 0)
    self.screen.blit("A", (j*40, i*40, 40, 40))

  def drawSquare(self, i, j):
    pygame.draw.rect(self.screen, white, (j*40, i*40, 40, 40), 2)

  def drawWumpus(self, i, j):
    #pygame.draw.rect(self.screen, blue, (x*20, y*20, square_width, square_height), 0)
    self.screen.blit("W", (j*40, i*40, 40, 40))

  def drawPit(self, i, j):
    #pygame.draw.rect(self.screen, purple, (x*20, y*20, square_width, square_height), 0)
    self.screen.blit("P", (j*40, i*40, 40, 40))

  def drawStench(self, i, j):
    self.screen.blit("S", (j*40, i*40, 40, 40))
  
  def drawBreeze(self, i, j):
    self.screen.blit("B", (j*40, i*40, 40, 40))

  def drawLabel(self, i, j, label):
    text = self.font.render(label, True, white)
    textRect = text.get_rect()
    textRect.center = (j*40+20, i*40+20)
    self.screen.blit(text, textRect)

  def drawMap(self, m, N):
    self.screen.fill(black)
    filename = 'map.txt'
    for i in range(N):
      for j in range(N):
        if(m[i][j] != '-'):
          self.drawLabel(i, j, m[i][j])
        self.drawSquare(i, j)

  def moveAgent(self, s, d, m):
    self.erase(s[0], s[1])
    self.drawLabel(d[0], d[1], 'A')
    if(m[s[0]][s[1]] != '-'):
      self.drawLabel(s[0], s[1], m[s[0]][s[1]])
  
  def erase(self, i, j):
    pygame.draw.rect(self.screen, black, (j*40, i*40, 40, 40))
    self.drawSquare(i,j)
  
  def play(self):

    while(True):
      N = self.board.N
      m = self.board.map
      freq_table = [[0 for i in range(N)] for j in range(N)]
      current = (9, 0)
      prev = current
      cnt = 0
      kb = True
      safe_list = []

      visited = [[0 for i in range(N)] for j in range(N)]
      before = [[(-1, -1) for i in range(N)] for j in range(N)]
      cur_exit_length = 0
      start = (9, 0)

      self.drawMap(m, N)
      for event in pygame.event.get():
        if event.type == QUIT:
          exit() 
      while(cnt <= 150):

        i,j = current
        visited[i][j] = True

        if(current != prev):
          self.moveAgent(prev, current, m)
          pygame.display.update()
          self.fpsClock.tick(9)

        moved = False
        print('current: {}, prev: {}'.format(current, prev))
        next_move = findNextMoveOf(i,j,N)
        #print(next_move)
        if(isSafe(i, j, start, m)):
          kb = And(kb, union(i, j, m, N))
          #print(kb)
          for d in range(len(next_move)):
            if(checkNextMove(d, next_move, freq_table)):
              freq_table[next_move[d][0]][next_move[d][1]] += 1
              prev = current
              current = next_move[d]
              moved = True
              kb = And(kb, union(next_move[d][0], next_move[d][1], m, N))
              break

        else:
          kb = And(kb, union(i, j, m, N))
          #print(kb)
          result = satisfiable(And(kb, union(i, j, m, N)))
          #print(result)
          possible = [k for k,v in result.items() if v == False]
          safe = buildSafeList(possible, kb)
          if(len(safe) == 0):
            current = prev
          else:
            safe_list += safe
            for d in range(len(next_move)):
              if(checkNextMove(d, next_move, freq_table) and (next_move[d][0], next_move[d][1]) in safe_list):
                freq_table[next_move[d][0]][next_move[d][1]] += 1
                prev = current
                current = next_move[d]
                moved = True
                kb = And(kb, union(next_move[d][0], next_move[d][1], m, N))
                break
        #print('move to: ' + str(current))
        # print(freq_table)
        #-----------------SUA CHO NAY -------------------#
        if(moved == False):
          BFS(current, start, visited, before, freq_table, N)
          way_to_exit = path(before, current, start)
          print(way_to_exit)
          cur_exit_length = len(way_to_exit)
          print(cur_exit_length)
          break
        #------------------------------------------------#
        cnt+=1
