from dragonfly import *
from dragonfly.engines.backend_sapi5.engine import Sapi5InProcEngine

from collections import defaultdict
import sys

################################################################################
# Global variables
################################################################################
engine = Sapi5InProcEngine()
engine.connect()

# Battery characteristics
batteries = 99
freak = 'freak'
car = 'car'
parallel = 'parallel'
serial = 'serial'
vowel = 'vowel'

# Maxes
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
x|x|x x|x x
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

# Wire sequence
counts = defaultdict(int) 
sequences = {}
sequences['red'] = [
    ('c'),
    ('b'),
    ('a'),
    ('a', 'c'),
    ('b'),
    ('a', 'c'),
    ('a', 'b', 'c'),
    ('a', 'b'),
    ('b')
    ]
sequences['blue'] = [
    ('b'),
    ('a', 'c'),
    ('b'),
    ('a'),
    ('b'),
    ('b','c'),
    ('c'),
    ('a', 'c'),
    ('a')
    ]
sequences['black'] = [
    ('a', 'b', 'c'),
    ('a', 'c'),
    ('b'),
    ('a', 'c'),
    ('b'),
    ('b', 'c'),
    ('a', 'b'),
    ('c'),
    ('c')
    ]

# Memory
values = []
positions = []
curr_stage = 1

# Morse
morse_letters = []

# On first words
on_first_words = []

# Password
curr_password = []

def get_maze_dict(maze):
    maze_dict = defaultdict(list)
    maze = maze[1:]
    maze = maze.split('\n')

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

def easy_answer(answer):
    count = 0
    curr_letter = answer[0]
    curr_answer = ''

    for index, letter in enumerate(answer):
        left = start[index:]
        if letter != curr_letter:
            curr_answer += curr_letter + str(count) + ' '
            curr_letter = letter
            count = 1
        else:
            count += 1

    curr_answer += curr_letter + str(count)

    return curr_answer
    

def traverse_maze(maze_dict, start, finish):
    path = [[('x', start)]]
    while True:
        for curr_path in path:
            temp_path = curr_path[:]
            new_paths = maze_dict[temp_path[-1][1]]
            for new_path in new_paths:
                if finish == new_path[1]:
                    answer = ''
                    for pair in (temp_path + [new_path])[1:]:
                        answer += pair[0]

                    return answer
                else:
                    path.append(temp_path + [new_path])

def get_maze(indicator):
    for indicators,maze in mazes.iteritems():
        if indicator in indicators:
            return maze

    return ''

def odd_serial():
    return serial in ('one', 'three', 'five', 'seven', 'nine')

def even_serial():
    return serial in ('zero', 'two', 'four', 'six', 'eight')

def sanitize_colors(words):
    print "Sanitizing: {}".format(words)
    words = words.replace('read', 'red').replace('blew', 'blue')
    words = ' '.join([word for word in words.split() if word in ('yellow', 'red', 'black', 'blue', 'white')])
    print "Sanitized: {}".format(words)
    return words

class SampleRule(CompoundRule):
    spec = "simple wires <wires>"                  # Spoken form of command.
    extras = [Dictation("wires")]
    def _process_recognition(self, node, extras):   # Callback when command is spoken.
        wire = str(extras['wires'])

class BombResetRule(CompoundRule):
    spec = "bomb reset"

    def _process_recognition(self, node, extras):   # Callback when command is spoken.
        global batteries
        global freak
        global car
        global paralle
        global serial
        global vowel
        global counts
        global values
        global positions
        global curr_stage
        global morse_letters
        global on_first_words

        # Battery characteristics
        batteries = 99
        freak = 'freak'
        car = 'car'
        parallel = 'parallel'
        serial = 'serial'
        vowel = 'vowel'

        # Wire sequence
        counts = defaultdict(int) 

        # Memory
        values = []
        positions = []
        curr_stage = 1

        # Morse
        morse_letters = []

        # On First Words
        on_first_words = []

class BombStatusRule(CompoundRule):
    spec = "bomb status"

    def _process_recognition(self, node, extras):   # Callback when command is spoken.
        global batteries
        global freak
        global car
        global paralle
        global serial
        global vowel
        global counts
        global values
        global positions
        global curr_stage
        global morse_letters
        global on_first_words

        # Battery characteristics
        print 'batteries', batteries
        print 'frk', freak
        print 'car', car
        print 'parallel', parallel
        print 'serial', serial
        print 'vowel', vowel

        # Wire sequence
        print 'wire sequence', counts

        # Memory
        print 'values', values
        print 'position', positions
        print 'curr_stage', curr_stage

        # Morse
        print 'morse_letters', morse_letters

        # On First Words
        print 'on first words', on_first_words

