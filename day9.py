with open('day9.in', 'r') as f:
	inp = f.readlines()[0]

data = {}

groups = []
garbage = False
ignore = False

garbage_count = 0

# Parse groups
for c in inp:
	if not ignore:
		if c == ">" and garbage:
			garbage = False
		elif c == "!" and garbage:
			ignore = True
		elif garbage:
			garbage_count += 1
		elif c == "{":
			groups.append({})
		elif c == "<":
			garbage = True
		elif c == "}": 
			g = groups[-1]
			if len(groups) > 1:
				if 'groups' not in groups[-2]:
					groups[-2]['groups'] = []
				groups[-2]['groups'].append(g)
				del groups[-1]
		elif c == ",":
			pass
		else:
			print("Unexpected character {}".format(c))
	else:
		ignore = False

data = groups[0]
import pprint
pprint.pprint(data)

total_score = 0
# Calculate score
def calculate(data, parent_score):
	global total_score
	data['score'] = parent_score + 1
	total_score += parent_score + 1
	if 'groups' in data and data['groups'] != []:
		for i, group in enumerate(data['groups']):
			data['groups'][i] = calculate(group, data['score'])
	return data

data = calculate(data, 0)
pprint.pprint(data)
print("Total score: {}".format(total_score))
print("Garbage found: {} chars".format(garbage_count))
