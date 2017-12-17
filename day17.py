inp = 355

c_i = 0
lst = [0]

for i in range(1, 2018):
	c_i = (c_i + inp) % len(lst)
	lst.insert(c_i+1, i)
	c_i += 1

print("Next to {} at index {} is {}".format(lst[c_i], c_i, lst[(c_i+1) % len(lst)]))

c_i = 0
result = 0

for i in range(1, 50000001):
	c_i = (c_i + inp) % i+1

	if c_i == 1:
		result = i

# Find 0
print("Next to 0 is {}".format(result))