class BombCarRule(CompoundRule):
    spec = "car <car>"
    extras = [IntegerRef('car', 0, 10)]

    def _process_recognition(self, node, extras):   # Callback when command is spoken.
        global car
        car = str(extras['car'])

class BombBatteriesRule(CompoundRule):
    spec = "batteries <batteries>"
    extras = [IntegerRef('batteries', 0, 10)]

    def _process_recognition(self, node, extras):   # Callback when command is spoken.
        global batteries
        batteries = int(str(extras['batteries']))

class BombFreakRule(CompoundRule):
    spec = "freak <word>"
    extras = [Dictation('word')]

    def _process_recognition(self, node, extras):   # Callback when command is spoken.
        global freak
        freak = str(extras['word'])

class BombParallelRule(CompoundRule):
    spec = "parallel <word>"
    extras = [
              Dictation('word'),
              ]

    def _process_recognition(self, node, extras):   # Callback when command is spoken.
        global parallel
        parallel = str(extras['word'])

class BombSerialRule(CompoundRule):
    spec = "serial <word>"
    extras = [
              Dictation('word'),
              ]

    def _process_recognition(self, node, extras):   # Callback when command is spoken.
        global serial
        serial = str(extras['word'])

class BombVowelRule(CompoundRule):
    spec = "vowel <word>"
    extras = [
              Dictation('word')
              ]

    def _process_recognition(self, node, extras):   # Callback when command is spoken.
        global vowel
        vowel = str(extras['word'])

# Voice command rule combining spoken form and recognition processing.
class SimpleWiresRule(CompoundRule):
    spec = "simple wires <wires>"                  # Spoken form of command.
    extras = [Dictation("wires")]
    def _process_recognition(self, node, extras):   # Callback when command is spoken.
        spoken = 'need'
        if serial == 'serial':
            spoken += ' last digit of serial'
        if spoken != 'need':
            engine.speak(spoken)
            return

        wire = str(extras['wires'])
        wire = sanitize_colors(wire)
        wire = wire.split()
        
        if len(wire) == 3:
            if 'red' not in wire:
                engine.speak('cut second wire')
            elif wire[-1] == 'white':
                engine.speak('cut last wire')
            elif wire.count('blue') > 1:
                engine.speak('cut last blue wire')
            else:
                engine.speak('cut last wire')

        elif len(wire) == 4:
            if wire.count('red') > 1 and odd_serial():
                engine.speak('cut last red wire')
            elif wire[-1] == 'yellow' and wire.count('red') == 0:
                engine.speak('cut first wire')
            elif wire.count('blue') == 1:
                engine.speak('cut first wire')
            elif wire.count('yellow') > 1:
                engine.speak('cut last wire')
            else:
                engine.speak('cut second wire')

        elif len(wire) == 5:
            if wire[-1] == 'black' and odd_serial():
                engine.speak('cut fourth wire')
            elif wire.count('red') and wire.count('yellow') > 1:
                engine.speak('cut first wire')
            elif wire.count('black') == 0:
                engine.speak('cut second wire')
            else:
                engine.speak('cut first wire')

        elif len(wire) == 6:
            if wire.count('yellow') == 0 and odd_serial():
                engine.speak('cut third wire')
            elif wire.count('yellow') == 1 and wire.count('white') > 1:
                engine.speak('cut fourth wire')
            elif wire.count('red') == 0:
                engine.speak('cut last wire')
            else:
                engine.speak('cut fourth wire')

