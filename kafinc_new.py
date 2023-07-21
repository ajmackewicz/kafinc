import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

class Office:
	def __init__(self, number):
		self.number = number
		self.forms_count = 0
		self.neighbors = set()
		self.inbox_count = 0
		self.previously_occupied = False

	'''
	def __repr__(self):
		return f"Office Number {self.number} has {self.forms_count} forms."
	'''

class Supervisor:
	def __init__(self):
		self.offices_count = 0
		self.offices = {}
		self.new_offices = {}
		self.adj_matrix = [] 
		self.offices_count = 0
		self.prev_configurations = []
		self.cycle_configurations = []
		self.edges_list = []

	def initialize_offices(self):
		for number in range(1, self.offices_count + 1):
			self.offices[str(number)] = Office(number)
		
	def assign_forms(self):
		print("Input the forms per offices list: ")
		forms_configuration_initial = tuple(map(int, input().split()))
		for i in range(len(forms_configuration_initial)):
			self.offices[str(i + 1)].forms_count = forms_configuration_initial[i]
		self.current_configuration = self.get_current_config()

	def assign_neighbors(self):
		result = None
		while result is None:
			try:
				print("Input the adjacency matrix: ")
				neighbors = list(map(int, input().split()))
				self.adj_matrix = np.array(neighbors).reshape(self.offices_count, self.offices_count)
				# self.adj_matrix = np.matrix(self.adj_matrix)
				result = True
			except ValueError:
				print("Invalid adjacency matrix.")
				pass
			else:
				print("Adjacency matrix:")
				print(f"{self.adj_matrix}")

		for i in range(self.offices_count):
			for j in range(self.offices_count):
				if self.adj_matrix[i][j] == 1:
					self.offices[str(i + 1)].neighbors.update(str(j + 1))
					self.offices[str(j + 1)].neighbors.update(str(i + 1))

	def is_final_config(self):
		is_final = True
		for _, office in self.offices.items():
			if not office.forms_count == 1 and not office.forms_count == 0:
				is_final = False
				break
		return is_final

	def is_cycling(self):
		if self.current_configuration in self.prev_configurations:
			return True
		else:
			return False

	def get_current_config(self):
		forms_configuration = []
		sorted_dict = dict(sorted(self.offices.items()))
		for _, office in sorted_dict.items():
			forms_configuration.append(office.forms_count)
		forms_configuration = tuple(forms_configuration)

		return forms_configuration
		
	def distribute(self):
		self.current_configuration = self.get_current_config()
		
		is_stable = True

		for _, office in self.offices.items():
			distribution_amount = office.forms_count // len(office.neighbors)
			if distribution_amount > 0:
				if self.is_cycling():
					cycle_length = len(self.prev_configurations) - self.prev_configurations.index(self.current_configuration)
					print(f"Cycling config reached: {cycle_length = }")
					return True
				is_stable = False
				for neighbor_number in office.neighbors:
					if neighbor_number not in self.offices:
						new_office = Office(neighbor_number)
						new_office.inbox_count = distribution_amount
						self.new_offices[neighbor_number] = new_office
					else:
						self.offices[neighbor_number].inbox_count += distribution_amount
				office.forms_count -= distribution_amount * len(office.neighbors)

		for _, office in self.offices.items():
			office.forms_count += office.inbox_count
			office.inbox_count = 0

		self.prev_configurations.append(self.current_configuration)

		self.offices.update(self.new_offices)
		self.new_offices = {}

		print(self.current_configuration)
		return is_stable

	def stabilize(self, max_iterations=100):
		steps_taken = 0
		is_stable = self.distribute()
		self.draw() # Draw!
		while not is_stable:
			is_stable = self.distribute()
			steps_taken += 1
			if steps_taken >= max_iterations:
				raise RuntimeError("Help, we're in a loop")
		return steps_taken

	def get_labels_dict(self):
		print(f"{self.current_configuration = }")
		labels_dict = {}
		for i in range(len(self.current_configuration)):
			labels_dict[i + 1] = str(self.current_configuration[i])
		print(f"{labels_dict = }")
		return labels_dict

	# Assign list of edge-tuples
	def draw(self):
		for i in range(self.offices_count):
			j = 0
			j += i
			while j < self.offices_count:
				if self.adj_matrix[i][j] == 1:
					self.edges_list.append((i + 1, j + 1))
				j += 1

		G = nx.Graph()
		G.add_edges_from(self.edges_list)
		pos = nx.spring_layout(G)

		weights = self.get_labels_dict()
		
		print(f"{weights = }")
		nx.draw_networkx(G, pos=pos, with_labels=False)
		nx.draw(G, pos=pos, node_color="skyblue", node_size=2000, font_size=10)
		nx.draw_networkx_labels(G, pos=pos, labels=weights)
		plt.show()

	"""
	def __repr__(self):
		sorted_dict = dict(sorted(self.offices.items()))
		lst = []
		for _, office in sorted_dict.items():
			if office.number == 0:
				lst.append(f"({office.forms_count})")
			else:
				lst.append(f"{office.forms_count}")
		return f"<{', '.join(lst)}>"
	"""

if __name__ == "__main__":
	supervisor = Supervisor()
	supervisor.offices_count = int(input("Input the number of offices: "))

	# Assign forms and neighbors as adjacency matrix
	supervisor.initialize_offices()
	supervisor.assign_forms()
	supervisor.assign_neighbors()

	# Test edge-tuples creation code
	print(f"{supervisor.edges_list = }")

	reassignments = supervisor.stabilize()
	print(f"Number of {reassignments = }")

	supervisor.draw()
