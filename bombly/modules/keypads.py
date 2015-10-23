def keypad(extras):
    symbols = str(extras['symbols'])

    groups = [
        ['tennis', 'apple', 'a', 'l', 'lightning', 'spider', 'h', 'house', 'c', 'charlie'],
        ['e', 'echo', 'tennis', 'c', 'charlie', 'o', 'oscar', 'starr', 'star', 'h', 'house', 'question'],
        ['copyright', 'but', 'butt', 'o', 'oscar', 'k', 'r', 'romeo', 'l', 'starr', 'star'],
        ['six', 'paragraph', 'b', 'bravo', 'spider', 'k', 'question', 'smile'],
        ['goblet', 'smile', 'b', 'bravo', 'c', 'charlie', 'paragraph', 'three', 'star'],
        ['six', 'e', 'echo', 'equals', 'smash', 'goblet', 'in', 'omega']
    ]

    print symbols
    symbols = symbols.replace('butt', 'but')
    curr_symbols = symbols.replace('.', '').lower().split()
    print curr_symbols

    answer = ''
    for group in groups:
        for symbol in curr_symbols:
            if symbol not in group:
                break
        else:
            for symbol in group:
                if symbol in curr_symbols:
                    answer += symbol + ' '

    return answer
