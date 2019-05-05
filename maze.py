class Maze:

  def __init__(self):
    self.matrix = None
    self.N = None
    self.map = None

  def loadMap(self, filepath):
    f = open(filepath)
    self.N = int(f.readline())
    self.map = [[j for j in line.split()] for line in f]