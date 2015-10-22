def complicated_wires(extras, batteries, serial, parallel):
    """
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
    """

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

    for key, val in meaning.iteritems():
        print key, val


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

        print wire, total

        if meaning[total] == 'cut':
            if answer == 'cut nothing':
                answer = 'cut '
            answer += str(index+1) + ', '

    return answer
