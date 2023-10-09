class Trie:
	def __init__(self):
		"""
        This function initializes a trie with only the root node.

        Input:
            -
		
		Return:
			-

        Time complexity: O(1)
        Aux space complexity: O(1) 
        """
		self.root = Node(level=0)				# root node of the Trie, which is at level 0
		self.deepest_branch_node = self.root	# branch(of two strings) node with deepest level

	def suffix_insert(self, string, is_second_string):
		"""
        This function insert all the suffix of the string into the suffix tree.

        Input:
            string: the string to be inserted
			is_second_string: True if the string is second string, False if the string is first string
		Return:
			-

        Time complexity: O(N^2), where N denote the length of string.
        Aux space complexity: O(N^2), where N denote the length of string.
        """
		current = self.root																# current point to the root node
		for i in range(len(string)):													# for every suffix start from string[i]
			self.suffix_insert_aux(current, string, i, i+1, is_second_string)			# insert the suffix into tree

	def suffix_insert_aux(self, current, string, i, suffix_ID, is_second_string_suffix):
		"""
		Auxiliary function for suffix_insert

        Input:
        	current: pointer for the current node
            string: the string to be inserted
            i: pointer for the index of character in the suffix we are inserting 
            suffix_ID: the Id of the suffix we are inserting
			is_second_string_suffix: True if the string is a second string suffix, False if the string is first string suffix
		Return:
			-

        Time complexity: O(N), where N denote the length of string.
        Aux space complexity: O(N), where N denote the length of string.

		"""
		# base case
		if i == len(string):															# when we reach the end of the string
			index = 0 																	# $ is at index 0
			if current.link[index] is not None:											# if there is already a path
				current = current.link[index]											# update current

			else:																		# if there is no path yet
				current.link[index] = Node(level = current.level + 1)					# create a new code
				current.child_number += 1                                               # increment the child number of current node
				current = current.link[index]											# update current

				if current.child_number > 1:											# if current node is a branch node
					if is_second_string_suffix == True and current.first_string_suffix == True and current.level >= self.deepest_branch_node.level:
						self.deepest_branch_node = current								# update deepest_branch_node
			return

		# inductive case
		else:		
			index = ord(string[i]) - 97 + 1 											# calculate index of the character
			if index < 0:																# if the character is space
				index = 27																# space is at index 27

			if current.link[index] is not None:											# if there is already a path
				current= current.link[index]											# update current

				if is_second_string_suffix == False:									# if we are inserting the first string suffix
					current.first_string_suffix = True									# current node is a path of first string suffix

				if is_second_string_suffix == True and current.first_string_suffix == True and current.level >= self.deepest_branch_node.level:
					self.deepest_branch_node = current									# update deepest_branch_node

			else:
				current.link[index] = Node(level = current.level + 1)					# create a new code
				current.child_number += 1 												# increment the child_number of the node
				current = current.link[index]											# update current								
				
				if is_second_string_suffix == False:									# if we are inserting the first string suffix
					current.first_string_suffix = True									# current node is a path of first string suffix

				if current.child_number > 1:											# if current node is a branch node
					if is_second_string_suffix == True and current.first_string_suffix == True and current.level >= self.deepest_branch_node.level:
						self.deepest_branch_node = current								# update deepest_branch_node

			if current.suffix_ID_flag == False:											# if the current.suffix_ID have never been changed
				if is_second_string_suffix == True:										# if the string is second string suffix
					current.suffix_ID = suffix_ID 										# update current.suffix_ID
					current.suffix_ID_flag = True										# update the flag
			
			self.suffix_insert_aux(current, string, i+1, suffix_ID, is_second_string_suffix)	# recursively call the function, with i incremented by 1
	
	def compare_subs(self, submission1, submission2):
		"""
	    This function find longest common substring between submission1 and submission2, and also similarity score for submission1 and submission2.

	    Input: 
			submission1: string containing only characters in the range[a-z] or the space character
			submission2: string containing only characters in the range[a-z] or the space character
	    Return:
			[longest common substring between submission1 and submission2, the similarity score for submission1, the similarity score for submission2]

        Time complexity: O((N + M)^2), where M and N denote the length of strings submission1 and submission2, respectively.
        Aux space complexity: O((N + M)^2), where M and N denote the length of strings submission1 and submission2, respectively.
	    """
		self.suffix_insert(submission1, False)											# insert first string into suffix tree
		self.suffix_insert(submission2, True)											# insert second string into suffix tree

		start_index = self.deepest_branch_node.suffix_ID - 1
		end_index = start_index + self.deepest_branch_node.level
		length_common = end_index - start_index 

		if len(submission1) == 0:														# if submission1 is empty string
			similarity_s1 = 0  															# similarity score for submission1 would be 0
		else:
			similarity_s1 = self.rounding((length_common / len(submission1)) * 100) 	
			
		if len(submission2) == 0:														# if submission2 is empty string
			similarity_s2 = 0  															# similarity score for submission2 would be 0
		else:		
			similarity_s2 = self.rounding((length_common / len(submission2)) * 100) 

		return [submission2[start_index:end_index], similarity_s1, similarity_s2]

	def rounding(self, n):
		"""
		This function round the number to the nearest integer.
		0.5 --> 1
		1.4 --> 1
		1.45 --> 1
		1.55 --> 2

	    Input:
			n: a number
	    Return:
			rounded integer

	    Time complexity: O(1)
	    Space complexity: O(1)

		"""
		if n - math.floor(n) < 0.5:
			return math.floor(n)
		return math.ceil(n)

class Node:
	def __init__(self, size = 28, level = None):
		"""
	    This function is the constructor of Node

	    Input:
	        size: the size of character that can to be stored in the Node(Eg. a-z, size = 26)
	        level: level of node
	    Return:
	        -
	    Time complexity: O(1)
	    Space complexity: O(1)
	    """
		self.link = [None] * size					# terminal $ is at index 0, space is at index 27
		self.child_number = 0 						# number of child node
		self.level = level							# level of node, root node is at level 0						
		self.suffix_ID = 1                 	 		# the minimum id of the suffix(of the second string) which use the current node as path.
													# ** for string abc, suffix 1 = abc, suffix 2 = bc, suffix 3 = c 
		self.suffix_ID_flag = False					# True if suffix_ID have been changed before
		self.first_string_suffix = False			# True if the node is a path of first string suffix

def compare_subs(submission1, submission2):
	"""
    This function find longest common substring between submission1 and submission2, and also similarity score for submission1 and submission2.

    Input: 
		submission1: string containing only characters in the range[a-z] or the space character
		submission2: string containing only characters in the range[a-z] or the space character
    Return:
		[longest common substring between submission1 and submission2, the similarity score for submission1, the similarity score for submission2]

    Time complexity: O((N + M)^2), where M and N denote the length of strings submission1 and submission2, respectively.
    Aux space complexity: O((N + M)^2), where M and N denote the length of strings submission1 and submission2, respectively.
    """
	return Trie().compare_subs(submission1, submission2)