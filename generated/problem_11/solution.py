def remove_Occ(s, char):
    first_idx = s.find(char)
    if first_idx == -1:
        return s
    last_idx = s.rfind(char)
    if first_idx == last_idx:
        return s[:first_idx] + s[first_idx+1:]
    return s[:first_idx] + s[first_idx+1:last_idx] + s[last_idx+1:]