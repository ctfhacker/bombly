# Password
curr_password = []


def solve_password(extras):
    global curr_password
    letters = str(extras['letters'])
    letters = [letter[0].lower() for letter in letters.split()]
    curr_password.append(letters)
    print curr_password

    passwords = ['about',
    'after', 'again', 'below', 'could', 'every', 'first', 'found', 'great',
    'house', 'large', 'learn', 'never', 'other', 'place', 'plant', 'point',
    'right', 'small', 'sound', 'spell', 'still', 'study', 'their', 'there',
    'these', 'thing', 'think', 'three', 'water', 'where', 'which', 'world',
    'would', 'write']

    possibles = []
    if len(curr_password) == 2:
        for password in passwords:
            if password[0] in curr_password[0] and password[2] in curr_password[1]:
                possibles.append(password)

        print possibles

    return possibles


def reset():
    global curr_password
    curr_password = []
    print curr_password
