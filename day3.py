inp = 368078
import collections
data = collections.defaultdict(dict)

def calc_coords(n):
    if n < 1:
        raise ValueError("N must be 1 or higher")
    max_x = 0
    max_y = 0
    curr_x = 0
    curr_y = 0
    x_direction = "right"
    y_direction = "up"
    first_bigger = True

    for i in range(n-1):
        #print("State: mx:{} my:{} cx:{} cy:{} xd:{} yd:{}".format(max_x, max_y, curr_x, curr_y, x_direction, y_direction))
        
        # Assign data as sum of surrounding blocks
        sum_data = 0
        for x in range(-1, 2):
            for y in range(-1, 2):
                try:
                    sum_data += data[curr_x+x][curr_y+y]
                except KeyError:
                    pass
        if curr_x == 0 and curr_y == 0:
            sum_data = 1
        data[curr_x][curr_y] = sum_data
        if first_bigger and sum_data > n:
            print("Value written {} was first bigger than input {}".format(sum_data, n))
            first_bigger = False

        if x_direction == "right" and y_direction == "up":
            # Going right on the bottom
            if curr_x <= max_x:
                if curr_x == max_x:
                    max_x += 1
                    x_direction = "left"
                curr_x += 1
            else:
                raise ValueError("Maximum x was {} but current x was {}!".format(max_x, curr_x))
        elif x_direction == "right" and y_direction == "down":
            # Going down on the left side
            if curr_y > -max_y:
                if curr_y == -(max_y-1):
                    y_direction = "up"
                curr_y -= 1
            else:
                raise ValueError("Minimum y was {} but current y was {}".format(-max_y, curr_y))
        elif x_direction == "left" and y_direction == "up":
            # Going up on the right side
            if curr_y <= max_y:
                if curr_y == max_y:
                    max_y += 1
                    y_direction = "down"
                curr_y += 1
            else:
                raise ValueError("Maximum y was {} but current y was {}".formay(max_y, curr_y))
        elif x_direction == "left" and y_direction == "down":
            # Going left on the top
            if curr_x > -max_x:
                if curr_x == -(max_x-1):
                    x_direction = "right"
                curr_x -= 1
            else:
                raise ValueError("Minimum x was {} but current x was {}".format(-max_x, curr_x))
        else:
            raise ValueError("Impossible situation! xdir: {} ydir: {}".format(x_direction, y_direction))

    print("{} is at coordinates {},{}".format(n, curr_x, curr_y))
    return curr_x, curr_y


def manhattan_distance(x, y):
    # Calculate manhattan distance between input and 0,0
    return abs(x)+abs(y)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        inp = int(sys.argv[1])
    x, y = calc_coords(inp)

    print("Manhattan distance = {}".format(manhattan_distance(x, y)))

