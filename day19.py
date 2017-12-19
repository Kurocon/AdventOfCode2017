with open('day19.in') as f:
	inp = [[y for y in x.replace("\n", "")] for x in f.readlines()]

start_index = (0, 0)
for i in range(len(inp[0])):
	if inp[0][i] == "|":
		start_index = (0, i)
		break

direction = "down"
current_index = start_index
collected = []
stop = False
stepcount = 0

dtx = {
	'up': (-1, 0),
	'down': (1, 0),
	'left': (0, -1),
	'right': (0, 1),
}
opp = {
	'up': 'down',
	'down': 'up',
	'left': 'right',
	'right': 'left',
}


def get(index):
	return inp[index[0]][index[1]]

while not stop:
	cur = get(current_index)
	print(current_index, ": '", cur, "'")

	if cur not in "|-+":
		if cur == " ":
			print("Stepped out of line on ", current_index)
			stop = True
		else:
			collected.append(cur)

		if direction in ['up', 'down']:
			cur = "|"
		else:
			cur = "-"

	if cur == "|" or cur == "-":
		current_index = (current_index[0]+dtx[direction][0], current_index[1]+dtx[direction][1])
	elif cur == "+":
		other_dirs = filter(lambda x: x != opp[direction], ["up", "down", "left", "right"])

		new_dir = direction
		for d in other_dirs:
			try:
				if get((current_index[0]+dtx[d][0], current_index[1]+dtx[d][1])) != " ":
					new_dir = d
					break
			except IndexError:
				continue
		direction = new_dir
		current_index = (current_index[0]+dtx[direction][0], current_index[1]+dtx[direction][1])

	stepcount += 1

stepcount -= 1

print("Collected letters: {}".format("".join(collected)))
print("Stepped {} steps".format(stepcount))