from dragonfly import *
from dragonfly.engines.backend_sapi5.engine import Sapi5InProcEngine

from collections import defaultdict
import sys
import random

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


# On first words
on_first_words = []
curr_wordlist = []

# Password
curr_password = []


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


def odd_serial():
    return serial in (1, 3, 5, 7, 9)

def even_serial():
    return serial in (0, 2, 4, 6, 8)

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

        # Password
        curr_password = []

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
              IntegerRef('word', 0, 10),
              ]

    def _process_recognition(self, node, extras):   # Callback when command is spoken.
        global serial
        serial = str(extras['word'])

class BombVowelRule(CompoundRule):
    spec = "contains vowel <word>"
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
        from bombly.modules.wires import wires
        engine.speak(wires(extras, sanitize_colors, odd_serial))

class ComplexWiresRule(CompoundRule):
    spec = "complex wires <wires>"                  # Spoken form of command.
    extras = [Dictation("wires")]

    def _process_recognition(self, node, extras):   # Callback when command is spoken.
        from bombly.modules.complicated_wires import complicated_wires
        engine.speak(complicated_wires(extras, batteries, serial, parallel))


class MazeRule(CompoundRule):
    spec = "maze <maze>"                  # Spoken form of command.
    extras = [Dictation("maze")]
    def _process_recognition(self, node, extras):   # Callback when command is spoken.
        from bombly.modules.mazes import solve_maze
        answer = solve_maze(extras)
        for item in answer:
            engine.speak(item)

class SimonRule(CompoundRule):
    spec = "simon <words>"                  # Spoken form of command.
    extras = [Dictation("words")]
    def _process_recognition(self, node, extras):   # Callback when command is spoken.
        from bombly.modules.simon_says import simon
        engine.speak(simon(extras, vowel))

class WireSequenceRule(CompoundRule):
    spec = "wire sequence <words>"                  # Spoken form of command.
    extras = [Dictation("words")]
    def _process_recognition(self, node, extras):   # Callback when command is spoken.
        from bombly.modules.wire_sequences import wire_sequence
        engine.speak(wire_sequence(extras))

class WireSequenceResetRule(CompoundRule):
    spec = "wire sequence reset"                  # Spoken form of command.
    def _process_recognition(self, node, extras):   # Callback when command is spoken.
        from bombly.modules.wire_sequences import reset
        reset()

class ButtonRule(CompoundRule):
    spec = "button <words>"                  # Spoken form of command.
    extras = [Dictation("words")]
    def _process_recognition(self, node, extras):   # Callback when command is spoken.
        from bombly.modules.the_button import button
        engine.speak(button(extras, batteries, car, freak))

class ButtonColorRule(CompoundRule):
    spec = "button color <words>"                  # Spoken form of command.
    extras = [Dictation("words")]
    def _process_recognition(self, node, extras):   # Callback when command is spoken.
        from bombly.modules.the_button import button_color
        engine.speak(button_color(extras))

class KnobsRule(CompoundRule):
    spec = "knobs <words>"                  # Spoken form of command.
    extras = [Dictation("words")]
    def _process_recognition(self, node, extras):   # Callback when command is spoken.
        from bombly.modules.needy.knob import knob
        engine.speak(knob(extras))


class MemoryRule(CompoundRule):
    spec = "memory <words>"                  # Spoken form of command.
    extras = [Dictation("words")]
    def _process_recognition(self, node, extras):   # Callback when command is spoken.
        from bombly.modules.memory import memory
        engine.speak(memory(extras))


class MemoryResetRule(CompoundRule):
    spec = "memory reset"                  # Spoken form of command.
    def _process_recognition(self, node, extras):   # Callback when command is spoken.
        from bombly.modules.memory import reset
        reset()

class MorseRule(CompoundRule):
    spec = "morse <words>"                  # Spoken form of command.
    extras = [Dictation("words")]
    def _process_recognition(self, node, extras):   # Callback when command is spoken.
        from bombly.modules.morse_code import morse_code
        engine.speak(morse_code(extras))
        

