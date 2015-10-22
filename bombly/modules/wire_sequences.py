from collections import defaultdict

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


def wire_sequence(extras):
    global sequences
    words = str(extras['words'])
    print words
    words = words.replace('read', 'red').replace('blew', 'blue')
    print words
    words = [word for word in words.split() if word in ('red', 'blue', 'black', 'apple', 'bravo', 'charlie')]
    print words
    words = [words[x:x+2] for x in xrange(0, len(words), 2)]
    print words
    answer = []
    for index, item in enumerate(words):
        print index, item
        color, letter = item
        print "Color: {}".format(color)
        print "Letter: {}".format(letter)
        print "Count: {}".format(counts[color])
        print sequences[color]
        print counts[color]
        print sequences[color][counts[color]]
        print sequences[color][counts[color]]
        if letter[0] in sequences[color][counts[color]]:
            answer.append(str(index+1))

        counts[color] += 1

    if not answer:
        return 'cut nothing'
    else:
        return ', '.join(answer)


def reset():
    global counts
    counts = defaultdict(int)
