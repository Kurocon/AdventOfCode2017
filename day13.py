import re

inp = """0: 3
1: 2
4: 4
6: 4""".split("\n")

REG = re.compile(r'([0-9]+): ([0-9]+)')

with open('day13.in', 'r') as f:
    inp = f.readlines()

data = []

def reset():
    global data
    data = []
    tmp_data = {}
    for line in inp:
        match = REG.match(line)
        if match:
            tmp_data[match.group(0)] = {
                'layer': int(match.group(1)),
                'depth': int(match.group(2)),
                'scanpos': 0,
                'direction': 'inc'
            }
        else:
            raise ValueError("Line did not match: {}".format(line))

    c_l = 0
    for d in sorted(list(tmp_data.values()), key=lambda x: x['layer']):
        while d['layer'] > c_l:
            data.append({'layer': c_l, 'depth': 0, 'scanpos': 0, 'direction': 'inc'})
            c_l += 1
        data.append(d)
        c_l += 1

current_position = -1
collisions = []

def step(stop_on_collision=False):
    """Step through the layer. Return true if stepped past last layer"""
    global data
    global current_position

    # First the hacker steps
    current_position += 1

    # If we are past the last layer, we are done
    if current_position >= len(data):
        return True

    if current_position >= 0:
        # Check if there was a collision
        if data[current_position]['scanpos'] == 0 and data[current_position]['depth'] != 0:
            collisions.append({
                'layer': current_position,
                'depth': data[current_position]['depth']
            })
            if stop_on_collision:
                return True

    # Then the bots step
    for l in data:
        if l['depth'] != 0:
            if l['scanpos'] == 0:
                l['direction'] = 'inc'
            elif l['scanpos'] == l['depth']-1:
                l['direction'] = 'dec'

            if l['direction'] == "inc":
                l['scanpos'] += 1
            else:
                l['scanpos'] -= 1

    return False

stop = False

reset()

while not stop:
    stop = step()

severity = 0
for c in collisions:
    severity += c['layer']*c['depth']
print("Severity is {}".format(severity))

stop = False
current_delay = -1
while not stop:
    # Reset and run the simulation with decreasing starting positions
    # until we find a result without any collisions
    reset()
    current_position = current_delay
    collisions = []
    done = False
    while not done:
        done = step(stop_on_collision=True)
    if len(collisions) == 0:
        print("No collisions on round with delay {}!".format(abs(current_delay+1)))
        stop = True
    print("Offset {}, {} collision at layer {}".format(abs(current_delay+1), len(collisions), collisions[0]['layer']))
    current_delay -= 1

