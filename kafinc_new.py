"""
Adjacency Matrices 

Three-regular Graphs
4 nodes: 0111011101110
6 nodes: 011100101010110001100011010101001110
8 nodes: 0101100010100100010100101010000110000101010010100010010100011010
10 nodes: 0100110000101000100001010001000010100010100100000110000010010100010100001000101000010001010000110010

Other graphs
Peterson graph: 0100110000101000100001010001000010100010100100000110000001100100000011001001000100010110000000101100
Octahedron: 011011 101101 110110 011011 101101 110110
"""

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import time

def get_adj_mat(n, layout):
    adj_matrix = np.zeros([n, n], dtype=int)
    if layout == "c_n":
        adj_matrix = get_adj_mat_deg2(n)
    elif layout == "deg3loop":
        adj_matrix = get_adj_mat_deg3(n)
    elif layout == "other":
        adj_matrix = get_adj_mat_manual(n)
    elif layout == "k_n":
        adj_matrix = get_adj_mat_k_n(n)
    elif layout == "test":
        adj_matrix = get_adj_mat_dodecahedron(n)
    return adj_matrix
    
def get_adj_mat_manual(n):
    adj_matrix = np.zeros([n, n], dtype=int)
    result = None
    while result is None:
        try:
            print("Input the adjacency matrix: ")
            neighbors = list(map(int, [*input()]))
            adj_matrix = np.array(neighbors).reshape(n, n)
            adj_matrix = np.asmatrix(adj_matrix)
            result = True
        except ValueError:
            print("Invalid adjacency matrix.")
            pass
    return adj_matrix

def get_adj_mat_deg2(n):
    adj_matrix = np.zeros([n, n], dtype=int)
    for i in range(n):
        adj_matrix[i][(i - 1)%n] = 1
        adj_matrix[i][(i)%n] = 0
        adj_matrix[i][(i + 1)%n] = 1
    return adj_matrix

def get_adj_mat_deg3(n):
    adj_matrix = np.zeros([n, n], dtype=int)
    m = int(n/2)
    intractions = np.zeros([m, m], dtype=int)
    interactions = np.zeros([m, m], dtype=int)
    for i in range(m):
        intractions[i][(i - 1)%m] = 1
        intractions[i][i%m] = 0
        intractions[i][(i + 1)%m] = 1
        interactions[i][i] = 1
    sub_matrix_top = np.hstack((intractions, interactions))
    sub_matrix_bottom = np.hstack((interactions, intractions))
    adj_matrix = np.vstack((sub_matrix_top, sub_matrix_bottom))
    return adj_matrix

def get_adj_mat_k_n(n):
    adj_matrix = np.ones([n, n], dtype=int)
    for i in range(n):
        adj_matrix[i][i] = 0
    return adj_matrix

def get_adj_mat_dodecahedron(n):
    adj_mat = np.zeros([n, n], dtype=int)
    for i in range(n):
        adj_mat[i, (i-2)%n] = 1
        adj_mat[i, (i-1)%n] = 1
        adj_mat[i, (i+1)%n] = 1
    return adj_mat

def get_edge_count(n, graph_type, adj_mat):
    edge_count = 0
    if graph_type == "k_n":
        edge_count = int(0.5 * n * (n - 1))
    elif graph_type == "deg3loop":
        edge_count = int(1.5 * n)
    elif graph_type == "other":
        print(f"{adj_mat = }")
        for i in range(int(n/2)): # by adj_mat's symmetry
            for j in range(int(n/2)):
                if adj_mat[i][j] == 1:
                    edge_count += 1
        edge_count *= 0.5 
        edge_count = int(edge_count)
    print(f"{edge_count = }")
    return edge_count

class Office:
    def __init__(self, number):
        self.number = number
        self.forms_count = 0
        self.neighbors = set()
        self.inbox_count = 0
        self.previously_occupied = False

    def __repr__(self):
        return f"Office Number {self.number} has {self.forms_count} forms"

class PublicRelations:
    def __init__(self):
        self.purpose = ""
        self.purposes = ["c_n", "deg3loop", "other", "testdeg3loop", "k_n", "test_k_n", "test_other", "test"]

    def get_purpose_id(self):
        self.purpose = ""
        result = None
        while result is None:
            purpose_id = int(input("""Choose the type of layout:
    1. two-regular graph, c_n
    2. three-regular graph, double loop
    3. other
    4. test three-regular graph, double loop
    5. complete graph, k_n
    6. test complete graph, k_n
    7. test other graph by adj mat
    8. test
Number for layout: """))
            try:
                self.purpose = self.purposes[purpose_id - 1]
                result = True
            except ValueError:
                print("Invalid choice.")
                pass
        return self.purpose
    
    def get_offices_count(self):
        offices_count = int(input("Input the number of offices: "))
        return offices_count
        
    def manage_output(self):
        supervisor = Supervisor()
        supervisor.manage_input()
        supervisor.set_adj_mat()
        supervisor.initialize_offices()
        self.purpose = supervisor.office_layout_id

        if self.purpose == "c_n" or self.purpose == "deg3loop" or self.purpose == "k_n" or self.purpose == "other":
            supervisor.assign_forms()
            supervisor.assign_neighbors()
            reassignments = supervisor.stabilize()
            print(f"Number of {reassignments = }")
            print(f"Maximum number of firing nodes = {supervisor.firing_nodes_count}")
        elif self.purpose == "testdeg3loop":
            supervisor.test_stability_interval("deg3loop")
        elif self.purpose == "test_k_n":
            supervisor.test_stability_interval("k_n")
        elif self.purpose == "test_other":
            supervisor.test_stability_interval("other")
        elif self.purpose == "test":
            supervisor.test()
    