class MorseResetRule(CompoundRule):
    spec = "morse reset"                  # Spoken form of command.
    def _process_recognition(self, node, extras):   # Callback when command is spoken.
        from bombly.modules.morse_code import reset
        reset()


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
            ['tennis', 'apple', 'a', 'l', 'lightning', 'spider', 'h', 'house', 'c', 'charlie'],
            ['e', 'echo', 'tennis', 'c', 'charlie', 'o', 'oscar', 'starr', 'star', 'h', 'house', 'question'],
            ['copyright', 'but', 'butt', 'o', 'oscar', 'k', 'r', 'romeo', 'l', 'starr', 'star'],
            ['six', 'paragraph', 'b', 'bravo', 'spider', 'k', 'question', 'smile'],
            ['goblet', 'smile', 'b', 'bravo', 'c', 'charlie', 'paragraph', 'three', 'star'],
            ['six', 'e', 'echo', 'equals', 'smash', 'goblet', 'in', 'omega']
        ]

        print symbols
        symbols = symbols.replace('butt', 'but')
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
        global curr_wordlist
        words = str(extras['words'])

        combos = {
            ('you', 'are', 'words'): 'you are',
            ('your', 'words'): 'you are',
            ('done',): 'done',
            ('don',): 'done',
            ('you', 'are', 'letters'): 'ur',
            ('uniform', 'romeo'): 'ur',
            ('sure',): 'sure',
            ('shore',): 'sure',
            ('you', 'word'): 'you',
            ('you', 'were'): 'you',
            ('you', 'were', 'to'): 'you',
            ('you', 'work'): 'you',
            ('hold',): 'hold',
            ('you', 'letter'): 'u',
            ('uniform'): 'u',
            ('yes',): 'yes',
            ('first',): 'first',
            ('display',): 'display',
            ('okay',): 'okay',
            ('OK',): 'okay',
            ('says',): 'says',
            ('nothing',): 'nothing',
            ('literally', 'blank'): ' ',
            ('literally', 'nothing'): ' ',
            ('blank',): 'blank',
            ('no',): 'no',
            ('L. E. D.'): 'led',
            ('lead',): 'lead',
            ('mead',): 'lead',
            ('read',): 'read',
            ('red', 'short'): 'red',
            ('read', 'too'): 'reed',
            ('hold', 'on', 'two'): 'hold on',
            ("you're", 'word'): 'your',
            ("your", 'word'): 'your',
            ('your', 'mark'): "you're",
            ('your', 'contraction'): "you're",
            ('your', 'apostrophe'): "you're",
            ('you', 'are', 'marked'): "you're",
            ('you', 'are', 'mark'): "you're",
            ('you', 'are', 'contraction'): "you're",
            ('you', 'are', 'apostrophe'): "you're",
            ("Sierra", "echo", "echo"): "see",
            ('they', 'are', 'words'): "they are",
            ("echo", "india", "romeo"): "their",
            ("echo", "romeo", "echo"): "there",
            ('they', 'are', 'marked'): "they're",
            ('they', 'are', 'contraction'): "they're",
            ('they', 'are', 'apostrophe'): "they're",
            ('they', 'mark'): "they're",
            ('their', 'mark'): "they're",
            ('there', 'mark'): "they're",
            ('Sierra', 'echo', 'echo'): "see",
            ('charlie',): "c",
            ('see', 'letter'): "c",
            ('charlie', 'echo', 'echo'): "cee",
            ('ready',): 'ready',
            ('yes',): 'yes',
            ('what', 'no', 'mark'): 'what',
            ('what', 'know', 'mark'): 'what',
            ('three', 'H.'): 'uhhh',
            ('left',): 'left',
            ('right',): 'right',
            ('write',): 'right',
            ('middle',): 'middle',
            ('metal',): 'middle',
            ('wait',): 'wait',
            ('press',): 'press',
            ('five', 'letters'): 'uh huh',
            ('hotel', 'uniform', 'hotel'): 'uh huh',
            ('four', 'letters'): 'uh uh',
            ('uniform', 'hotel'): 'uh uh',
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
            "ready": ["yes", "okay", "what", "middle", "left", "press", "right", "blank", "ready"],
            "first": ["left", "okay", "yes", "middle", "no", "right", "nothing", "uhhh", "wait", "ready", "blank", "what", "press", "first"], 
            "no": ["blank", "uhhh", "wait", "first", "what", "ready", "right", "yes", "nothing", "left", "press", "okay", "no", "middle"], 
            "blank": ["wait", "right", "okay", "middle", "blank"],
            "nothing": ["uhhh", "right", "okay", "middle", "yes", "blank", "no", "press", "left", "what", "wait", "first", "nothing", "ready"], 
            "yes": ["okay", "right", "uhhh", "middle", "first", "what", "press", "ready", "nothing", "yes"], 
            "what": ["uhhh", "what"],
            "uhhh": ["ready", "nothing", "left", "what", "okay", "yes", "right", "no", "press", "blank", "uhhh"], 
            "left": ["right", "left"],
            "right": ["yes", "nothing", "ready", "press", "no", "wait", "what", "right"],
            "middle": ["blank", "ready", "okay", "what", "nothing", "press", "no", "wait", "left", "middle"],
            "okay": ["middle", "no", "first", "yes", "uhhh", "nothing", "wait", "okay"],
            "wait": ["uhhh", "no", "blank", "okay", "yes", "left", "first", "press", "what", "wait"],
            "press": ["right", "middle", "yes", "ready", "press"],
            "you": ["sure", "you are", "your", "you're", "next", "uh huh", "ur", "hold", "what?", "you"],
            "you are": ["your", "next", "like", "uh huh", "what?", "done", "uh uh", "hold", "you", "u", "you're", "sure", "ur", "you are"],
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
            "says": ("says",),
            "nothing": ("nothing",),
            " ": ("literally", "blank"),
            "blank": ("blank",),
            "no": ("no",),
            "led": ("L.", "E.", "D."),
            "lead": ("lead",),
            "read": ("read",),
            "red": ("red", "short"),
            "reed": ("read", "too"),
            "hold on": ("hold", "on", "two"),
            "your": ("your", "word"),
            "you're": ("you", "are", "mark"),
            "see": ("Sierra", "echo", "echo"),
            "they are": ("they", "are", "words"),
            "their": ("E.", "I.", "R."),
            "there": ("E.", "R.", "E."),
            "they're": ("they", "are", "marked"),
            "c": ("charlie"),
            "cee": ("charlie", "echo", "echo"),
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
            "what?": ("what", "question"),
            "done": ("done",),
            "next": ("next",),
            "hold": ("hold",),
            "sure": ("sure",),
            "like": ("like",),
        }
        print "Voice receive: ", words

        for combo, select in reversed(sorted(combos.iteritems(), key=lambda x: len(x[0]))):
            for word in combo:
                if word not in words.split():
                    break
            else:
                print 'Words', words
                print "Found word: {}".format(select)
                if 'one' in words.split():
                    curr_wordlist = []
                    engine.speak(positions[select])

                if 'two' in words.split():
                    print 'select', select
                    wordlist = table[select]
                    answer = []
                    new_length = min(4, len(wordlist))
                    curr_wordlist = []
                    print wordlist

                    # Cache next set of words in case we need to ask for more
                    # words
                    for word in wordlist[new_length:]:
                        print 'word:', word
                        curr_wordlist.append(' '.join(responses[word]))

                    for word in wordlist[:new_length]:
                        answer.append(' '.join(responses[word]))

                    engine.speak(', '.join(answer))
                break

