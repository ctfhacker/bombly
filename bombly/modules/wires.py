def wires(extras, sanitize_colors, odd_serial):
    """
    spoken = 'need'
    if serial == 'serial':
        spoken += ' last digit of serial'
    if spoken != 'need':
        engine.speak(spoken)
        return
    """

    wire = str(extras['wires'])
    wire = sanitize_colors(wire)
    wire = wire.split()
    
    if len(wire) == 3:
        if 'red' not in wire:
            return 'cut second wire'
        elif wire[-1] == 'white':
            return 'cut last wire'
        elif wire.count('blue') > 1:
            return 'cut last blue wire'
        else:
            return 'cut last wire'

    elif len(wire) == 4:
        if wire.count('red') > 1 and odd_serial():
            return 'cut last red wire'
        elif wire[-1] == 'yellow' and wire.count('red') == 0:
            return 'cut first wire'
        elif wire.count('blue') == 1:
            return 'cut first wire'
        elif wire.count('yellow') > 1:
            return 'cut last wire'
        else:
            return 'cut second wire'

    elif len(wire) == 5:
        if wire[-1] == 'black' and odd_serial():
            return 'cut fourth wire'
        elif wire.count('red') and wire.count('yellow') > 1:
            return 'cut first wire'
        elif wire.count('black') == 0:
            return 'cut second wire'
        else:
            return 'cut first wire'

    elif len(wire) == 6:
        if wire.count('yellow') == 0 and odd_serial():
            return 'cut third wire'
        elif wire.count('yellow') == 1 and wire.count('white') > 1:
            return 'cut fourth wire'
        elif wire.count('red') == 0:
            return 'cut last wire'
        else:
            return 'cut fourth wire'
