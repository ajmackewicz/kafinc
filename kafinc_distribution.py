def is_even(numb):
	if numb % 2 == 0:
		return True
	else:
		return False

def create_sandpile(grain):
	if grain == 1:
		return [1]
	elif grain == 0:
		return [0]
	elif is_even(grain):
		return [int(grain/2), 0, int(grain/2)]
	else:
		return [int(grain//2), 1, int(grain//2)]

def create_sandpiles(pile_prev):
	sandpiles = []
	for grain in pile_prev:
		sandpiles.append(create_sandpile(grain))
	return sandpiles

def add_lists_offset(list1, list2, offset):
	compilation = []
	for i in range(offset):
		compilation.append(list1[i])
	if offset < len(list1):
		for j in range(offset, len(list1)):
			compilation.append(list1[j] + list2[j - offset])
	elif offset > len(list1):
		print("Offset is greater than length of list1.")
		sys.exit()
	for k in range(len(list1) - offset, len(list2)):
		compilation.append(list2[k])
	return compilation

def cascade_sandpiles(sandpiles):
	compilation = sandpiles[0]
	del sandpiles[0]
	offset = 1
	for pile in sandpiles:
		if pile == [0]:
			print("Pile = [0]")
			offset += 1
			continue
		elif pile == [1]:
			print("Pile = [1]")
			offset = 0
		else:
			compilation = add_lists_offset(compilation, pile, offset)
			offset += 1
	return compilation

# Test interlocked structures
n = int(input("Enter number of elements in the initial pile: "))
pile_init = list(map(int, input("\nEnter the values in the pile, separated by spaces: ").strip().split()))[:n]
print(f"Pile = {pile_init}")

sandpiles = create_sandpiles(pile_init)
print(f"Sandpiles = {sandpiles}")

compilation = cascade_sandpiles(sandpiles)
print(f"Compilation of sandpiles: {compilation}")
