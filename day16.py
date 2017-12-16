programs = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 
            'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p']

def spin(programs, num):
    e = programs[-num:]
    b = programs[:-num]
    return e + b

def exchange(programs, a, b):
    programs[b], programs[a] = programs[a], programs[b]
    return programs

def partner(programs, a, b):
    ia = programs.index(a)
    ib = programs.index(b)
    return exchange(programs, ia, ib)

with open('day16.in', 'r') as f:
    inp = f.readlines()[0].strip().split(',')

def step(programs):
    for i in inp:
        if i[0] == "s":
            programs = spin(programs, int(i[1:]))
        elif i[0] == "x":
            a, b = i[1:].split("/")
            programs = exchange(programs, int(a), int(b))
        elif i[0] == "p":
            a, b = i[1:].split("/")
            programs = partner(programs, a, b)
    return programs

print("".join(programs))

start_programs = programs.copy()
repetition = False
rcount = 0
cache = [programs.copy()]

while not repetition:
    programs = step(programs)
    rcount += 1
    cache.append(programs.copy())
    if programs == start_programs:
        repetition = True

print("Repetition found after {} cycles".format(rcount))
end_step = 1000000000 % rcount
print("".join(cache[end_step]))
