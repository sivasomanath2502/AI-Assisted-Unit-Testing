def split_lowerstring(s):
    result = []
    current = []
    for ch in s:
        if 'a' <= ch <= 'z':
            result.append(''.join(current))
            current = []
        else:
            current.append(ch)
    result.append(''.join(current))
    return result