# **************************************************************************** #
#                                                                              #
#                                                         ::::::::             #
#    turing.py                                          :+:    :+:             #
#                                                      +:+                     #
#    By: omulder <omulder@student.codam.nl>           +#+                      #
#                                                    +#+                       #
#    Created: 2019/10/20 17:34:48 by omulder        #+#    #+#                 #
#    Updated: 2019/10/22 22:17:17 by omulder       ########   odam.nl          #
#                                                                              #
# **************************************************************************** #

import json
import sys
import machine
import argparse

def start_machine():
	parse = argparse.ArgumentParser(description='A small Turing machine interpreter')
	parse.add_argument('Machine_file', metavar='jsonfile', type=str, help='json description of the machine')
	parse.add_argument('Tape', metavar='input', type=str, help='input of the machine')
	args = parse.parse_args()

	try:
		with open(args.Machine_file) as file:
			string = file.read()
	except FileNotFoundError as e:
		print(f'Error opening jsonfile: {e}')
		sys.exit(1)

	try:
		obj = json.loads(string)
	except json.decoder.JSONDecodeError as e:
		print(f'Error decoding jsonfile: {e}')
		sys.exit(1)

	try:
		for step in machine.Machine(obj, args.Tape):
			print(step.print)
	except ValueError as e:
		print(f'Input error: {e}')
		sys.exit(1)

if __name__ == '__main__':
	start_machine()