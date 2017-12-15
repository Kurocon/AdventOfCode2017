factora = 16807
factorb = 48271

divisor = 2147483647

preva = 591
prevb = 393

# preva = 65
# prevb = 8921

count = 0

# Part 1
for i in range(40000000):
	preva = (preva * factora) % divisor
	prevb = (prevb * factorb) % divisor
	if (preva & 0xFFFF) == (prevb & 0xFFFF):
		count += 1

print("Count: {}".format(count))

# Part 2
factora2 = 4
factorb2 = 8
preva = 591
prevb = 393
count = 0

for i in range(5000000):
	nexta = (preva * factora) % divisor
	while nexta % factora2:
		nexta = (nexta * factora) % divisor
	nextb = (prevb * factorb) % divisor
	while nextb % factorb2:
		nextb = (nextb * factorb) % divisor
	preva, prevb = nexta, nextb
	if (preva & 0xFFFF) == (prevb & 0xFFFF):
		count += 1

print("Count: {}".format(count))
