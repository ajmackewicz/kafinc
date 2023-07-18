class Office:
	def __init__(self, numb_forms):
		self.numb_forms = numb_forms
		self.to_give = 0
	
	def split(self):
		self.to_give = self.numb_forms//2
		self.numb_forms %= 2

	def add_forms(self, numb_to_add):
		self.numb_forms += numb_to_add
		
class Building:
	def __init__(self, forms_initial): # to do: make list of objects with each having their initial forms
		self.offices = []
		self.forms_initial = forms_initial # list(int)

	def assign_paperwork(self):
		for i in range(len(self.forms_initial)):
			self.offices.append[Office(self.forms_initial[i])]

	def add_new_office(self):
		# add office object where needed, at beginning of list or end

	def distribute(self):
		# ! TO DO
		if self.offices[1].to_give != 0:
			# add forms to sides
			self.offices[0].numb_forms.add_forms(self.offices[1].to_give)
			# add forms to other side 
		else:
			# do something
		for i in range(1, len(self.offices - 1)):
			self.offices[i].add_forms(self.offices[i - 1].to_give)
			self.offices[i].add_forms(self.offices[i + 1].to_give)
		self.offices[-1].add_forms(self.offices[-2].to_give)
		# add condition for adding another office, s.a. when the paperwork is at the edges

	def return_offices(self):
		return self.offices

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

def is_zero_or_one(lst):
	if len(lst) == 1:
		return True
	else:
		return False

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
