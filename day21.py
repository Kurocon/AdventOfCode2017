import re

START_PATTERN = """.#.
..#
###"""

cur_pattern = [list(x) for x in START_PATTERN.split()]
RULE = re.compile(r'(?P<pre>[.#]+(/[.#]+)*) => (?P<post>[.#]+(/[.#]+)*)')


def flip(square):
    return [list(reversed(x)) for x in square]


def rotate(square):
    # Rotate a square clockwise
    return list(zip(*square[::-1]))


def split_patterns(data, size):
    new_squares = []

    for i in range(len(data) // size):
        for j in range(len(data) // size):
            # print("i=", i)
            # print("j=", j)
            square = [x[(j * size):((j + 1) * size)] for x in data[(i * size):((i + 1) * size)]]
            new_square = None
            rotate_count = 0
            while new_square is None:
                # print("sqare", square)
                try:
                    # print("trying", "/".join(["".join(x) for x in square]))
                    new_square = enhancement_rules["/".join(["".join(x) for x in square])]
                except KeyError:
                    try:
                        flipped_square = flip(square)
                        # print("flipped")
                        # print("trying", "/".join(["".join(x) for x in flipped_square]))
                        new_square = enhancement_rules["/".join(["".join(x) for x in flipped_square])]
                    except KeyError:
                        if rotate_count < 5:
                            # print("rotated")
                            square = rotate(square)
                            rotate_count += 1
                        else:
                            raise ValueError("Could not find match for pattern {}".format("/".join(["".join(x) for x in square])))

            # print("found", "/".join(["".join(x) for x in square]), " => ", "/".join(["".join(x) for x in new_square]))
            new_squares.append(new_square)
            # print("next")

    return new_squares


def join_pattens(squares, line_size):
    block_size = len(squares[0])
    num_blocks_per_line = line_size // block_size
    result = []
    # print("joining")
    # print("squares", squares)
    # print("lsize", line_size)
    # print("bsize", block_size)
    # print("bpl", num_blocks_per_line)

    # For each square
    for i in range(len(squares)):
        # print("new i = ", i)
        if i % num_blocks_per_line == 0:
            # Add lines for the new blocks
            for k in range(block_size):
                result.append([])

        # For each line in the block
        for j in range(block_size):
            # print("sq", squares[i][j])
            # print("index", ((i // num_blocks_per_line) * block_size) + j)
            result[((i // num_blocks_per_line) * block_size) + j].extend(squares[i][j])

        # print(result)
    return result


# Read input
enhancement_rules = {}
test_input = ["../.# => ##./#../...", ".#./..#/### => #..#/..../..../#..#"]

with open('day21.in', 'r') as f:
    inp = f.readlines()

    for l in inp:
        match = RULE.match(l)
        if match:
            pre = match.group('pre')
            post = [list(x) for x in match.group('post').split("/")]
            #print("added rule {} > {}".format(pre, post))
            enhancement_rules[pre] = post
        else:
            print("invalid input {}".format(l))

print("rules", enhancement_rules)

# Process input
for i in range(18):
    # print("curr", cur_pattern)
    temp_squares = []
    new_line_size = 0
    if len(cur_pattern) % 2 == 0:
        temp_squares = split_patterns(cur_pattern, 2)
        new_line_size = (len(cur_pattern) // 2) * 3
    elif len(cur_pattern) % 3 == 0:
        temp_squares = split_patterns(cur_pattern, 3)
        new_line_size = (len(cur_pattern) // 3) * 4
    else:
        print("Unknown pattern size {}".format(len(cur_pattern)))

    cur_pattern = join_pattens(temp_squares, new_line_size)

print("Finished, result after iterations:")
print("\n".join(["".join(x) for x in cur_pattern]))

on = len([y for x in cur_pattern for y in x if y == "#"])
print("{} pixels are on".format(on))
