def remove_Occ(string, char):
    if not char:
        return string
    
    first = string.find(char)
    if first == -1:
        return string
    
    last = string.rfind(char)
    
    result = []
    for i, c in enumerate(string):
        if c == char and (i == first or i == last):
            continue
        result.append(c)
    
    return ''.join(result)