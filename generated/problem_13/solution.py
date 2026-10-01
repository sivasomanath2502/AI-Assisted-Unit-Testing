def count_common(words):
    from collections import Counter
    counts = Counter(words)
    sorted_items = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    return sorted_items[:4]