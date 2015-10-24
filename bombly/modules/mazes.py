from collections import defaultdict
from Queue import Queue

mazes = {
(('1','2'), ('6','3')): """
x x x|x x x
  -     - -
x|x x|x x x
    - - -
x|x x|x x x
  -     -
x|x x x|x x
  - - - -
x x x|x x|x
  -     -
x x|x x|x x
""",
(('5','2'), ('2','4')): """
x x x|x x x
-   -     -
x x|x x|x x
  -   - -
x|x x|x x x
    -   -
x x|x x|x|x
  -   -
x|x|x|x x|x
        -
x|x x|x x x
""",
(('4','4'), ('6','4')): """
x x x|x|x x
  -
x|x|x|x x|x
-     - -
x x|x|x x|x

x|x|x|x|x|x

x|x x|x|x|x
  - -
x x x x|x x
""",
(('1','1'), ('1','4')): """
x x|x x x x
    - - -
x|x|x x x x
      - -
x|x x|x x|x
  - -   -
x|x x x x x
  - - - -
x x x x x|x
  - - -
x x x|x x|x
""",
(('5','3'), ('4','6')): """
x x x x x x
- - - -
x x x x x|x
  - -   - -
x x|x x|x x
    - -
x|x x x|x|x
  - -   -
x|x x x x|x
    - - -
x|x x x x x
""",
(('5','1'), ('3','5')): """
x|x x|x x x
      -
x|x|x|x x|x
        -
x x|x|x|x x
  - -     -
x x|x x|x|x
-
x x|x|x|x x
  - -   -
x x x x|x x
""",
(('2','1'), ('2','6')): """
x x x x|x x
  - -
x|x x|x x|x
    - - -
x x|x x|x x
- -   -   -
x x|x x x|x
      - -
x|x|x x x|x
  - - -
x x x x x x
""",
(('4','1'), ('3','4')): """
x|x x x|x x
    -
x x x|x x|x
  - - - -
x|x x x x|x
    - -
x|x x|x x x
  -   - - -
x|x|x x x x
    - - - -
x x x x x x
""",
(('3','2'), ('1','5')): """
x|x x x x x
    - -
x|x|x x|x|x
      -
x x x|x x|x
  - -   -
x|x|x x|x x
      - -
x|x|x|x x|x
          -
x x|x x|x x
""",
}


def get_maze_dict(maze):
    maze_dict = defaultdict(list)
    maze = maze[1:]
    maze = maze.split('\n')

    # Ensure all lines have enough spacing to fill the maze
    maze = [row.ljust(12, ' ') for row in maze]

    for row_index, line in enumerate(maze):
        for col_index, item in enumerate(line):
            if item == 'x':
                col = col_index/2+1
                row = row_index/2+1
                try:
                    if maze[row_index+1][col_index] == ' ':
                        maze_dict[(col, row)].append(('D', (col, row+1)))
                except:
                    pass
                try:
                    if maze[row_index-1][col_index] == ' ':
                        maze_dict[(col, row)].append(('U', (col, row-1)))
                except:
                    pass
                try:
                    if maze[row_index][col_index+1] == ' ':
                        maze_dict[(col, row)].append(('R', (col+1, row)))
                except:
                    pass
                try:
                    if maze[row_index][col_index-1] == ' ':
                        maze_dict[(col, row)].append(('L', (col-1, row)))
                except:
                    pass

    return maze_dict


def traverse_maze(maze_dict, start, finish):
    path = Queue()
    path.put([('x', start)])
    loop = {'D': 'U', 'U': 'D', 'L':'R', 'R':'L', 'x':''}
    while not path.empty():
        curr_path = path.get()
        temp_path = curr_path[:]
        new_paths = maze_dict[temp_path[-1][1]]
        # Check that we are not looping back and forth
        new_paths = [place for place in new_paths if place[0] != loop[curr_path[-1][0]]]
        for new_path in new_paths:
            if finish == new_path[1]:
                answer = ''
                for pair in (temp_path + [new_path])[1:]:
                    answer += pair[0]

                return answer
            else:
                path.put(temp_path + [new_path])
    return None


def get_maze(indicator):
    for indicators, maze in mazes.iteritems():
        if indicator in indicators:
            return maze

    return ''


def solve_maze(extras):
    maze = str(extras['maze'])
    maze = ' '.join([x for x in maze.split() if x in ['one', 'two','three', 'four', 'five', 'six', 'seven', 'eight', 'nine']])
    print maze
    for word, num in [('one', '1'), ('two', '2'), ('three', '3'), ('four', '4'), ('five', '5'), ('six', '6'), ('seven', '7'), ('eight', '8'), ('nine', '9')]:
        maze = maze.replace(word, num)

    maze = maze.replace(' ', '')
    # If users input , or spaces, we ignore them
    indicator = tuple(maze[0:2])
    start = tuple([int(x) for x in maze[2:4]])
    finish = tuple([int(x) for x in maze[4:6]])

    if len(indicator) != 2 or len(start) != 2 or len(finish) != 2:
        return ['Try Maze Again',]

    maze = get_maze(indicator)
    print maze
    maze_dict = get_maze_dict(maze)
    letters = {'L': 'left', 'R': 'right', 'D':'down', 'U':'up'}
    path = []
    for letter in traverse_maze(maze_dict, start, finish):
        path.append(letters[letter])

    answer = []
    for path in [path[x:x+3] for x in range(0, len(path), 3)]:
        answer.append(path)

    return answer
