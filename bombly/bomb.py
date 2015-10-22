import random

# Battery characteristics
batteries = 99
freak = 'freak'
car = 'car'
parallel = 'parallel'
serial = 'serial'
vowel = 'vowel'


def odd_serial():
    return serial in (1, 3, 5, 7, 9)


def even_serial():
    return serial in (0, 2, 4, 6, 8)


def set_car(extras):
    global car
    car = str(extras['car'])


def set_batteries(extras):
    global batteries
    batteries = int(str(extras['batteries']))


def set_freak(extras):
    global freak
    freak = str(extras['word'])


def set_parallel(extras):
    global parallel
    parallel = str(extras['word'])


def set_serial(extras):
    global serial
    serial = str(extras['word'])


def set_vowel(extras):
    global vowel
    vowel = str(extras['word'])


def status():
    global batteries
    global freak
    global car
    global parallel
    global serial
    global vowel

    from bombly.modules import morse_code, whos_on_first, memory, wire_sequences

    # Battery characteristics
    print 'batteries', batteries
    print 'frk', freak
    print 'car', car
    print 'parallel', parallel
    print 'serial', serial
    print 'vowel', vowel

    # Wire sequence
    print 'wire sequence', wire_sequences.counts

    # Memory
    print 'values', memory.values
    print 'position', memory.positions
    print 'curr_stage', memory.curr_stage

    # Morse
    print 'morse_letters', morse_code.morse_letters

    # On First Words
    print 'on first words', whos_on_first.on_first_words


def done():
    lines = [
        "I AM YOUR BOMB DEFUSING OVERLORD",
        "BOOM SHAKALAKA",
    ]

    global batteries
    global freak
    global car
    global parallel
    global serial
    global vowel

    # Battery characteristics
    batteries = 99
    freak = 'freak'
    car = 'car'
    parallel = 'parallel'
    serial = 'serial'
    vowel = 'false'

    reset()

    return random.sample(lines, 1)


def exploded():
    lines = [
        "YOU STUPID FUCK",
        "NOT MY FAULT!",
        "PLANNED..",
        "CRAP, BOMB EXPLODED",
        "HOW CAN YOU TELL ME THAT?",
        "IT'S ALL YOUR FAULT",
    ]
    return random.sample(lines, 1)


def reset():
    global batteries
    global freak
    global car
    global parallel
    global serial
    global vowel

    # Battery characteristics
    batteries = 99
    freak = 'freak'
    car = 'car'
    parallel = 'parallel'
    serial = 'serial'
    vowel = 'vowel'

    from bombly.modules import morse_code, whos_on_first, memory, wire_sequences, passwords

    wire_sequences.reset()
    memory.reset()
    morse_code.reset()
    whos_on_first.reset()
    passwords.reset()
