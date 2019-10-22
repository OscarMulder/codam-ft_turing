# **************************************************************************** #
#                                                                              #
#                                                         ::::::::             #
#    machine.py                                         :+:    :+:             #
#                                                      +:+                     #
#    By: omulder <omulder@student.codam.nl>           +#+                      #
#                                                    +#+                       #
#    Created: 2019/10/20 17:34:39 by omulder        #+#    #+#                 #
#    Updated: 2019/10/22 13:00:10 by omulder       ########   odam.nl          #
#                                                                              #
# **************************************************************************** #

class Tape:
	def __init__(self, tape_str, blank):
		self.blank = blank
		self.tape = dict((enumerate(tape_str)))

	def __getitem__(self, index):
		if index in self.tape:
			return self.tape[index]
		else:
			return self.blank
	
	def __setitem__(self, i, c):
		self.tape[i] = c
	
	def to_string_front(self, index):
		s = ""
		for i in range(0, index):
			s += self.tape[i]
		return s

	def to_string_back(self, index):
		s = ""
		for i in range(index, len(self.tape)):
			s += self.tape[i]
		return s

	def __str__(self):
		s = ""
		for key, value in self.tape:
			s += value
		return s

class Transitions:
	def __init__(self, name, transitions):
		self.name = name
		self.transitions = {}
		for transition in transitions:
			self.transitions[transition['read']] = transition

	def __getitem__(self, char):
		if (char in self.transitions):
			return self.transitions[char]
		else:
			return None

	def print_one(self, char):
		t = self.transitions[char]
		s = f"({self.name}, {t['read']}) -> ({t['to_state']}, {t['write']}, {t['action']})"
		return s
	
	def __str__(self):
		s = ""
		for t in self.transitions:
			s += "({name}, {read}) -> ({to_state}, {write}, {action})\n".format(
				name=self.name, read=self.transitions[t]['read'],
				to_state=self.transitions[t]['to_state'], write=self.transitions[t]['write'],
				action=self.transitions[t]['action'])
		return s

class Machine:
	'''Define the turing machine'''
	def __init__(self, jsonmachine, tape, to_print = True):
		self.check_jsonmachine(jsonmachine)
		self.name = jsonmachine['name']
		self.alphabet = jsonmachine['alphabet']
		self.blank = jsonmachine['blank']
		self.states = jsonmachine['states']
		self.current_state = jsonmachine['initial']
		self.finals = jsonmachine['finals']
		self.head = 0
		self.check_tape(tape)
		self.tape = Tape(tape, self.blank)
		self.transitions = {}
		for key in jsonmachine['transitions']:
			self.transitions[key] = Transitions(key, jsonmachine['transitions'][key])
		if to_print:
			print(self)
	
	def check_jsonmachine(self, jsonmachine):
		if not all(key in jsonmachine for key in ('name', 'alphabet', 'blank', 'states', 'initial', 'finals', 'transitions')):
			raise ValueError('Not all keys found in json file')
		for state in jsonmachine['states']:
			if not state in jsonmachine['transitions']:
				if not state in jsonmachine['finals']:
					raise ValueError(f"State: {state} not found in transitions table")
		if not jsonmachine['initial'] in jsonmachine['transitions']:
			raise ValueError(f"Initial state: {jsonmachine['initial']} not in transitions table")
	
	def check_tape(self, tape):
		if not all((c in self.alphabet) for c in tape):
			raise ValueError('Not all characters in tape are defined in alphabet')

	def set_print(self, cur_char, l):
		self.print = "["
		tmp = self.tape.to_string_front(self.head)
		if len(tmp) > l:
			tmp = tmp[-l]
		self.print += tmp
		self.print += "<" + cur_char + ">"
		tmp = self.tape.to_string_back(self.head + 1)
		if len(tmp) > l:
			tmp = tmp[l]
		self.print += tmp
		for i in range(len(self.print), (l * 2 + 4)):
			self.print += "."
		self.print += "] "
		self.print += self.transitions[self.current_state].print_one(cur_char)

	def __iter__(self):
		return self

	def __next__(self):
		if self.current_state in self.finals:
			raise StopIteration
		cur_char = self.tape[self.head]
		self.set_print(cur_char, 10)
		t = self.transitions[self.current_state][cur_char]
		if t != None:
			self.tape[self.head] = t['write']
			if t['action'] == "RIGHT":
				self.head += 1
			elif t['action'] == "LEFT":
				self.head -= 1
			else:
				pass
			self.current_state = t['to_state']
		else:
			raise StopIteration
		return self

	def __str__(self):
		stars = '*' * 80
		s = f"{stars}\nName\t: {self.name}\nAlphabet: {self.alphabet}\nInitial\t: {self.current_state}\nFinals\t: {self.finals}\n"
		for key in self.transitions:
			s += str(self.transitions[key])
		s += stars
		return s
