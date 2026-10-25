def count_consistent_strings(allowed, words):
    allowed_set = set(allowed)
    return sum(all(ch in allowed_set for ch in w) for w in words)


print(count_consistent_strings("ab", ["ad", "bd", "aaab", "baa", "badab"]))
print(count_consistent_strings("abc", ["a", "b", "c", "ab", "ac", "bc", "abc"]))
print(count_consistent_strings("cad", ["cc", "acd", "b", "ba", "bac", "bad", "ac", "d"]))