class ComplexWiresRule(CompoundRule):
    spec = "complex wires <wires>"                  # Spoken form of command.
    extras = [Dictation("wires")]


    def _process_recognition(self, node, extras):   # Callback when command is spoken.
        spoken = 'need'
        if batteries == 99:
            spoken += ' batteries'
        if parallel == 'parallel':
            spoken += ' parallel port'
        if serial == 'serial':
            spoken += ' last digit of serial'
        if spoken != 'need':
            engine.speak(spoken)
            return

        meaning = {
            int('0000', 2): 'cut',
            int('0001', 2): 'dont cut',
            int('0010', 2): 'cut',
            int('0011', 2): 'cut' if batteries > 1 else 'dont cut',
            int('0100', 2): 'cut' if serial in ('zero', 'two', 'four', 'six', 'eight') else 'dont cut',
            int('0101', 2): 'cut' if parallel in ('true', 'yes') else 'dont cut',
            int('0110', 2): 'dont cut',
            int('0111', 2): 'cut' if parallel in ('true', 'yes') else 'dont cut',
            int('1000', 2): 'cut' if serial in ('zero', 'two', 'four', 'six', 'eight') else 'dont cut',
            int('1001', 2): 'cut' if batteries > 1 else 'dont cut',
            int('1010', 2): 'cut',
            int('1011', 2): 'cut' if batteries > 1 else 'dont cut',
            int('1100', 2): 'cut' if serial in ('zero', 'two', 'four', 'six', 'eight') else 'dont cut',
            int('1101', 2): 'cut' if serial in ('zero', 'two', 'four', 'six', 'eight') else 'dont cut',
            int('1110', 2): 'cut' if parallel in ('true', 'yes') else 'dont cut',
            int('1111', 2): 'dont cut'
            }

        bad_words = [('read', 'red'), ('blew', 'blue'), ('start', 'star'),
        ('white', 'light')]
        wire = str(extras['wires'])
        print wire
        wires = [wire for wire in wire.split('next')]
        print wires
        print 'parallel', parallel
        print 'serial', serial
        print 'batteries', batteries
        final_wires = []
        answer = 'cut nothing'
        for index, wire in enumerate(wires):
            for bad, good in bad_words:
                wire = wire.replace(bad, good)

            wire = [item for item in wire.split() if item in ('red', 'blue', 'light',
            'star', 'blank')]

            print wire
            total = 0
            for letter, value in [('red', 8), ('blue', 4), ('star', 2), ('light', 1)]:
                if letter in wire:
                    total += value

            
            if answer == 'cut nothing':
                answer = 'cut '
            
            if meaning[total] == 'cut':
                answer += str(index+1) + ', '

        engine.speak(answer)
            # engine.speak(meaning[total])

class MazeRule(CompoundRule):
    spec = "maze <maze>"                  # Spoken form of command.
    extras = [Dictation("maze")]
    def _process_recognition(self, node, extras):   # Callback when command is spoken.
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
            engine.speak("Try maze again")
            return

        maze = get_maze(indicator)
        print maze
        maze_dict = get_maze_dict(maze)
        letters = {'L': 'left', 'R': 'right', 'D':'down', 'U':'up'}
        path = []
        for letter in traverse_maze(maze_dict, start, finish):
            path.append(letters[letter])

        for path in [path[x:x+3] for x in range(0, len(path), 3)]:
            engine.speak(path)

class SimonRule(CompoundRule):
    spec = "simon <words>"                  # Spoken form of command.
    extras = [Dictation("words")]
    def _process_recognition(self, node, extras):   # Callback when command is spoken.
        print str(extras['words'])
        if vowel == 'vowel':
            engine.speak("Serial contain vowel?")
            return

        words = str(extras['words'])
        print words
        words = words.replace('read', 'red').replace('blew', 'blue')
        words = [word for word in words.split() if word in ('blue', 'yellow', 'red', 'green')]

        new_words = []
        print "Your words: {}".format(words)
        if vowel in ('true', 'yes'):
            colors = {'red': 'blue', 
                      'blue': 'red',
                      'green': 'yellow', 
                      'yellow': 'green'}
            for word in words:
                new_words.append(colors[word])
        else:
            colors = {'red': 'blue', 
                      'blue': 'yellow',
                      'green': 'green', 
                      'yellow': 'red'}
            for word in words:
                new_words.append(colors[word])
        
        new_words = ' '.join(new_words)
        print "My words: {}".format(new_words)
        engine.speak(new_words)

class WireSequenceRule(CompoundRule):
    spec = "wire sequence <words>"                  # Spoken form of command.
    extras = [Dictation("words")]
    def _process_recognition(self, node, extras):   # Callback when command is spoken.
        global sequences
        words = str(extras['words'])
        print words
        words = words.replace('read', 'red').replace('blew', 'blue')
        print words
        words = [word for word in words.split() if word in ('red', 'blue', 'black', 'apple', 'bravo', 'charlie')]
        print words
        words = [words[x:x+2] for x in xrange(0, len(words), 2)]
        print words
        for color, letter in words:
            print "Color: {}".format(color)
            print "Letter: {}".format(letter)
            print "Count: {}".format(counts[color])
            if letter[0] in sequences[color][counts[color]]:
                engine.speak('Cut')
            else:
                engine.speak('Dont Cut')

            counts[color] += 1

