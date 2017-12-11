import re
from collections import defaultdict

LINE = re.compile(r'(?P<vara>[a-z]+) (?P<op>(inc|dec)) (?P<val1>[\-0-9]+) if (?P<varb>[a-z]+) (?P<cmp>(>|<|<=|>=|==|!=)) (?P<val2>[\-0-9]+)')

def parse(line):
    match = LINE.match(line)
    if not match:
        raise ValueError("No match for line '{}'".format(line))
    return {
        'rega': match.group('vara'), 'op': match.group('op'), 'val1': int(match.group('val1')),
        'regb': match.group('varb'), 'cnd': match.group('cmp'), 'val2': int(match.group('val2')),
    }

def execute(p):
    global maximum_value
    condition_success = False
    if p['cnd'] == ">":
        condition_success = registers[p['regb']] > p['val2']
    elif p['cnd'] == "<":
        condition_success = registers[p['regb']] < p['val2']
    elif p['cnd'] == ">=":
        condition_success = registers[p['regb']] >= p['val2']
    elif p['cnd'] == "<=":
        condition_success = registers[p['regb']] <= p['val2']
    elif p['cnd'] == "==":
        condition_success = registers[p['regb']] == p['val2']
    elif p['cnd'] == "!=":
        condition_success = registers[p['regb']] != p['val2']
    else:
        print("Invalid condition {}".format(p['cnd']))

    if condition_success:
        if p['op'] == "inc":
            registers[p['rega']] += p['val1']
            if registers[p['rega']] > maximum_value:
                maximum_value = registers[p['rega']]
        elif p['op'] == "dec":
            registers[p['rega']] -= p['val1']
            if registers[p['rega']] > maximum_value:
                maximum_value = registers[p['rega']]
        else:
            print("Invalid operation {}".format(p['op']))

registers = defaultdict(int)
maximum_value = 0

with open('day8.in', 'r') as f:
    inp = f.readlines()

for line in inp:
    parsed = parse(line.strip())
    execute(parsed)

print(dict(registers))
biggest = max(registers.keys(), key=lambda x: registers[x])
print("Biggest register is {} with value {}".format(biggest, registers[biggest]))
print("Biggest value in any register during operation: {}".format(maximum_value))