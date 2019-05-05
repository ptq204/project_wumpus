from logic import *
import pygame
from pygame.locals import *
from maze import *
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
    m = self.board.map
    N = self.board.N
    path = findPathOfGame(m, N)
    while(True):
      self.drawMap(m, N)
      for event in pygame.event.get():
        if event.type == QUIT:
          exit()
      for i in range(len(path)):
        if(i > 0):
          self.moveAgent(path[i-1], path[i], m)
          pygame.display.update()
          self.fpsClock.tick(9)
