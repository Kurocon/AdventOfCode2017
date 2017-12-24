LEFT_DIRS = {
    "up": "left",
    "left": "down",
    "down": "right",
    "right": "up",
}

RIGHT_DIRS = {
    "up": "right",
    "right": "down",
    "down": "left",
    "left": "up",
}

MOVE_DIFFERENCES = {
    "up": (0, -1),
    "down": (0, 1),
    "left": (-1, 0),
    "right": (1, 0)
}


def burst(current_node, direction):
    global bursts_caused_infection

    infected = current_node in INFECTED_NODES
    if infected:
        newdir = RIGHT_DIRS[direction]
        INFECTED_NODES.remove(current_node)
    else:
        newdir = LEFT_DIRS[direction]
        INFECTED_NODES.append(current_node)
        bursts_caused_infection += 1

    diff = MOVE_DIFFERENCES[newdir]
    newnode = (current_node[0] + diff[0], current_node[1] + diff[1])

    return newnode, newdir


def parse_input(inp):
    # Calculate center
    center_y = (len(inp) // 2) if len(inp) % 2 == 0 else ((len(inp) // 2))
    center_x = (len(inp[0]) // 2) if len(inp[0]) % 2 == 0 else ((len(inp[0]) // 2))

    infected = []

    for i in range(len(inp)):
        for j in range(len(inp[i])):
            if inp[i][j]:
                infected.append((j - center_x, i - center_y))

    return infected


with open('day22.in', 'r') as f:
    lines = f.readlines()
    data = [[True if y == "#" else False for y in list(x.strip())] for x in lines]

INFECTED_NODES = parse_input(data)

curnode = (0, 0)
curdir = "up"
bursts_caused_infection = 0

for i in range(10000):
    curnode, curdir = burst(curnode, curdir)

print(INFECTED_NODES)
print("{} bursts caused infection".format(bursts_caused_infection))