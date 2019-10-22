# **************************************************************************** #
#                                                                              #
#                                                         ::::::::             #
#    turing.py                                          :+:    :+:             #
#                                                      +:+                     #
#    By: omulder <omulder@student.codam.nl>           +#+                      #
#                                                    +#+                       #
#    Created: 2019/10/20 17:34:48 by omulder        #+#    #+#                 #
#    Updated: 2019/10/20 17:34:49 by omulder       ########   odam.nl          #
#                                                                              #
# **************************************************************************** #

import json
import sys
import machine

if len(sys.argv) == 2:
	if sys.argv[1] == "--help":
		pass
elif len(sys.argv) != 3:
	pass

file = open(sys.argv[1])
string = file.read()
obj = json.loads(string)
tape = sys.argv[2]
for step in machine.Machine(obj, tape):
	print(step.print)
