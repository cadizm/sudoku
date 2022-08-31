from itertools import chain

def read_values(path):
  """
  Read `path` and return `values` string suitable for initializing a `Sudoku` puzzle.
  """
  return ''.join(list(map(lambda x: x.strip(), open(path).readlines()))).replace(' ', '')


def replace(s, index, value):
  """
  Replace a single character within string `s` and return it.
  """
  assert 0 <= index <= len(s)
  return ''.join(s[:index] + str(value) + s[index + 1:])


def next_unset_square(sudoku):
  """
  Return the 'next unset square' within the sudoku puzzle.

  Squares are ordered by increasing number of candidate values.
  Throws IndexError if no such candidate exists.
  """
  return sorted(filter(lambda x: x.val is None, chain(*sudoku.squares)), key=lambda x: len(x.candidates))[0]


def solve(sudoku):
  """
  Given a sudoku puzzle, find first unknown square and expand each candidate square into its own
  sudoku puzzle and recurse until solution found.
  """
  if sudoku.solved():
    return sudoku

  sq = next_unset_square(sudoku)
  for val in sq.candidates:
    candidate_values = replace(sudoku.values, sq.index, val)
    print(candidate_values)
    candidate_sudoku = solve(Sudoku(candidate_values))
    if candidate_sudoku is not None:  # found solution
      return candidate_sudoku


class Square:
  """
  Representation of a 'square' within a Sudoku puzzle grid.

  `index` is one of the 81 indices in the grid. Indices are numbered numerically left-to-right,
  top-to-bottom beginning at 0.
  `val` is the square's value (1-9 inclusive).
  `candidates` are the square's candidate values when `val` is not set.

   0  1  2   3  4  5   6  7  8
   9 10 11  12 13 14  15 16 17
  18 19 20  21 22 23  24 25 26

  27 28 29  30 31 32  33 34 35
  36 37 38  39 40 41  42 43 44
  45 46 47  48 49 50  51 52 53

  54 55 56  57 58 59  60 61 62
  63 64 65  66 67 68  69 70 71
  72 73 74  75 76 77  78 79 80
  """
  def __init__(self, index, val=None):
    self.index = index
    self.val = val
    self.candidates = []

  def box(self):
    """
    Return the 'box' this square belongs to.

    Boxes are represented using 0-based 2-tuple of `(row, column)`:

             0     |      1     |      2
      + ------------------------------------ +
      |  0   1   2 |  3   4   5 |  6   7   8 |
    0 |  9  10  11 | 12  13  14 | 15  16  17 |
      | 18  19  20 | 21  22  23 | 24  25  26 |
      | ------------------------------------ |
      | 27  28  29 | 30  31  32 | 33  34  35 |
    1 | 36  37  38 | 39  40  41 | 42  43  44 |
      | 45  46  47 | 48  49  50 | 51  52  53 |
      | ------------------------------------ |
      | 54  55  56 | 57  58  59 | 60  61  62 |
    2 | 63  64  65 | 66  67  68 | 69  70  71 |
      | 72  73  74 | 75  76  77 | 78  79  80 |
      + ------------------------------------ +
    """
    return (self.index // 27, (self.index % 9) // 3)

  def __repr__(self):
    return f'{self.val or "."}'

  def __str__(self):
    return self.__repr__()


class Sudoku:
  """
  Representation of a `Sudoku` puzzle made up 81 `Square`'s.

  `values` is an 81 character string used to initialize the puzzle.
  `squares` is the two-dimensional array (9x9) of `Square`'s representing the puzzle grid.
  """
  def __init__(self, values):
    assert len(values) == 81
    self.values = values
    self.squares = []
    for i in range(9):  # init squares
      start, end = i * 9, i * 9 + 9
      self.squares.append([Square(start + index, int(c) if c != '.' else None) \
          for index, c in enumerate(values[start:end])])
    for sq in chain(*self.squares):
      sq.candidates = self.candidates(sq)

  def solved(self):
    """
    Return true if this Sudoku puzzle is solved, false otherwise.
    """
    incomplete = lambda x: set(range(1, 10)) - set([sq.val for sq in x]) != set()
    for sq in chain(*self.squares):
      if any(map(incomplete, self.rcb(sq))):
        return False
    return True

  def candidates(self, sq):
    """
    Return the possible 'candidate' values for square `sq` in this `Sudoku` puzzle, given the
    current state of its `squares`.
    """
    if sq.val is not None:
      return []
    return list(set(range(1, 10)) - set(map(lambda x: x.val, chain(*self.rcb(sq)))))

  def rcb(self, sq):
    """
    Return a 3-tuple of the `(row, column, box)` that square `sq` belongs to.

    Useful for determining candiates for `sq` or whether this `Sudoku` is valid/solved.
    """
    row = [self.squares[sq.index // 9][x] for x in range(9)]
    col = [self.squares[x][sq.index % 9] for x in range(9)]
    box = filter(lambda x: x.box() == sq.box(), chain(*self.squares))
    return (row, col, box)

  def __repr__(self):
    return f'{self.values} solved={self.solved()}'

  def __str__(self):
    return '\n'.join([' '.join([f'{sq}' for sq in row])
        for row in self.squares])


if __name__ == '__main__':
  sudoku = Sudoku(read_values('hard.txt'))
  print(f'{sudoku}\n{repr(sudoku)}')

  solution = solve(sudoku)
  print(f'{solution}\n{repr(solution)}')
