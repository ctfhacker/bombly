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
        from bombly.modules.whos_on_first import reset
        reset()


class WordsRemoveRule(CompoundRule):
    spec = "words remove"                  # Spoken form of command.
    def _process_recognition(self, node, extras):   # Callback when command is spoken.
        from bombly.modules.whos_on_first import remove
        remove()


class SymbolsRule(CompoundRule):
    spec = "symbols <symbols>"                  # Spoken form of command.
    extras = [Dictation("symbols")]
    def _process_recognition(self, node, extras):   # Callback when command is spoken.
        from bombly.modules.keypads import keypad
        engine.speak(keypad(extras))


class WordsRule(CompoundRule):
    spec = "words <words>"                  # Spoken form of command.
    extras = [Dictation("words")]
    def _process_recognition(self, node, extras):   # Callback when command is spoken.
        from bombly.modules.whos_on_first import whos_on_first
        engine.speak(whos_on_first(extras))


class WordsMoreRule(CompoundRule):
    spec = "words more"                  # Spoken form of command.
    def _process_recognition(self, node, extras):   # Callback when command is spoken.
        from bombly.modules.whos_on_first import more
        engine.speak(more())


class PasswordResetRule(CompoundRule):
    spec = "password reset"                  # Spoken form of command.
    def _process_recognition(self, node, extras):   # Callback when command is spoken.
        from bombly.modules.passwords import reset
        reset()


class PasswordRule(CompoundRule):
    spec = "password <letters>"                  # Spoken form of command.
    extras = [Dictation("letters")]
    def _process_recognition(self, node, extras):   # Callback when command is spoken.
        from bombly.modules.passwords import solve_password
        for word in solve_password(extras):
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
