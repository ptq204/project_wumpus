import os
import glob
# from game import Game

if __name__ == "__main__":
  lf = glob.glob('*.txt')
  print("List of map: ")
  for filename in lf:
    filename = filename.split('.')[0]
    print(filename + ' ---> ' + filename[-1])
  m = str(input("Choose map: "))
  print(m)
  os.system("python graphic.py " + m)
  exit()