class WireSequenceResetRule(CompoundRule):
    spec = "wire sequence reset"                  # Spoken form of command.
    def _process_recognition(self, node, extras):   # Callback when command is spoken.
        global counts
        global sequences
        counts = defaultdict(int) 
        sequences = {}

class ButtonRule(CompoundRule):
    spec = "button <words>"                  # Spoken form of command.
    extras = [Dictation("words")]
    def _process_recognition(self, node, extras):   # Callback when command is spoken.
        spoken = 'need'
        print "Batteries: {}".format(batteries)
        print "Freak: {}".format(freak)
        print "Car: {}".format(car)
        if batteries == 99:
            spoken += ' batteries'
        if freak == 'freak':
            spoken += ' freak'
        if car == 'car':
            spoken += ' car identifier'
        if spoken != 'need':
            engine.speak(spoken)
            return

        words = str(extras['words'])
        print words
        words = words.replace('read', 'red').replace('blew', 'blue')
        print words
        if 'blue' in words and 'abort' in words:
            engine.speak('Press and hold')
        elif 'detonate' in words and batteries > 1:
            engine.speak('Press and release')
        elif 'white' in words and car in ('true', 'yes'):
            engine.speak('Press and hold')
        elif batteries > 2 and freak in ('true', 'yes'):
            engine.speak('Press and release')
        elif 'yellow' in words:
            engine.speak('Press and hold')
        elif 'red' in words and 'hold' in words:
            engine.speak('Press and release')
        else:
            engine.speak('Press and hold')

class ButtonColorRule(CompoundRule):
    spec = "button color <words>"                  # Spoken form of command.
    extras = [Dictation("words")]
    def _process_recognition(self, node, extras):   # Callback when command is spoken.
        words = str(extras['words'])
        print words
        words = words.replace('read', 'red').replace('blew', 'blue')
        print words
        if 'blue' in words:
            engine.speak('four')
        elif 'yellow' in words:
            engine.speak('five')
        else:
            engine.speak('one')

class KnobsRule(CompoundRule):
    spec = "knobs <words>"                  # Spoken form of command.
    extras = [Dictation("words")]
    def _process_recognition(self, node, extras):   # Callback when command is spoken.
        words = str(extras['words'])
        print words
        words = ''.join([word for word in words.split() if word in ('one', 'zero')])
        print words
        leds = words.replace('one', '1').replace('zero', '0').replace(' ', '')
        print leds
        if leds == '111011' or leds == '011010':
            engine.speak('Up')
        if leds == '111001' or leds == '010010':
            engine.speak('Down')
        if leds == '100010' or leds == '000010':
            engine.speak('Left')
        if leds == '111111' or leds == '111100':
            engine.speak('Right')


class MemoryRule(CompoundRule):
    spec = "memory <words>"                  # Spoken form of command.
    extras = [Dictation("words")]
    def _process_recognition(self, node, extras):   # Callback when command is spoken.
        global values
        global positions
        global curr_stage
        words = str(extras['words'])
        print words
        words = [word for word in words.split() if word in ('one', 'two', 'three', 'four')]
        print words
        if len(words) != 5:
            engine.speak("Try memory again.")
            return 

        display = words[0]
        stage = words[1:]

        print "Current Stage: {}".format(curr_stage)
        print "Values: {}".format(values)
        print "Positions: {}".format(values)
        if curr_stage == 1:
            if display == 'one':
                answer = stage[1]
            if display == 'two':
                answer = stage[1]
            if display == 'three':
                answer = stage[2]
            if display == 'four':
                answer = stage[3]
            position = stage.index(answer)

        if curr_stage == 2:
            if display == 'one':
                answer = 'four'
            if display == 'two':
                answer = stage[positions[0]]
            if display == 'three':
                answer = stage[0]
            if display == 'four':
                answer = stage[positions[0]]
            position = stage.index(answer)

        if curr_stage == 3:
            if display == 'one':
                answer = values[1]
                position = 'one'
            if display == 'two':
                answer = values[0]
                position = 'two'
            if display == 'three':
                answer = stage[2]
                position = stage.index(answer)
            if display == 'four':
                answer = 'four'
                position = stage.index(answer)

        if curr_stage == 4:
            if display == 'one':
                answer = stage[positions[0]]
                position = stage.index(answer)
            if display == 'two':
                answer = stage[0]
                position = stage.index(answer)
            if display == 'three':
                answer = stage[positions[1]]
                position = stage.index(answer)
            if display == 'four':
                answer = stage[positions[1]]
                position = stage.index(answer)

        if curr_stage == 5:
            if display == 'one':
                answer = values[0]
            if display == 'two':
                answer = values[1]
            if display == 'three':
                answer = values[3]
            if display == 'four':
                answer = values[2]
            position = stage.index(answer)

        values.append(answer)
        positions.append(position)
        curr_stage += 1
        print "Answer: {}".format(answer)
        engine.speak(answer)
        if curr_stage > 5:
            values = []
            positions = []
            curr_stage = 1


