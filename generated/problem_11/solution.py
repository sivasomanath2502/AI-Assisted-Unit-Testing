def remove_Occ(s, c):
    first = s.find(c)
    last = s.rfind(c)
    if first == -1:
        return s
    if first == last:
        return s[:first] + s[first+1:]
    return s[:first] + s[first+1:last] + s[last+1:]