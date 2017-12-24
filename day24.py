from collections import defaultdict

pieces = defaultdict(list)
with open('day24.in', 'r') as f:
    inp = [x.strip().split('/') for x in f.readlines()]
    for x in inp:
        pieces[int(x[0])].append(int(x[1]))
        # Add the reverse as well because that is also possible
        pieces[int(x[1])].append(int(x[0]))


def get_pieces(pieces, piece):
    return [(piece, x) for x in pieces[piece]]


def get_bridges(bridge, pieces):
    bridges = []

    # Create bridges with all possible pieces,
    # Removing that piece from the pieces in the next iteration.
    #print(bridge)
    next_number = bridge[-1][1] if len(bridge) > 0 else 0
    nextpieces = get_pieces(pieces, next_number)
    for nextpiece in nextpieces:
        #print("Trying", nextpiece)

        newbridge = copy_bridge(bridge)
        newbridge.append(nextpiece)
        newpieces = copy_pieces(pieces)
        newpieces[nextpiece[0]].remove(nextpiece[1])
        # Remove the reverse too
        newpieces[nextpiece[1]].remove(nextpiece[0])
        if len(newpieces[nextpiece[0]]) == 0:
            del newpieces[nextpiece[0]]
        if len(newpieces[nextpiece[1]]) == 0:
            del newpieces[nextpiece[1]]
        newbridges = get_bridges(newbridge, newpieces)

        bridges.extend(newbridges)

    # Add the current bridge
    if bridge:
        bridges.append(bridge)

    return bridges


def copy_bridge(bridge):
    return [(x[0], x[1]) for x in bridge]


def copy_pieces(pieces):
    res = defaultdict(list)
    copy = {x: y.copy() for x, y in pieces.items()}
    res.update(copy)
    return res


def bridge_strength(bridge):
    return sum([x[0]+x[1] for x in bridge])


def remove_duplicates(bridges):
    str_bridges = set()
    for b in bridges:
        s = " -- ".join(["{}/{}".format(x[0], x[1]) for x in b])
        str_bridges.add(s)

    new_bridges = []
    for s in str_bridges:
        b = s.split(" -- ")
        nbr = []
        for x in b:
            pts = x.split("/")
            nbr.append((int(pts[0]), int(pts[1])))
        new_bridges.append(nbr)

    return sorted(new_bridges)


bridges = get_bridges([], pieces)
maxlen = max([len(x) for x in bridges])
longest = [x for x in bridges if len(x) == maxlen]

bridges = remove_duplicates(bridges)
longest = remove_duplicates(longest)

print("Strongest Bridge: ")
strengths = []
for b in bridges:
    strengths.append((b, bridge_strength(b)))
    # print(" -- ".join(["{}/{}".format(x[0], x[1]) for x in b]))
    # print(bridge_strength(b))

print(sorted(strengths, key=lambda x: x[1])[-1])

print("Longest, strongest bridge: ")
strengths = []
for b in longest:
    strengths.append((b, bridge_strength(b)))
    # print(" -- ".join(["{}/{}".format(x[0], x[1]) for x in b]))
    # print(bridge_strength(b))

print(sorted(strengths, key=lambda x: x[1])[-1])