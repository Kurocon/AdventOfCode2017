import re

REG = r'^(?P<name>[a-z]+) \((?P<weight>[0-9]+)\)( -> (?P<names>([a-z]+, )*)(?P<lastname>[a-z]+))?'

data = {}

with open('day7.in', 'r') as f:
	inp = "\n".join(f.readlines())

for line in inp.split('\n'):
    match = re.match(REG, line)
    if match:
        name = match.group('name')
        weight = match.group('weight')
        children = []
        if match.group('names') is None:
            if match.group('lastname') is not None:
                children = [match.group('lastname')]
        else:
            children = (match.group('names') + match.group('lastname')).split(', ')
    data[name] = {'weight': weight, 'children': {x: None for x in children}}

def insert(data, name, namedata):
    if data is None:
        pass
    inserted = False
    for x in data:
        if data[x] is None:
            continue
        if name in data[x]['children']:
            data[x]['children'][name] = namedata
            inserted = inserted or True
        else:
            for nxt in data[x]['children']:
                if data[x]['children'][nxt] is not None:
                    inserted = inserted or insert(data[x]['children'], nxt, namedata)
                    if inserted:
                        break;
    return inserted

changed = True
while changed:
    changed = False
    to_remove = []
    for x in data:
        done = insert(data, x, data[x])
        if done:
            changed = True
            to_remove.append(x)

    for x in to_remove:
        del data[x]

print("Root node: {}".format(data.keys()))

def check_weight(name, data):
    if data is None:
        return 0
    weight = int(data['weight'])
    child_weights = {}
    if data['children']:
        # All child weights must be the same
        for child in data['children']:
            child_weights[child] = check_weight(child, data['children'][child])
        w = -1
        for ch in child_weights:
            if w == -1:
                w = child_weights[ch]
            else:
                if w != child_weights[ch]:
                    child_ws = [check_weight(x, data['children'][ch]['children'][x]) for x in data['children'][ch]['children']]
                    child_sum = sum(child_ws)
                    node_w = int(data['children'][ch]['weight'])
                    correct_weight = node_w - ((node_w+child_sum) - w)
                    print("Error detected, children total weights:")
                    print(child_ws)
                    print("Child {} has wrong weight {}, must be {} (total {}, must be {})!".format(ch, data['children'][ch]['weight'], correct_weight, child_weights[ch], w))

    # Return on weight plus sum of child weights
    return int(weight) + sum([int(child_weights[x]) for x in child_weights])

root = list(data.keys())[0]
check_weight(root, data[root])

