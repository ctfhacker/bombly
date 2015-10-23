def button(extras, batteries, car, freak):
    """
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
        return spoken
        return
    """

    words = str(extras['words'])
    print words
    words = words.replace('read', 'red').replace('blew', 'blue')
    print words
    if 'blue' in words and 'abort' in words:
        return 'Press and hold'
    elif 'detonate' in words and batteries > 1:
        return 'Press and release'
    elif 'white' in words and car in ('true', 'yes'):
        return 'Press and hold'
    elif batteries > 2 and freak in ('true', 'yes'):
        return 'Press and release'
    elif 'yellow' in words:
        return 'Press and hold'
    elif 'red' in words and 'hold' in words:
        return 'Press and release'
    else:
        return 'Press and hold'


def button_color(extras):
    words = str(extras['words'])
    print words
    words = words.replace('read', 'red').replace('blew', 'blue')
    print words
    if 'blue' in words:
        return 'four'
    elif 'yellow' in words:
        return 'five'
    else:
        return 'one'
