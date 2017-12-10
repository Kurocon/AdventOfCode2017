print("Part 1:")
lst = list(range(256))
lns = [88,88,211,106,141,1,78,254,2,111,77,255,90,0,54,205]
skip = 0
c_i = 0

def reverse(ln, start):
	global lst
	end_part = lst[start:start+ln]
	begin_part = lst[:(ln-len(end_part))]
	total_part = end_part + begin_part
	new_part = list(reversed(total_part))
	i = start
	for x in new_part:
		lst[i] = x
		i = (i + 1) % len(lst)

for ln in lns:
	reverse(ln, c_i)
	c_i = (c_i + ln + skip) % len(lst)
	skip += 1

print("First two numbers multiplied: {} x {} = {}".format(lst[0], lst[1], lst[0]*lst[1]))

######

print("")
print("Part 2:")
lst = list(range(256))
lns = [ord(x) for x in "88,88,211,106,141,1,78,254,2,111,77,255,90,0,54,205"]
suffix = [17, 31, 73, 47, 23]
skip = 0
c_i = 0

def reverse(ln, start):
    global lst
    end_part = lst[start:start+ln]
    begin_part = lst[:(ln-len(end_part))]
    total_part = end_part + begin_part
    new_part = list(reversed(total_part))
    i = start
    for x in new_part:
        lst[i] = x
        i = (i + 1) % len(lst)

for i in range(64):
    for ln in (lns+suffix):
        reverse(ln, c_i)
        c_i = (c_i + ln + skip) % len(lst)
        skip += 1

knothash = []
for i in range(16):
    begin = i*16
    end = (i+1)*16
    data = lst[begin:end]
    value = None
    for x in data:
        if value is None:
            value = x
        else:
            value ^= x
    knothash.append(value)

print("Knot hash: {}".format("".join('{:02x}'.format(a) for a in knothash)))
