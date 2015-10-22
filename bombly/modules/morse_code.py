# Morse
morse_letters = []


def morse_code(extras):
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
        return words[combos[code]]

    possibles = []
    for key, val in combos.iteritems():
        curr_word = ''.join([morse[letter] for letter in key])
        if code.startswith(curr_word):
            # print val, key, code, words[val]
            print words[val]


def reset():
    global morse_letters
    morse_letters = []
