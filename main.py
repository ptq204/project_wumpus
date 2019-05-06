import os
from game import Game

if __name__ == "__main__":
  print(
    "1. map.txt\n" + 
    "2. map01.txt\n")
  m = str(input("Choose map: "))
  print(m)
  os.system("python graphic.py " + m)
  exit()