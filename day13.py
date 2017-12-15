import re
from pprint import pprint

REG = re.compile(r'([0-9]+): ([0-9]+)')

with open('day13.in', 'r') as f:
    inp = f.readlines()

data = []
max_depth = 0

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
        if int(match.group(2)) > max_depth:
            max_depth = int(match.group(2))
    else:
        raise ValueError("Line did not match: {}".format(line))

def reset():
    global data
    data = []
    c_l = 0
    for d in sorted(list(tmp_data.values()), key=lambda x: x['layer']):
        while d['layer'] > c_l:
            data.append({'layer': c_l, 'depth': 0, 'scanpos': 0, 'direction': 'inc'})
            c_l += 1
        data.append(d.copy())
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
print ("Severity is {}".format(severity))

stop = False
current_delay = 0
while not stop:
    # For each layer calculate if there is a collision
    collision = False
    for layer in data:
        if layer['depth'] == 0:
            continue

        if ((current_delay + layer['layer']) % ((layer['depth']*2)-2)) == 0:
            collision = True
            break

    if not collision:
        print ("No collision with offset {}!".format(current_delay))
        stop = True

    if current_delay % 10000 == 0:
        print ("Processing... {}".format(current_delay))

    current_delay += 1
