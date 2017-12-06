inp = "2	8	8	5	4	2	3	1	5	5	1	2	15	13	5	14".split()

test_inp = "0 2 7 0".split()

history = []
current = [int(x) for x in inp]
steps = 0
stop = False
loop_size = 0
loop_stop = False
loop_start = None

while not stop or not loop_stop:
    print(current)
    biggest_bank = max(current)
    biggest_bank_i = current.index(biggest_bank)
    curr_i = biggest_bank_i

    # Empty biggest bank
    current[biggest_bank_i] = 0
    while biggest_bank > 0:
        curr_i = (curr_i + 1) % len(current)
        current[curr_i] += 1
        biggest_bank -= 1
    
    # Check if loop has ended
    if loop_start is not None and not loop_stop and current == loop_start:
        loop_stop = True

    # Check if current already in history
    if not stop and current in history:
        stop = True
        loop_start = current.copy()
    
    # Add current to history
    history.append(current.copy())

    # Increment the step counter if we haven't encountered it, else increment the loop counter
    if not stop:
        steps += 1
    elif not loop_stop:
        loop_size += 1
print(current)
print("Loop detected after {} steps".format(steps))
print("Loop is of size {}".format(loop_size))

