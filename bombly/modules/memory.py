# Memory
values = []
positions = []
curr_stage = 1


def memory(extras):
    global values
    global positions
    global curr_stage
    words = str(extras['words'])
    print words
    words = [word for word in words.split() if word in ('one', 'two', 'three', 'four')]
    print words
    if len(words) != 5:
        return 'Try memory again'

    display = words[0]
    stage = words[1:]

    print "Current Stage: {}".format(curr_stage)
    print "Values: {}".format(values)
    print "Positions: {}".format(values)
    if curr_stage == 1:
        if display == 'one':
            answer = stage[1]
        if display == 'two':
            answer = stage[1]
        if display == 'three':
            answer = stage[2]
        if display == 'four':
            answer = stage[3]
        position = stage.index(answer)

    if curr_stage == 2:
        if display == 'one':
            answer = 'four'
        if display == 'two':
            answer = stage[positions[0]]
        if display == 'three':
            answer = stage[0]
        if display == 'four':
            answer = stage[positions[0]]
        position = stage.index(answer)

    if curr_stage == 3:
        if display == 'one':
            answer = values[1]
            position = 'one'
        if display == 'two':
            answer = values[0]
            position = 'two'
        if display == 'three':
            answer = stage[2]
            position = stage.index(answer)
        if display == 'four':
            answer = 'four'
            position = stage.index(answer)

    if curr_stage == 4:
        if display == 'one':
            answer = stage[positions[0]]
            position = stage.index(answer)
        if display == 'two':
            answer = stage[0]
            position = stage.index(answer)
        if display == 'three':
            answer = stage[positions[1]]
            position = stage.index(answer)
        if display == 'four':
            answer = stage[positions[1]]
            position = stage.index(answer)

    if curr_stage == 5:
        if display == 'one':
            answer = values[0]
        if display == 'two':
            answer = values[1]
        if display == 'three':
            answer = values[3]
        if display == 'four':
            answer = values[2]
        position = stage.index(answer)

    values.append(answer)
    positions.append(position)
    curr_stage += 1
    print "Answer: {}".format(answer)
    if curr_stage > 5:
        values = []
        positions = []
        curr_stage = 1

    return answer


def reset():
    global positions
    global curr_stage
    global values
    positions = []
    values = []
    curr_stage = 1
