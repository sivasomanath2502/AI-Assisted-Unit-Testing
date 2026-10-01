def split_lowerstring(s):
    result = []
    current = ""
    started = False
    for char in s:
        if char.islower():
            if current:
                result.append(current)
            current = char
            started = True
        else:
            if started:
                current += char
    if current:
        result.append(current)
    return result