class WordsMoreRule(CompoundRule):
    spec = "words more"                  # Spoken form of command.
    def _process_recognition(self, node, extras):   # Callback when command is spoken.
        global curr_wordlist
        speak = ', '.join(curr_wordlist[:4])
        new_length = min(4, len(curr_wordlist))
        curr_wordlist = curr_wordlist[new_length:]
        engine.speak(speak)
    
class PasswordResetRule(CompoundRule):
    spec = "password reset"                  # Spoken form of command.
    def _process_recognition(self, node, extras):   # Callback when command is spoken.
        global curr_password
        curr_password = []
        print curr_password

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
        lines = [
            "I AM YOUR BOMB DEFUSING OVERLORD",
            "BOOM SHAKALAKA",
        ]
        line = random.sample(lines, 1)
        engine.speak(line)

        global batteries
        global freak
        global car
        global parallel
        global serial
        global vowel
        global counts
        global values
        global positions
        global curr_stage
        global morse_letters
        global on_first_words
        global curr_wordlist

        # Battery characteristics
        batteries = 99
        freak = 'freak'
        car = 'car'
        parallel = 'parallel'
        serial = 'serial'
        vowel = 'false'

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

        # Who's on First
        curr_wordlist = []

class BombDoneRule(CompoundRule):
    spec = "bomb exploded"                  # Spoken form of command.
    def _process_recognition(self, node, extras):   # Callback when command is spoken.
        lines = [
            "YOU STUPID FUCK",
            "NOT MY FAULT!",
            "PLANNED..",
            "CRAP, BOMB EXPLODED",
            "HOW CAN YOU TELL ME THAT?",
            "IT'S ALL YOUR FAULT",
        ]
        line = random.sample(lines, 1)
        engine.speak(line)

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
grammar.add_rule(WordsMoreRule())                     # Add the command rule to the grammar.
grammar.add_rule(PasswordResetRule())                     # Add the command rule to the grammar.
grammar.add_rule(PasswordRule())                     # Add the command rule to the grammar.
grammar.add_rule(BombDoneRule())
grammar.load()
