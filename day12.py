import re

inp = """0 <-> 2
1 <-> 1
2 <-> 0, 3, 4
3 <-> 2, 4
4 <-> 2, 3, 6
5 <-> 6
6 <-> 4, 5""".split('\n')

with open('day12.in', 'r') as f:
    inp = [x.strip() for x in f.readlines()]

REG = re.compile(r'([0-9]+) <-> (([0-9]+, )*[0-9]+)')

data = {}
nodes = set()

def parse(line):
    global data
    match = REG.match(line)
    if match:
        prog = match.group(1)
        links = [x.strip() for x in match.group(2).split(", ")]
        data[prog] = links
    else:
        raise ValueError("Invalid line {}".format(line))

def group(start, exclude):
    global data
    global nodes
    nodes.add(start)
    for node in data[start]:
        if node not in nodes and node not in exclude:
            nodes.add(node)
            group(node, nodes)

for line in inp:
    print(line)
    parse(line)


group('0', [])

print("There are {} nodes in group 0".format(len(nodes)))

to_check = list(data.keys())
groups = []
while to_check:
    x = to_check[0]
    nodes = set()
    group(x, [])
    groups.append(nodes.copy())
    for n in nodes:
        if n in to_check:
            to_check.remove(n)

print("There are {} groups in total".format(len(groups)))
