def count_common(words):
    if not words:
        return 0
    counts = {}
    for word in words:
        counts[word] = counts.get(word, 0) + 1
    return max(counts.values())