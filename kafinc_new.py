import numpy as np

class Office:
	def __init__(self, number):
		self.number = number
		self.forms_count = 0
		self.neighbors = set()
		self.inbox_count = 0

	def __repr__(self):
		return f"Office Number {self.number} has {self.forms_count} forms."

class Supervisor:
	def __init__(self):
		self.offices_count = 0
		self.offices = {}
		self.new_offices = {}
		self.adj_matrix = [] 
		self.offices_count = 0

	def initialize_offices(self):
		for number in range(1, self.offices_count + 1):
			self.offices[str(number)] = Office(number)
		
	def assign_neighbors(self):
		self.initialize_offices()

		print("Input the adjacency matrix: ")
		entries = list(map(int, input().split()))
		self.adj_matrix = np.array(entries).reshape(self.offices_count, self.offices_count)
		print(f"{self.adj_matrix = }")

		for i in range(self.offices_count):
			for j in range(self.offices_count):
				if self.adj_matrix[i][j] == 1:
					self.offices[str(i + 1)].neighbors.update(str(j + 1))
					self.offices[str(j + 1)].neighbors.update(str(i + 1))

	def distribute(self):
		is_stable = True
		for _, office in self.offices.items():
			distribution_amount = office.forms_count // len(office.neighbors)
			if distribution_amount > 0:
				is_stable = False
				for neighbor_number in office.neighbors:
					if neighbor_number not in self.offices:
						new_office = Office(neighbor_number)
						new_office.inbox_count = distribution_amount
						self.new_offices[neighbor_number] = new_office
					else:
						self.offices[neighbor_number].inbox_count += distribution_amount
				office.forms_count -= distribution_amount

		self.offices.update(self.new_offices)
		self.new_offices = {}

		for _, office in self.offices.items():
			office.forms_count += office.inbox_count
			office.inbox_count = 0

		print(self)
		return is_stable

	def stabilize(self, max_iterations=100_000):
		steps_taken = 0
		is_stable = self.distribute()
		while not is_stable:
			is_stable = self.distribute()
			steps_taken += 1
			if steps_taken >= max_iterations:
				raise RuntimeError("Help, we're in a loop")
		return steps_taken

	def __repr__(self):
		sorted_dict = dict(sorted(self.offices.items()))
		lst = []
		for _, office in sorted_dict.items():
			if office.number == 0:
				lst.append(f"({office.forms_count})")
			else:
				lst.append(f"{office.forms_count}")
		return f"<{', '.join(lst)}>"

if __name__ == "__main__":

	supervisor = Supervisor()
	supervisor.offices_count = int(input("Input the number of offices: "))
	supervisor.assign_neighbors()

	print(f"{supervisor.adj_matrix = }")
	for key in supervisor.offices:
		print(f"Neighbor set of office {key} = {supervisor.offices[key].neighbors}")

	"""
	reassignments = supervisor.stabilize()
	print(f"{reassignments=}: {supervisor.offices}")
	"""
