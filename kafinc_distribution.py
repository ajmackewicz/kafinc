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
	print(f"Considering {list1} and {list2} with offset = {offset}")
	if (list1 == [1] and list2 == [1]): # or (list1 == [0] and list2 == [0]):
		compilation = list1 + list2
	elif (list1 == [0] and list2 == [0]):
		compilation = list1 + list2
	elif list1 == [1] or list1 == [0]:
		compilation = [list1[0] + list2[0]] + list2[1:]
	elif list2 == [1]:
		compilation = list1[0:-1] + [list1[-1] + list2[0]]
	else:
		for i in range(offset):
			print(f"In list1: {i}")
			print(f"...Appending {list1[i]}")
			compilation.append(list1[i])
		if offset < len(list1):
			for j in range(offset, len(list1)):
				print(f"In overlap: {j}")
				print(f"...Appending {list1[j] + list2[j - offset]}")
				compilation.append(list1[j] + list2[j - offset])
		elif offset > len(list1):
			print("Offset is greater than length of list1.")
			sys.exit()
		for k in range(len(list1) - offset, len(list2)):
			print(f"In list2: {k}")
			print(f"...Appending {list2[k]}")
			compilation.append(list2[k])
		print(f"compilation = {compilation}")
	return compilation

def cascade_sandpiles(sandpiles):
	compilation = sandpiles[0]
	del sandpiles[0]
	offset = 1
	for i in range(len(sandpiles)):
		if compilation == [1] or compilation == [0]:
			print(f"Pile = {compilation}")
			compilation = add_lists_offset(compilation, sandpiles[i], offset)
			continue
		elif sandpiles[i] == [1]:
			print("Pile = [1]")
			compilation = add_lists_offset(compilation, sandpiles[i], offset)
			continue
		else:
			print("Running cascade_sandpiles else.")
			compilation = add_lists_offset(compilation, sandpiles[i], offset)
			offset += 1
	return compilation

def all_zeros_and_ones(lst):
	for item in lst:
		if item != 1 or item != 0:
			return False
	return True

def loop_through(pile):
	pile_current = pile
	while not all_zeros_and_ones(pile_current):
		print(f"pile_current = {pile_current}")
		sandpiles = create_sandpiles(pile_current)
		pile_current = cascade_sandpiles(sandpiles)
	return pile_current

# Test interlocked structures
n = int(input("Enter number of elements in the initial pile: "))
pile_init = list(map(int, input("\nEnter the values in the pile, separated by spaces: ").strip().split()))[:n]
print(f"Pile = {pile_init}")

sandpiles = create_sandpiles(pile_init)
print(f"Sandpiles = {sandpiles}")

compilation = cascade_sandpiles(sandpiles)
print(f"Compilation of sandpiles: {compilation}")

"""
final_pile = loop_through(pile_init)
print(f"Final pile: {final_pile}")
"""
