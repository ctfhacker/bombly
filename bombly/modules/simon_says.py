def simon(extras, vowel):
    print str(extras['words'])
    # if vowel == 'vowel':
        # engine.speak("Serial contain vowel?")
        # return

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

    return new_words
