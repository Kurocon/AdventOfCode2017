import re

REG = re.compile(r'^(?P<instr>(set|sub|mul|jnz)) (?P<x>([a-z]|[\-0-9]+))( (?P<y>([a-z]|[\-0-9]+)))?')

with open('day23.in', 'r') as f:
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

registers_0 = {chr(x): 0 for x in range(ord('a'), ord('h')+1)}
registers_0['a'] = 1
mul_count_0 = 0


def p_debug(i, line, registers, send_count):
    print("")
    print("---  STACK FRAME  ---")
    print("PCNT: {}".format(i))
    print("EXEC: {}".format(line))
    print("REGS: {}".format(registers))
    print("MULC: {}".format(send_count))
    print("---END STACK FRAME---")
    print("")


#p_debug(0, "n/a", registers, last_sound)


def execute():
    global instrs, p0recv
    global registers_0, i_0, mul_count_0
    registers = registers_0

    line = instrs[i_0]
    increment = True

    if line['instr'] == "set":
        # Set reg X to val Y
        try:
            registers[line['x']] = int(line['y'])
        except ValueError:
            registers[line['x']] = registers[line['y']]
    elif line['instr'] == "sub":
        # Decrease reg X with Y
        try:
            registers[line['x']] -= int(line['y'])
        except ValueError:
            registers[line['x']] -= registers[line['y']]
    elif line['instr'] == "mul":
        # Set reg X to X times Y
        mul_count_0 += 1
        try:
            registers[line['x']] *= int(line['y'])
        except ValueError:
            registers[line['x']] *= registers[line['y']]
    elif line['instr'] == "jnz":
        # Jump with offset of Y, if X is not 0.
        # Offset 2 is next instruction, offset -1 previous.
        try:
            x = int(line['x'])
        except ValueError:
            x = registers[line['x']]

        if x != 0:
            try:
                y = int(line['y'])
            except ValueError:
                y = registers[line['y']]

            i_0 += y
            increment = False

    else:
        print("Unknown instr '{}'.".format(line['instr']))

    if increment:
        i_0 += 1

    # p_debug(i_0, line, registers, mul_count_0)


i_0 = 0
stop_0 = False
p0recv = False

while i_0 < len(instrs):
    stop_0 = stop_0 or execute()
    if stop_0:
        break

print("Program multiplied {} times".format(mul_count_0))