class MemoryResetRule(CompoundRule):
    spec = "memory reset"                  # Spoken form of command.
    def _process_recognition(self, node, extras):   # Callback when command is spoken.
        global positions
        global curr_stage
        global values
        positions = []
        values = []
        curr_stage = 1

class MorseRule(CompoundRule):
    spec = "morse <words>"                  # Spoken form of command.
    extras = [Dictation("words")]
    def _process_recognition(self, node, extras):   # Callback when command is spoken.
        global morse_letters
        words = str(extras['words'])

        words = ''.join([word for word in words.split() if word in ('one', 'zero')])
        print words
        code = words.replace('one', '-').replace('zero', '.')
        print code

        morse = {
            'a': '.-',
            'b': '-...',
            'c': '-.-.',
            'e': '.',
            'f': '..-.',
            'g': '--.',
            'h': '....',
            'i': '..', 
            'k': '-.-',
            'l': '.-..',
            'm': '--',
            'n': '-.',
            'o': '---',
            'r': '.-.',
            's': '...',
            't': '-',
            'v': '...-',
            'x': '-..-',
        }

        codes = {}
        for key, val in morse.iteritems():
            if code == val:
                morse_letters.append(key)

            codes[val] = key

        print "Current morse letters: {}".format(morse_letters)
        if len(morse_letters) < 2:
            return

        words = {
            'shell': '5 0 5',
            'halls': '5 1 5',
            'slick': '5 2 2',
            'trick': '5 3 2',
            'boxes': '5 3 5',
            'leaks': '5 4 2',
            'strobe': '5 4 5',
            'bistro': '5 5 2',
            'flick': '5 5 5',
            'bombs': '5 6 5',
            'break': '5 7 2',
            'brick': '5 7 5',
            'steak': '5 8 2',
            'sting': '5 9 2',
            'vector': '5 9 5',
            'beats': '6 0 0',
        }

        code = ''.join(morse_letters)

        combos = {}
        for word in words:
            curr_combo = []
            for num in xrange(len(word)):
                curr_word = ''.join((word+word)[num:num+3])
                combos[curr_word] = word

        print code
        print combos.keys()
        if code in combos:
            engine.speak(words[combos[code]])

        possibles = []
        for key, val in combos.iteritems():
            curr_word = ''.join([morse[letter] for letter in key])
            if code.startswith(curr_word):
                # print val, key, code, words[val]
                print words[val]

class MorseResetRule(CompoundRule):
    spec = "morse reset"                  # Spoken form of command.
    def _process_recognition(self, node, extras):   # Callback when command is spoken.
        global morse_letters
        morse_letters = []

class WordsResetRule(CompoundRule):
    spec = "words reset"                  # Spoken form of command.
    def _process_recognition(self, node, extras):   # Callback when command is spoken.
        global on_first_words
        on_first_words = []

class WordsRemoveRule(CompoundRule):
    spec = "words remove"                  # Spoken form of command.
    def _process_recognition(self, node, extras):   # Callback when command is spoken.
        global on_first_words
        on_first_words = on_first_words[:-1]

class SymbolsRule(CompoundRule):
    spec = "symbols <symbols>"                  # Spoken form of command.
    extras = [Dictation("symbols")]
    def _process_recognition(self, node, extras):   # Callback when command is spoken.
        symbols = str(extras['symbols'])

        groups = [
            ['tennis', 'a', 'l', 'lightning', 'kitty', 'h', 'c'],
            ['e', 'tennis', 'c', 'o', 'star', 'h', 'question'],
            ['copyright', 'but', 'o', 'k', 'r', 'l', 'star'],
            ['six', 'paragraph', 'b', 'kitty', 'k', 'question', 'smile'],
            ['goblet', 'smile', 'b', 'c', 'paragraph', 'three', 'star'],
            ['six', 'e', 'equals', 'smash', 'goblet', 'in', 'omega']
        ]

        print symbols
        curr_symbols = symbols.replace('.', '').lower().split()
        print curr_symbols

        answer = ''
        for group in groups:
            for symbol in curr_symbols:
                if symbol not in group:
                    break
            else:
                for symbol in group:
                    if symbol in curr_symbols:
                        answer += symbol + ' '

        engine.speak(answer)

