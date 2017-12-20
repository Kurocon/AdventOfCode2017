import pprint
import re

REG = re.compile(r'^p=<(?P<px>(-)?[0-9]+),(?P<py>(-)?[0-9]+),(?P<pz>(-)?[0-9]+)>, v=<(?P<vx>(-)?[0-9]+),(?P<vy>(-)?[0-9]+),(?P<vz>(-)?[0-9]+)>, a=<(?P<ax>(-)?[0-9]+),(?P<ay>(-)?[0-9]+),(?P<az>(-)?[0-9]+)>')

with open('day20.in', 'r') as f:
    inp = f.readlines()


def step(data):
    for p in data:
        # Apply accelleration
        p['v']['x'] += p['a']['x']
        p['v']['y'] += p['a']['y']
        p['v']['z'] += p['a']['z']

        # Apply velocity
        p['p']['x'] += p['v']['x']
        p['p']['y'] += p['v']['y']
        p['p']['z'] += p['v']['z']

    # Check collisions
    for i, p in enumerate(data):
        to_disable = set()
        for j, q in enumerate(data):
            if not p['collision'] and not q['collision']:
                if i != j and (p['p']['x'] == q['p']['x'] and p['p']['y'] == q['p']['y'] and p['p']['z'] == q['p']['z']):
                    to_disable.add(j)
                    to_disable.add(i)
        for x in to_disable:
            data[x]['collision'] = True

    return data


def manhattan_distances(data):
    distances = []
    for p in data:
        distances.append(abs(p['p']['x']) + abs(p['p']['y']) + abs(p['p']['z']))
    return distances


def can_stop(data):
    stop = True
    for p in data:
        c1 = (p['p']['x'] < 0 and p['v']['x'] <= 0 and p['a']['x'] <= 0) or (p['p']['x'] >= 0 and p['v']['x'] >= 0 and p['a']['x'] >= 0)
        c2 = (p['p']['y'] < 0 and p['v']['y'] <= 0 and p['a']['y'] <= 0) or (p['p']['y'] >= 0 and p['v']['y'] >= 0 and p['a']['y'] >= 0)
        c3 = (p['p']['z'] < 0 and p['v']['z'] <= 0 and p['a']['z'] <= 0) or (p['p']['z'] >= 0 and p['v']['z'] >= 0 and p['a']['z'] >= 0)
        if not (c1 and c2 and c3):
            stop = False
            #print("Preventing stop:")
            #pprint.pprint(p)
    return stop


data = []
for l in inp:
    match = REG.match(l)
    if match:
        data.append({
            'p': {'x': int(match.group('px')), 'y': int(match.group('py')), 'z': int(match.group('pz'))},
            'v': {'x': int(match.group('vx')), 'y': int(match.group('vy')), 'z': int(match.group('vz'))},
            'a': {'x': int(match.group('ax')), 'y': int(match.group('ay')), 'z': int(match.group('az'))},
            'collision': False
        })

condition = True
s_count = 0
while condition:
    data = step(data)
    condition = not can_stop(data)
    s_count += 1
    #pprint.pprint(data)

distances = manhattan_distances(data)
minimum_i = None
minimum_v = None
for i, v in enumerate(distances):
    if minimum_i is None or minimum_v is None or minimum_v > v:
        minimum_i = i
        minimum_v = v

print("Minimum manhattan distance: point {} ({}):".format(minimum_i, minimum_v))
pprint.pprint(data[minimum_i])
print("{} points have not collided".format(len([x for x in data if not x['collision']])))
print("Simulated {} steps".format(s_count))
