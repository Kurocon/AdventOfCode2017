import re

REG = re.compile(r'^(?P<instr>(snd|set|add|mul|mod|rcv|jgz)) (?P<x>([a-z]|[\-0-9]+))( (?P<y>([a-z]|[\-0-9]+)))?')

with open('day18.in', 'r') as f:
    inp = f.readlines()

instrs = []
for x in inp:
    match = REG.match(x.strip())
    if not match:
        print("Line '{}' does not match!".format(x.strip()))
    else:
        instrs.append({
            'instr': match.group('instr'),
            'x': match.group('x'),
            'y': match.group('y')
        })

registers_0 = {chr(x): 0 for x in range(ord('a'), ord('z')+1)}
registers_1 = {chr(x): 0 for x in range(ord('a'), ord('z')+1)}
registers_1['p'] = 1  # Program 1 should have pid 1
send_count_0 = 0
send_count_1 = 0

def p_debug(thread, i, line, registers, queue_0, queue_1, send_count):
    print("")
    print("---  STACK FRAME  ---")
    print("THRD: {}".format(thread))
    print("PCNT: {}".format(i))
    print("EXEC: {}".format(line))
    print("REGS: {}".format(registers))
    print("Q_0 : {}".format(queue_0))
    print("Q_1 : {}".format(queue_1))
    print("SNDC: {}".format(send_count))
    print("---END STACK FRAME---")
    print("")

#p_debug(0, "n/a", registers, last_sound)

def execute(thread):
    global instrs, queue_0, queue_1, p0recv, p1recv
    if thread == 0:
        global registers_0, send_count_0, i_0
        registers, send_count, i = registers_0, send_count_0, i_0
    elif thread == 1:
        global registers_1, send_count_1, i_1
        registers, send_count, i = registers_1, send_count_1, i_1
    if thread == 0:
        i = i_0
    elif thread == 1:
        i = i_1
    line = instrs[i]
    increment = True

    if line['instr'] == "snd":
        # Send X to other program
        try:
            x = int(line['x'])
        except ValueError:
            x = registers[line['x']]
        send_count += 1
        if thread == 0:
            queue_1.append(x)
        elif thread == 1:
            queue_0.append(x)
    elif line['instr'] == "set":
        # Set reg X to val Y
        try:
            registers[line['x']] = int(line['y'])
        except ValueError:
            registers[line['x']] = registers[line['y']]
    elif line['instr'] == "add":
        # Increase reg X with Y
        try:
            registers[line['x']] += int(line['y'])
        except ValueError:
            registers[line['x']] += registers[line['y']]
    elif line['instr'] == "mul":
        # Set reg X to X times Y
        try:
            registers[line['x']] *= int(line['y'])
        except ValueError:
            registers[line['x']] *= registers[line['y']]
    elif line['instr'] == "mod":
        # Set reg X to X mod Y
        try:
            registers[line['x']] %= int(line['y'])
        except ValueError:
            registers[line['x']] %= registers[line['y']]
    elif line['instr'] == "rcv":
        # Receive value in register X, wait until value is received
        if thread == 0:
            if len(queue_0) > 0:
                registers[line['x']] = queue_0[0]
                queue_0 = queue_0[1:]
                p0recv = False
            else:
                increment = False
                p0recv = True
        elif thread == 1:
            if len(queue_1) > 0:
                registers[line['x']] = queue_1[0]
                queue_1 = queue_1[1:]
                p1recv = False
            else:
                increment = False
                p1recv = True
    elif line['instr'] == "jgz":
        # Jump with offset of Y, if X is greater than 0.
        # Offset 2 is next instruction, offset -1 previous.
        try:
            x = int(line['x'])
        except ValueError:
            x = registers[line['x']]

        if x > 0:
            try:
                y = int(line['y'])
            except ValueError:
                y = registers[line['y']]

            i += y
            increment = False


    else:
        print("Unknown instr '{}'.".format(line['instr']))

    if increment:
        i += 1

    if thread == 0:
        registers_0, send_count_0, i_0 = registers, send_count, i
    elif thread == 1:
        registers_1, send_count_1, i_1 = registers, send_count, i

    #p_debug(thread, i, line, registers, queue_0, queue_1, send_count)

i_0 = 0
i_1 = 0
stop_0, stop_1 = False, False
p0recv, p1recv = False, False
# queue_0 is input queue for thread 0, queue_1 is input for thread 1
queue_0, queue_1 = [], []
while i_0 < len(instrs) or i_1 < len(instrs):
    stop_0 = stop_0 or execute(0)
    stop_1 = stop_1 or execute(1)
    if stop_0 and stop_1:
        break
    if p0recv and p1recv and len(queue_0) == 0 and len(queue_1) == 0:
        print("Aborted program because of deadlock.")
        print("Program 0 sent {} times".format(send_count_0))
        print("Program 1 sent {} times".format(send_count_1))
        break