class Supervisor:
    def __init__(self):
        self.offices_count = 0
        self.offices = {}
        self.office_layout_id = ""
        self.new_offices = {}
        self.adj_matrix = [] 
        self.offices_count = 0
        self.prev_configurations = []
        self.cycle_configurations = []
        self.edges_list = []
        self.firing_nodes_count = 0
        self.new_firing_nodes_count = 0
        self.tikz_code = []
        self.iteration = 0

    def manage_input(self):
        pr = PublicRelations()
        self.office_layout_id = pr.get_purpose_id()
        self.offices_count = pr.get_offices_count()
        
    def set_adj_mat(self):
        self.adj_matrix = get_adj_mat(self.offices_count, self.office_layout_id)
        print("Adjacency matrix:")
        print(self.adj_matrix)

    def initialize_offices(self):
        for number in range(self.offices_count):
            self.offices[str(number + 1)] = Office(number + 1)
        
    def assign_forms(self, manually_input=True, initial_forms=0):
        forms_configuration_initial = []
        if manually_input == True:
            if self.office_layout_id == "c_n" or self.office_layout_id == "deg3loop":
                self.offices[str((self.offices_count + 1)//2)].forms_count = int(input("Input the number of forms in the single office: "))
            else:
                print("Input the forms per offices list: ")
                forms_configuration_initial = list(map(int, input().split()))
        elif manually_input == False:
            forms_configuration_initial = list(initial_forms if i == 0 else 0 for i in range(self.offices_count))
        for i in range(len(forms_configuration_initial)):
            self.offices[str(i + 1)].forms_count = forms_configuration_initial[i]
        self.current_configuration = self.get_current_config()

        forms_configuration_initial = tuple(forms_configuration_initial)

    def assign_neighbors(self):
        for i in range(self.offices_count):
            j = 0
            j += i
            while j < self.offices_count:
                if self.adj_matrix[i, j] == 1:
                    self.offices[str(i + 1)].neighbors.add(str(j + 1))
                    self.offices[str(j + 1)].neighbors.add(str(i + 1))
                j += 1
    
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
        offices_numbers_sorted = list(self.offices.keys())
        sorted_dict = {number: self.offices[number] for number in offices_numbers_sorted}
        for _, office in sorted_dict.items():
            forms_configuration.append(office.forms_count)
        forms_configuration = tuple(forms_configuration)

        return forms_configuration
        
    def distribute(self, to_draw=True):
        self.current_configuration = self.get_current_config()
        is_stable = True

        for _, office in self.offices.items():
            distribution_amount = office.forms_count // len(office.neighbors)
            if distribution_amount > 0:
                self.new_firing_nodes_count += 1
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

        if self.new_firing_nodes_count > self.firing_nodes_count:
            self.firing_nodes_count = self.new_firing_nodes_count

        self.prev_configurations.append(self.current_configuration)

        self.offices.update(self.new_offices)
        self.new_offices = {}
        self.new_firing_nodes_count = 0

        if to_draw == True:
            self.draw()
            print(self.current_configuration)
            # time.sleep(0.25)

        return is_stable

    def stabilize(self, to_draw=True):
        self.iteration = 0
        is_stable = self.distribute()
        while not is_stable:
            self.iteration += 1
            is_stable = self.distribute(to_draw)
        return self.iteration

    def get_labels_dict(self):
        labels_dict = {}
        for i in range(self.offices_count):
            labels_dict[i] = str(self.current_configuration[i])
        return labels_dict

    def draw(self):
        G = nx.from_numpy_matrix(self.adj_matrix)
        # pos = nx.shell_layout(G) # for complete and cycles
        # pos = nx.kamada_kawai_layout(G) # for cycles
        # pos = nx.spring_layout(G) # for three-regular
        pos = nx.spectral_layout(G) # tester
        weights = self.get_labels_dict()
        nx.draw_networkx(G, pos=pos, with_labels=False, node_color="#429aff", node_size=10000 / self.offices_count, font_size=10)
        nx.draw_networkx_labels(G, pos=pos, labels=weights, font_size=20, font_color="white") # Comment out for no labels
        plt.box(False)
        plt.margins(0.15)
        #plt.savefig(f"/pictures/loop_{int(self.offices_count)}.{self.iteration}_sunsetblue.png", bbox_inches="tight", dpi=300)
        plt.show()

    def test_stability_interval(self, graph_type):
        vertices_count = self.offices_count
        edge_count = get_edge_count(self.offices_count, graph_type, self.adj_matrix)
        for i in range(edge_count, 2 * edge_count - vertices_count + 1):
            self.assign_forms(manually_input=False, initial_forms=i)
            self.assign_neighbors()
            self.stabilize(to_draw=False)
    
    def test(self):
        vertices_count = self.offices_count
        edge_count = get_edge_count(self.offices_count, "other", self.adj_matrix)
        for i in range(edge_count, 2 * edge_count - vertices_count + 1):
            self.assign_forms(manually_input=False, initial_forms=i)
            self.assign_neighbors()
            self.stabilize(to_draw=False)

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
    pr = PublicRelations()
    pr.manage_output()
