import sys, time
from sudoku import solve, Sudoku

def read_puzzles(path):
  with open(path) as f:
    for line in f.readlines():
      yield line.strip()


def timed_solve(puzzle):
  start = time.perf_counter()
  soln = solve(puzzle)
  end = time.perf_counter()
  return (soln, end - start)


if __name__ == '__main__':
  for values in read_puzzles(sys.argv[1]):
    puzzle = Sudoku(values)
    soln, sec = timed_solve(puzzle)
    print(f'{values}\n{repr(soln)} sec={sec:0.3f}')
