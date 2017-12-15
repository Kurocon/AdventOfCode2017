key = "nbysizxe"
key = "flqrgnkx"
hashdata = {}
suffix = [17, 31, 73, 47, 23]

def reverse(data, ln, start):
    end_part = data[start:start+ln]
    begin_part = data[:(ln-len(end_part))]
    total_part = end_part + begin_part
    new_part = list(reversed(total_part))
    i = start
    for x in new_part:
        data[i] = x
        i = (i + 1) % len(data)
    return data

def knothash(k):
    data = list(range(256))
    inputs = [ord(x) for x in k]
    c_i = 0
    skip = 0

    # Calculate hash
    for i in range(64):
        for d in (inputs + suffix):
            data = reverse(data, d, c_i)
            c_i = (c_i + d + skip) % len(data)
            skip += 1

    # Generate representation
    knothash = []
    for i in range(16):
        begin = i*16
        end = (i+1)*16
        d = data[begin:end]
        val = None
        for x in d:
            if val is None:
                val = x
            else:
                val ^= x
        knothash.append(val)
    return knothash

# Calculate knot hashes
used = 0
for i in range(128):
    h = knothash("{}-{}".format(key, i))
    h = [int(x, base=16) for x in "".join("{:02x}".format(a) for a in h)]
    hashdata[i] = "".join("{:04b}".format(x) for x in h)
    used += sum([int(x) for x in hashdata[i]])
    hashdata[i] = ["#" if x == "1" else "." for x in hashdata[i]]
    print("{:3n}: {}".format(i, "".join(hashdata[i])))
print("\nUsed space: {}/{}\n".format(used, 128*128))

# Part 2

unique_i = 1
for i in range(128):
    for j in range(128):
        if hashdata[i][j] == "#":
            # Check surroundings
            # If we have a number on the top or left of us, use that
            # Elise, use a new number
            changed = False
            if i > 0 and type(hashdata[i-1][j]) == int:
                hashdata[i][j] = hashdata[i-1][j]
                changed = True
            if j > 0 and type(hashdata[i][j-1]) == int:
                if changed and hashdata[i][j] != hashdata[i][j-1]:
                    # Loop through the entire graph, replace all instances of the
                    # number to the left with the number set above.
                    num = hashdata[i][j-1]
                    r_num = hashdata[i][j]
                    for x in range(128):
                        for y in range(128):
                            if hashdata[x][y] == num:
                                hashdata[x][y] = r_num
                else:
                    hashdata[i][j] = hashdata[i][j-1]
                    changed = True

            if not changed:
                hashdata[i][j] = unique_i
                unique_i += 1
                changed = True

l = len(str(unique_i))
for i in range(128):
    print("".join("{:^{width}}".format(x, width=l+2) for x in hashdata[i]))


count = set()
for x in range(128):
    for y in range(128):
        count.add(hashdata[x][y])

count.remove('.')

print("There are {} unique groups".format(len(count)))