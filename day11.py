start = (0, 0)
end = (0, 0)

with open("day11.in", 'r') as f:
    inp = f.readlines()[0].strip().split(",")

#inp = ['ne', 'ne', 'ne']
#inp = ['ne', 'ne', 'sw', 'sw']
#inp = ['ne', 'ne', 's', 's']
#inp = ['se', 'sw', 'se', 'sw', 'sw']

def step(i):
    global end
    x, y = end
    if i == "n":
        end = (x+1, y)
    elif i == "nw":
        end = (x+1, y+1)
    elif i == "ne":
        end = (x, y-1)
    elif i == "s":
        end = (x-1, y)
    elif i == "sw":
        end = (x, y+1)
    elif i == "se":
        end = (x-1, y-1)
    else:
        print("Unknown input {}".format(i))

print("End: ", end)

def dist(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    du = x2 - x1
    dv = y2 - y1
    if (du >= 0 and dv >= 0) or (du < 0 and dv < 0):
        return max(abs(du), abs(dv))
    else:
        return abs(du) + abs(dv)

for i in inp:
    step(i)
print("Distance: ", dist(start, end))

furthest = 0
end = (0, 0)

for i in inp:
    step(i)
    d = dist(start, end)
    if d > furthest:
        furthest = d

print("Furthest: ", furthest)
