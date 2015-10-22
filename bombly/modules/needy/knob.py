def knob(extras):
    words = str(extras['words'])
    print words
    words = ''.join([word for word in words.split() if word in ('one', 'zero')])
    print words
    leds = words.replace('one', '1').replace('zero', '0').replace(' ', '')
    print leds
    if leds == '111011' or leds == '011010':
        return 'Up'
    if leds == '111001' or leds == '010010':
        return 'Down'
    if leds == '100010' or leds == '000010':
        return 'Left'
    if leds == '111111' or leds == '111100':
        return 'Right'
