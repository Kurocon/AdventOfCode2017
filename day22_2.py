from collections import defaultdict

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

REVERSE_DIRS = {
    "up": "down",
    "right": "left",
    "down": "up",
    "left": "right",
}

MOVE_DIFFERENCES = {
    "up": (0, -1),
    "down": (0, 1),
    "left": (-1, 0),
    "right": (1, 0)
}


def burst(current_node, direction):
    global bursts_caused_infection

    if NODES[current_node] == "#":  # Infected
        newdir = RIGHT_DIRS[direction]
        NODES[current_node] = "F"  # Flagged
    elif NODES[current_node] == "F":  # Flagged
        newdir = REVERSE_DIRS[direction]
        NODES[current_node] = "."  # Clean
    elif NODES[current_node] == "W":  # Weakened
        newdir = direction
        NODES[current_node] = "#"  # Infected
        bursts_caused_infection += 1
    else:
        newdir = LEFT_DIRS[direction]
        NODES[current_node] = "W"  # Weakened

    diff = MOVE_DIFFERENCES[newdir]
    newnode = (current_node[0] + diff[0], current_node[1] + diff[1])

    return newnode, newdir


def parse_input(inp):
    result = defaultdict(lambda: ".")
    for i in range(len(inp)):
        for j in range(len(inp[i])):
            result[j, i] = inp[i][j]
    return result


with open('day22.in', 'r') as f:
    lines = f.readlines()
    data = [list(x.strip()) for x in lines]

NODES = parse_input(data)

curnode = (len(data[0]) // 2, len(data) // 2)
curdir = "up"
bursts_caused_infection = 0

for i in range(10000000):
    curnode, curdir = burst(curnode, curdir)

print("{} bursts caused infection".format(bursts_caused_infection))
