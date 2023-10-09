"""
assignment3.py
Name: Wong Chee Hao
Student ID: 32734751
e-mail: cwon0112@student.monash.edu
"""
import math

class Sharing_Meals:
	def __init__(self, availability):
		"""
	    This function build the flow network using adjacency list

	    Input:
	       	availability: a list of lists which contain the time availability of each person.
	    Return:
	        -
	    Time complexity: O(V+E), where V is the number of vertices in the flow network, E is the number of edges in the flow network
	    Space complexity: O(V+E), where V is the number of vertices in the flow network, E is the number of edges in the flow network
	    """
		self.person = 6 				 # 5 person + 1 restaurant
		self.day = len(availability)	 
		self.meal = 2 * self.day		 # 2 meal per day
		
		total_vertices = self.person + (self.day * self.person) + self.meal + 2 # 1 start and 1 end node, 6 person node, self.day day node for each person, self.meal meal node.

		# create array
		self.vertices = [None] * total_vertices

		# Add vertex to array
		for i in range(total_vertices):
			self.vertices[i] = Vertex(i)

		minimum_meal_person = math.floor(0.36 * self.day)		# lower bound for edges from start node to person node(exclude restaurant node)
		maximum_meal_person = math.ceil(0.44 * self.day)		# capacity for edges from start node to person node(exclude restaurant node)
		maximum_meal_restaurant = math.floor(0.1 * self.day)	# capacity for edges from start node to restaurant node

		# Add edges from start node to each person node(exclude restaurant node) 
		for i in range(1, 6):
			self.add_edge(0, i, maximum_meal_person, minimum_meal_person)

		# Add edge from start node to restaurant node
		self.add_edge(0, 6, maximum_meal_restaurant)

		# Add edges from person nodes to day nodes, and from day nodes to meal nodes
		for i in range(5):
			for j in range(self.day):
				if availability[j][i] != 0:
					self.add_edge(i+1, self.person + i * self.day + j + 1, 1, 0)
					if availability[j][i] == 1:
						self.add_edge(self.person + i * self.day + j + 1, self.person + self.person * self.day + (j*2) + 1, 1, 0)
					if availability[j][i] == 2:		
						self.add_edge(self.person + i * self.day + j + 1, self.person + self.person * self.day + (j*2) + 2, 1, 0)
					if availability[j][i] == 3:		
						self.add_edge(self.person + i * self.day + j + 1, self.person + self.person * self.day + (j*2) + 1, 1, 0)
						self.add_edge(self.person + i * self.day + j + 1, self.person + self.person * self.day + (j*2) + 2, 1, 0)

		# Add edges from restaurent to day node
		for i in range(self.day):
			self.add_edge(6, self.person + 5 * self.day + 1 + i, 2)

		# Add edges from day nodes to meal nodes
		for i in range(self.day):
			self.add_edge(self.person + 5 * self.day + 1 + i, self.person + self.person * self.day + (i*2) + 1, 2)
			self.add_edge(self.person + 5 * self.day + 1 + i, self.person + self.person * self.day + (i*2) + 2, 2)

		# Add edges from meal nodes to end nodes
		for i in range(self.person + self.person * self.day + 1, total_vertices - 1):
			self.add_edge(i, total_vertices - 1, 1, 1)

		# Add demand to start node and end node
		self.vertices[0].demand = -self.meal	# start node demand, total demand = -2n
		self.vertices[-1].demand = self.meal	# end node demand, total demand = 2n
	
	def add_edge(self, u, v, capacity, lowerbound = 0, flow = 0):
		"""
	    This function add forward_edge from u to v, add backward_edge from v to u, and add referece to the reversed edge.

	    Input:
	        u: u is the starting vertex id
	        v: is the ending vertex id
			capacity: the capacity of the edge
			lowerbound:	the lower bound of the edge
			flow: the flow of the edge
	    Return:
	        -
	    Time complexity: O(1)
	    Space complexity: O(1)
		"""
		# add u to v
		edge_u_to_v = Edge(u, v, capacity, lowerbound, flow)
		self.vertices[u].add_edge(edge_u_to_v)
		self.vertices[u].add_front_edge(edge_u_to_v)

		# add v to u
		edge_v_to_u = Edge(v, u, 0, lowerbound, 0)
		self.vertices[v].add_edge(edge_v_to_u)

		# add reference to their reverse edge
		edge_u_to_v.reverse = edge_v_to_u
		edge_v_to_u.reverse = edge_u_to_v

	def recursive_depth_first_search(self, source, sink, bottleneck):
		"""
	    This function do dfs to find an augmenting path. If found, update the flow and reverse flow, otherwise return 0

	    Input:
			source: starting node of dfs
			sink: ending node of dfs
			bottleneck:	use as a bottleneck
	    Return:
	    	augment: if there is an augmenting path, return the smallest flow of the augmenting path.
	        0: if there is no augmenting path
	    Time complexity: O(V+E), where V is the number of vertices in the flow network, E is the number of edges in the flow network
	    Aux Space complexity: O(1)
		"""
		# We hit the sink, so we have an augmenting path
		if source == sink:
			return bottleneck

		self.vertices[source].visited = True
		# start dfs
		for edge in self.vertices[source].edges:
		    residual = edge.capacity - edge.flow
		    if residual > 0 and self.vertices[edge.v].visited == False:		# if there is a path
		    	augment = self.recursive_depth_first_search(edge.v, sink, min(residual, bottleneck))	# move to the next node
		    	# We found an augmenting path - add the flow
		    	if augment > 0:
		        	edge.flow += augment
		        	edge.reverse.flow -= augment
		        	return augment

		# We could not find an augmenting path
		return 0 	

	def max_flow(self):
		"""
	    This function do the ford-fulkerson method to find the max flow of a flow network.

	    Input:
			-
	    Return:
	        maximum flow of the flow network

	    Time complexity: O(FE+FV), where F is the maximum flow, where V is the number of vertices in the flow network, E is the number of edges in the flow network
	    Aux Space complexity: O(1)
		"""

		# initialize flow
		max_flow = 0

		# initialize augment
		augment = math.inf

		while augment > 0:						# as long as there is a augmenting path
			# make all vertex unvisited
			for vertex in self.vertices:
				vertex.visited = False
			augment = self.recursive_depth_first_search(len(self.vertices)-2, len(self.vertices)-1, math.inf)
			max_flow += augment					# update the maximum flow

		return max_flow

	def allocate(self):
		"""
	    This function do the circulation with demands and lower bounds, to produce an allocation of preparing meals that satisfy all constraints.

	    Input:
			-
	    Return:
	        None: if there is no feasible solution, otherwise
	        (breakfast, dinner): lists breakfast and dinner specify a valid allocation, 
			** breakfast[i] = j if person numbered j is allocated to prepare breakfast on day i, otherwise breakfast[i] = 5 to denote that the breakfast will be ordered from a restaurant on that day.
			** Similarly for the dinner list

	    Time complexity: O(FE+FV), where F is the maximum flow, V is the number of vertices in the flow network, E is the number of edges in the flow network
	    Aux Space complexity: O(V+E), where V is the number of vertices in the flow network, E is the number of edges in the flow network
		"""

		total_negative_demand = 0 	# sum of all negative demand in the flow network
		total_positive_demand = 0   # sum of all positive demand in the flow network

		# eliminate lower bound of each edges(for each nodes: minus flow of incoming edges, plus flow of outgoing edges)
		for vertex in self.vertices:
			for edge in vertex.front_edges:
				self.vertices[edge.u].demand = self.vertices[edge.u].demand + edge.lowerbound	# PLUS OUTGOING
				self.vertices[edge.v].demand = self.vertices[edge.v].demand - edge.lowerbound	# MINUS INCOMING
				edge.capacity = edge.capacity - edge.lowerbound						# update the edge capcity

		# eliminate demand of each node
		self.vertices.append(Vertex(len(self.vertices)))							# source node
		self.vertices.append(Vertex(len(self.vertices)))							# sink node
		for i in range(len(self.vertices)):
			if self.vertices[i].demand < 0:											# if the node with negative demand
				total_negative_demand += self.vertices[i].demand
				self.add_edge(len(self.vertices)-2, i, -self.vertices[i].demand)	# link the source node to the negative demand nodes
				self.vertices[i].demand = 0 										# eliminate the demand
			
			elif self.vertices[i].demand > 0:										# if the node with positive demand
				total_positive_demand += self.vertices[i].demand
				self.add_edge(i, len(self.vertices)-1, self.vertices[i].demand)		# link the positive demand nodes to the sink node
				self.vertices[i].demand = 0 										# eliminate the demand

		# check feasibility 
		if -total_negative_demand != total_positive_demand:							# if total_negative_demand not equal to total_positive_demand
			return None

		# check feasibility with ford-folkerson
		max_flow = self.max_flow()

		# check feasibility 
		if max_flow != -total_negative_demand or max_flow != total_positive_demand:	# if the max_flow not equal to the total demands
			return None

		# initialize the list of allocation
		breakfast = [None] * self.day
		dinner = [None] * self.day

		# update the list of allocation by using the flow attribute of each day node
		for i in range(self.person + 1, self.person + self.person * self.day + 1):	# for each day node
			for edge in self.vertices[i].front_edges:								# for each edges from day node to meal node	
				if edge.flow > 0:													# if the flow > 0, means the person are allocated to the meal
					if edge.v % 2 == 0:												# if this is a dinner node
						dinner[(edge.v - self.person - (self.person * self.day + 1)) // 2] = (edge.u - self.person - 1) // self.day
					else:															# if this is a lunch node
						breakfast[(edge.v - self.person - self.person * self.day) // 2] = (edge.u - self.person - 1) // self.day

		return (breakfast, dinner)

class Vertex:
	def __init__(self, id):
		"""
	    This function is the constructor of Vertex

	    Input:
	        id: The label of vertex.
	    Return:
	        -
	    Time complexity: O(1)
	    Space complexity: O(1)
	    """
		self.id = id
		self.front_edges = []		# List to store all forward edges
		self.edges = []				# List to store all forward and backward edges
		self.demand = 0 			# the demand of nodes
		self.visited = False		# check if the nodes is visited during traversal

	def add_edge(self,edge):
		"""
	    This function append edge to the edges list

	    Input:
	        edge: Edge object
	    Return:
	        -
	    Time complexity: O(1)
	    Space complexity: O(1)
	    """
		self.edges.append(edge)

	def add_front_edge(self, edge):
		"""
	    This function append edge to the front_edges list

	    Input:
	        edge: Edge object
	    Return:
	        -
	    Time complexity: O(1)
	    Space complexity: O(1)
	    """
		self.front_edges.append(edge)

class Edge:
	def __init__(self, u, v, capacity, lowerbound = 0, flow = 0):
		"""
	    This function is the constructor for Edge object

	    Input:
	        u: u is the starting vertex id
	        v: is the ending vertex id
			capacity: the capacity of the edge
			lowerbound:	the lower bound of the edge
			flow: the flow of the edge
	    Return:
	        -
	    Time complexity: O(1)
	    Space complexity: O(1)
	    """
		self.u = u
		self.v = v
		self.capacity = capacity
		self.lowerbound = lowerbound
		self.flow = flow
		self.reverse = None		# reference to the reversed edge

def allocate(availability):
	"""
    This function return an allocation of preparing meals that satisfy all constraints.

    Input:
		-
    Return:
        None: if there is no feasible solution, otherwise
        (breakfast, dinner): lists breakfast and dinner specify a valid allocation, 
		** breakfast[i] = j if person numbered j is allocated to prepare breakfast on day i, otherwise breakfast[i] = 5 to denote that the breakfast will be ordered from a restaurant on that day.
		** Similarly for the dinner list

	Time complexity: O(NE+NV), where N is len(availability), V is the number of vertices in the flow network, E is the number of edges in the flow network
	Aux Space complexity: O(V+E), where V is the number of vertices in the flow network, E is the number of edges in the flow network
	"""
	return Sharing_Meals(availability).allocate()