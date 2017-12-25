import re
import collections

tape = collections.defaultdict(int)
cursor = 0


"""Begin in state A.
Perform a diagnostic checksum after 6 steps.

In state A:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state B.
  If the current value is 1:
    - Write the value 0.
    - Move one slot to the left.
    - Continue with state B.

In state B:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the left.
    - Continue with state A.
  If the current value is 1:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state A."""

BEGIN_INSTR = re.compile(r'Begin in state (?P<beginstate>[A-Z])\.')
CHEKSUM_INSTR = re.compile(r'Perform a diagnostic checksum after (?P<checksum>[0-9]+) steps\.')
STATE_BEGIN = re.compile(r'In state (?P<statename>[A-Z]):')
STATE_IF = re.compile(r'If the current value is (?P<curval>[0-1]):')
WRITE_RULE = re.compile(r'- Write the value (?P<val>[0-1])\.')
MOVE_RULE = re.compile(r'- Move one slot to the (?P<dir>(left|right))\.')
CONTINUE_RULE = re.compile(r'- Continue with state (?P<nextstate>[A-Z])\.')

with open('day25.in', 'r') as f:
	inp = [x.strip() for x in f.readlines()]
	
	# Read begin state
	beginstate = BEGIN_INSTR.match(inp[0]).group('beginstate')
	# Checksum after
	checksum = int(CHEKSUM_INSTR.match(inp[1]).group('checksum'))

	states = {}
	instrs = {}

	i = 2
	while i < len(inp):
		instrs = {}
		# Disregard empty line
		#print("SKIP", inp[i])
		i += 1
		# Read state name
		#print("STATE", inp[i])
		state = STATE_BEGIN.match(inp[i]).group('statename')
		i += 1
		# Read next value
		#print("IF", inp[i])
		value = int(STATE_IF.match(inp[i]).group('curval'))
		i += 1
		# Read write instr
		#print("WRITE", inp[i])
		write = int(WRITE_RULE.match(inp[i]).group('val'))
		i += 1
		# Read move instr
		#print("MOVE", inp[i])
		move = MOVE_RULE.match(inp[i]).group('dir')
		i += 1
		# Read continue instr
		#print("CONTINUE", inp[i])
		nxt = CONTINUE_RULE.match(inp[i]).group('nextstate')
		i += 1
		instrs[value] = {'write': write, 'move': move, 'next': nxt}
		# Read next value
		value = int(STATE_IF.match(inp[i]).group('curval'))
		i += 1
		# Read write instr
		write = int(WRITE_RULE.match(inp[i]).group('val'))
		i += 1
		# Read move instr
		move = MOVE_RULE.match(inp[i]).group('dir')
		i += 1
		# Read continue instr
		nxt = CONTINUE_RULE.match(inp[i]).group('nextstate')
		i += 1
		instrs[value] = {'write': write, 'move': move, 'next': nxt}
		states[state] = instrs

#print(states)

# Start in the begin state
current_state = beginstate

#print(dict(tape), cursor, current_state)
# Run for the required amount of steps
for i in range(checksum):
	oldval = tape[cursor]
	# Write value belonging to current state and value
	tape[cursor] = states[current_state][oldval]['write']
	# Move in direction belonging to current state and value
	newdir = states[current_state][oldval]['move']
	if newdir == "left":
		cursor -= 1
	else:
		cursor += 1
	# Continue in next state belonging to current state and value
	current_state = states[current_state][oldval]['next']

	#print(dict(tape), cursor, current_state)

print("Number of 1s:", sum([x for x in tape.values() if x == 1]))
