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

registers = {chr(x): 0 for x in range(ord('a'), ord('z')+1)}
last_sound = 0

def p_debug(i, line, registers, last_sound):
    print("")
    print("---  STACK FRAME  ---")
    print("PCNT: {}".format(i))
    print("EXEC: {}".format(line))
    print("REGS: {}".format(registers))
    print("LSTS: {}".format(last_sound))
    print("---END STACK FRAME---")
    print("")

#p_debug(0, "n/a", registers, last_sound)

def execute():
    global instrs, registers, last_sound, i
    line = instrs[i]
    increment = True

    if line['instr'] == "snd":
        # Play sound with freq equal to X
        try:
            last_sound = int(line['x'])
        except ValueError:
            last_sound = registers[line['x']]
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
        # If X not 0, recover frequency of last sound
        try:
            x = int(line['x'])
        except ValueError:
            x = registers[line['x']]
        if x != 0:
            print("RCV: Recovered {}".format(last_sound))
            return True
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

    #p_debug(i, line, registers, last_sound)

i = 0
while i < len(instrs):
    stop = execute()
    if stop:
        break