class WordsRule(CompoundRule):
    spec = "words <words>"                  # Spoken form of command.
    extras = [Dictation("words")]
    def _process_recognition(self, node, extras):   # Callback when command is spoken.
        words = str(extras['words'])

        combos = {
            ('you', 'are', 'words'): 'you are',
            ('your', 'words'): 'you are',
            ('done',): 'done',
            ('don',): 'done',
            ('you', 'are', 'letters'): 'ur',
            ('sure',): 'sure',
            ('shore',): 'sure',
            ('you', 'word'): 'you',
            ('hold',): 'hold',
            ('you', 'letter'): 'u',
            ('yes',): 'yes',
            ('first',): 'first',
            ('display',): 'display',
            ('okay',): 'okay',
            ('OK',): 'okay',
            ('says',): 'says',
            ('nothing',): 'nothing',
            ('literally', 'blank'): ' ',
            ('blank',): 'blank',
            ('no',): 'no',
            ('L.', 'E.', 'D.'): 'led',
            ('lead',): 'lead',
            ('mead',): 'lead',
            ('read',): 'read',
            ('red', 'short'): 'red',
            ('read', 'too'): 'reed',
            ('hold', 'on', 'two'): 'hold on',
            ("you're", 'word'): 'your',
            ("your", 'word'): 'your',
            ('your', 'mark'): "you're",
            ('you', 'are', 'marked'): "you're",
            ('you', 'are', 'mark'): "you're",
            ('C.', 'S.'): "see",
            ('they', 'are', 'words'): "they are",
            ('E.', 'I.', 'R.'): "their",
            ('E.', 'R.', 'E.'): "there",
            ('they', 'are', 'marked'): "they're",
            ('they', 'mark'): "they're",
            ('CS'): "see",
            ('C.', 'letter'): "c",
            ('see', 'letter'): "c",
            ('C.', 'C.'): "cee",
            ('CC',): "cee",
            ('ready',): 'ready',
            ('yes',): 'yes',
            ('what', 'no', 'mark'): 'what',
            ('three', 'H.'): 'uhhh',
            ('left',): 'left',
            ('right',): 'right',
            ('write',): 'right',
            ('middle',): 'middle',
            ('metal',): 'middle',
            ('wait',): 'wait',
            ('press',): 'press',
            ('five', 'letters'): 'uh huh',
            ('four', 'letters'): 'uh uh',
            ('what', 'mark'): 'what?',
            ('done',): 'done',
            ('next',): 'next',
            ('hold',): 'hold',
            ('sure',): 'sure',
            ('like',): 'like',
            ('mike',): 'like',
            ('might',): 'like',
            ('white',): 'like',
            ('light',): 'like',
        }

        positions = {
            'yes': 3,
            'first': 2,
            'display': 6,
            'okay': 2,
            'says': 6,
            'nothing': 3,
            ' ': 5,
            'blank': 4,
            'no': 6,
            'led': 3,
            'lead': 6,
            'read': 4,
            'red': 4,
            'reed': 5,
            'leed': 5,
            'hold on': 6,
            'you': 4,
            'you are': 6,
            'your': 4,
            "you're": 4,
            'ur': 1,
            'there': 6,
            "they're": 5,
            'their': 4,
            'they are': 3,
            'see': 6,
            'c': 2,
            'cee': 6
        }

        table = {
            "ready": ["yes", "okay", "what", "middle", "left", "press", "right", "blank", "ready", "no", "first", "uhhh", "nothing", "wait"],
            "first": ["left", "okay", "yes", "middle", "no", "right", "nothing", "uhhh", "wait", "ready", "blank", "what", "press", "first"], 
            "no": ["blank", "uhhh", "wait", "first", "what", "ready", "right", "yes", "nothing", "left", "press", "okay", "no", "middle"], 
            "blank": ["wait", "right", "okay", "middle", "blank", "press", "ready", "nothing", "no", "what", "left", "uhhh", "yes", "first"],
            "nothing": ["uhhh", "right", "okay", "middle", "yes", "blank", "no", "press", "left", "what", "wait", "first", "nothing", "ready"], 
            "yes": ["okay", "right", "uhhh", "middle", "first", "what", "press", "ready", "nothing", "yes", "left", "blank", "no", "wait"], 
            "what": ["uhhh", "what", "left", "nothing", "ready", "blank", "middle", "no", "okay", "first", "wait", "yes", "press", "right"],
            "uhhh": ["ready", "nothing", "left", "what", "okay", "yes", "right", "no", "press", "blank", "uhhh", "middle", "wait", "first"], 
            "left": ["right", "left"],
            "right": ["yes", "nothing", "ready", "press", "no", "wait", "what", "right"],
            "middle": ["blank", "ready", "okay", "what", "nothing", "press", "no", "wait", "left", "middle"],
            "okay": ["middle", "no", "first", "yes", "uhhh", "nothing", "wait", "okay"],
            "wait": ["uhhh", "no", "blank", "okay", "yes", "left", "first", "press", "what", "wait"],
            "press": ["right", "middle", "yes", "ready", "press"],
            "you": ["sure", "you are", "your", "you're", "next", "uh huh", "ur", "hold", "what?", "you"],
            "you are": ["your", "next", "like", "uh huh", "what?", "done", "uh uh", "hold", "you ", "u", "you're", "sure", "ur", "you are"],
            "your": ["uh uh", "you are", "uh huh", "your"],
            "you're": ["you", "you're"],
            "ur": ["done", "u", "ur"],
            "u": ["uh huh", "sure", "next", "what?", "you're", "ur", "uh uh", "done", "u"],
            "uh huh": ["uh huh"],
            "uh uh": ["ur", "u", "you are", "you", "done", "hold", "uh uh", "next", "sure", "like", "your", "sure", "hold", "what?"],
            "what?": ["you", "hold", "you're", "your", "u", "done", "uh uh", "like", "you are", "uh huh", "ur", "next", "what?"],
            "done": ["sure", "uh huh", "next", "what?", "your", "ur", "you're", "hold", "like", "you", "u", "you are", "uh uh", "done"],
            "next": ["what?", "uh huh", "uh uh", "your", "hold", "sure", "next"],
            "hold": ["you are", "u", "done", "uh uh", "you", "ur", "sure", "what?", "you're", "next", "hold"],
            "sure": ["you are", "done", "like", "you're", "you", "hold", "uh huh", "ur", "sure"],
            "like": ["you're", "next", "u", "ur", "hold", "uh uh", "what?", "uh huh", "you", "like"],
        }

        responses = {
            "you are": ("you" "are", "words"),
            "done": ("done",),
            "ur": ("you", "are", "letters"),
            "sure": ("sure",),
            "you": ("you", "word"),
            "hold": ("hold",),
            "u": ("you", "letter"),
            "yes": ("yes",),
            "first": ("first",),
            "display": ("display",),
            "okay": ("okay",),
            "okay": ("OK",),
            "says": ("says",),
            "nothing": ("nothing",),
            " ": ("literally", "blank"),
            "blank": ("blank",),
            "no": ("no",),
            "led": ("L.", "E.", "D."),
            "lead": ("lead",),
            "lead": ("mead",),
            "read": ("read",),
            "red": ("red", "short"),
            "reed": ("read", "too"),
            "hold on": ("hold", "on", "two"),
            "your": ("you"re", "word"),
            "your": ("your", "word"),
            "you're": ("you", "are", "mark"),
            "see": ("C.", "S."),
            "they are": ("they", "are", "words"),
            "their": ("E.", "I.", "R."),
            "there": ("E.", "R.", "E."),
            "they're": ("they", "are", "marked"),
            "see": ("s e e"),
            "c": ("see", "letter"),
            "cee": ("C.", "C."),
            "cee": ("CC",),
            "ready": ("ready",),
            "yes": ("yes",),
            "what": ("what", "no", "mark"),
            "uhhh": ("three", "H."),
            "left": ("left",),
            "right": ("right",),
            "right": ("write",),
            "middle": ("middle",),
            "wait": ("wait",),
            "press": ("press",),
            "uh huh": ("five", "letters"),
            "uh uh": ("four", "letters"),
            "what?": ("what", "mark"),
            "done": ("done",),
            "next": ("next",),
            "hold": ("hold",),
            "sure": ("sure",),
            "like": ("like",),
        }
        print words

        for combo, select in sorted(combos.iteritems(), key=lambda x: len(x[0])):
            for word in combo:
                print word, words.split()
                if word not in words.split():
                    break
            else:
                print 'Words', words
                print "Found word: {}".format(select)
                if 'one' in words:
                    engine.speak(positions[select])

                if 'two' in words:
                    wordlist = table[select]
                    answer = []
                    for word in wordlist[:5]:
                        answer.append(responses[word])

                    engine.speak(', '.join(answer))
                break

class PasswordRule(CompoundRule):
    spec = "password reset"                  # Spoken form of command.
    def _process_recognition(self, node, extras):   # Callback when command is spoken.
        global curr_password
        curr_password = []

class PasswordRule(CompoundRule):
    spec = "password <letters>"                  # Spoken form of command.
    extras = [Dictation("letters")]
    def _process_recognition(self, node, extras):   # Callback when command is spoken.
        global curr_password
        letters = str(extras['letters'])
        letters = [letter[0].lower() for letter in letters.split()]
        curr_password.append(letters)
        print curr_password

        passwords = ['about',
        'after', 'again', 'below', 'could', 'every', 'first', 'found', 'great',
        'house', 'large', 'learn', 'never', 'other', 'place', 'plant', 'point',
        'right', 'small', 'sound', 'spell', 'still', 'study', 'their', 'there',
        'these', 'thing', 'think', 'three', 'water', 'where', 'which', 'world',
        'would', 'write']

        possibles = []
        if len(curr_password) == 2:
            for password in passwords:
                if password[0] in curr_password[0] and password[2] in curr_password[1]:
                    possibles.append(password)

            print possibles

        for word in possibles:
            engine.speak(word)

class BombDoneRule(CompoundRule):
    spec = "bomb done"                  # Spoken form of command.
    def _process_recognition(self, node, extras):   # Callback when command is spoken.
        engine.speak("I AM YOUR BOMB DEFUSING OVERLORD")

        global batteries
        global freak
        global car
        global paralle
        global serial
        global vowel
        global counts
        global values
        global positions
        global curr_stage
        global morse_letters
        global on_first_words

        # Battery characteristics
        batteries = 99
        freak = 'freak'
        car = 'car'
        parallel = 'parallel'
        serial = 'serial'
        vowel = 'vowel'

        # Wire sequence
        counts = defaultdict(int) 

        # Memory
        values = []
        positions = []
        curr_stage = 1

        # Morse
        morse_letters = []

        # On First Words
        on_first_words = []

# Create a grammar which contains and loads the command rule.
grammar = Grammar("Keep Talking")                # Create a grammar to contain the command rule.
grammar.add_rule(BombBatteriesRule())                     # Add the command rule to the grammar.
grammar.add_rule(BombVowelRule())                     # Add the command rule to the grammar.
grammar.add_rule(BombParallelRule())                     # Add the command rule to the grammar.
grammar.add_rule(BombSerialRule())                     # Add the command rule to the grammar.
grammar.add_rule(BombFreakRule())                     # Add the command rule to the grammar.
grammar.add_rule(BombCarRule())                     # Add the command rule to the grammar.
grammar.add_rule(BombResetRule())                     # Add the command rule to the grammar.
grammar.add_rule(BombStatusRule())                     # Add the command rule to the grammar.
grammar.add_rule(SimpleWiresRule())                     # Add the command rule to the grammar.
grammar.add_rule(ComplexWiresRule())                     # Add the command rule to the grammar.
grammar.add_rule(MazeRule())                     # Add the command rule to the grammar.
grammar.add_rule(SimonRule())                     # Add the command rule to the grammar.
grammar.add_rule(WireSequenceRule())                     # Add the command rule to the grammar.
grammar.add_rule(WireSequenceResetRule())                     # Add the command rule to the grammar.
grammar.add_rule(ButtonRule())                     # Add the command rule to the grammar.
grammar.add_rule(ButtonColorRule())                     # Add the command rule to the grammar.
grammar.add_rule(KnobsRule())                     # Add the command rule to the grammar.
grammar.add_rule(MemoryRule())                     # Add the command rule to the grammar.
grammar.add_rule(MemoryResetRule())                     # Add the command rule to the grammar.
grammar.add_rule(MorseRule())                     # Add the command rule to the grammar.
grammar.add_rule(MorseResetRule())                     # Add the command rule to the grammar.
grammar.add_rule(SymbolsRule())                     # Add the command rule to the grammar.
grammar.add_rule(WordsRule())                     # Add the command rule to the grammar.
grammar.add_rule(WordsResetRule())                     # Add the command rule to the grammar.
grammar.add_rule(WordsRemoveRule())                     # Add the command rule to the grammar.
grammar.add_rule(PasswordRule())                     # Add the command rule to the grammar.
grammar.add_rule(BombDoneRule())
grammar.load()
