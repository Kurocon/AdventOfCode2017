def is_anagram(words):
    for word in words:
        for compare in words:
            if word != compare:
                workingcopy = list(compare)
                for letter in word:
                    try:
                        workingcopy.remove(letter)
                    except ValueError:
                        pass

                if workingcopy == [] and len(word) == len(compare):
                    return True

with open("day4_input.txt", 'r') as f:
    lines = f.readlines()

res = 0
for line in lines:
    words = line.strip().split(" ")
    if len(words) != len(set(words)):
        print("Rejected b/c words: {}".format(line.strip()))
        pass
    elif is_anagram(words):
        print("Rejected b/c anagram: {}".format(line.strip()))
        pass
    else:
        print("Accepted: {}".format(line.strip()))
        res += 1

print("Result: {} passphrases out of {} are valid.".format(res, len(lines)))

