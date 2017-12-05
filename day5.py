with open("day5.in", 'r') as f:
    inp = f.readlines()

data = [int(i) for i in inp]

curr_i = 0
curr_step = 0

while True:
    try:
        # Try to jump
        old_i = curr_i
        curr_i = old_i + data[old_i] # Set current index
        if data[old_i] >= 3:
            data[old_i] = data[old_i]-1  # Decrement previous
        else:
            data[old_i] = data[old_i]+1  # Increment previous
        curr_step += 1  # Increment step counter
    except IndexError:
        # Outside of range
        print("Jumped outside of range ({}) after {} steps.".format(curr_i, curr_step))
        break

