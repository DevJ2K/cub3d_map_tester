# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    parsing_tester.py                                  :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: tajavon <tajavon@student.42.fr>            +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/01/09 15:04:36 by tajavon           #+#    #+#              #
#    Updated: 2024/01/19 12:38:08 by tajavon          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import subprocess
import time
import os

BHGREEN = "\033[1;92m"
BHMAG = "\033[1;95m"
BHWHITE = "\033[1;97m"
BHRED = "\033[1;91m"
RESET = "\033[0m"

valgrind = True
wait_next_map = False
display_all = False

leaksMsg = "All heap blocks were freed -- no leaks are possible"

def get_invalid_maps():
	all_invalid = []
	map_directory = [
		'maps/invalid/basic_test',
		'maps/invalid/path',
		'maps/invalid/extra',
		'maps/invalid/colors'
	]
	for directory in map_directory:
		for file in os.listdir(directory):
			if file.endswith('.cub'):
				all_invalid.append(f"{directory}/{file}")
	return (all_invalid)

subprocess.run("clear", shell=True)

for map in get_invalid_maps():
	if (wait_next_map == True):
		subprocess.run("clear", shell=True)

	if (valgrind):
		command = f'valgrind --leak-check=full --log-file=".tmp" ./cub3d {map}'
	else:
		command = f"./cub3d {map}"
	mapname = map.split("/")[-1]
	mapfolder = map.split("/")[-2]
	print(f"{BHWHITE}Executing in {BHMAG}{mapfolder}{RESET} of :{RESET}{BHGREEN} {mapname}{RESET}")

	subprocess.run(command, shell=True)
	# output = subprocess.run(command, shell=True, capture_output=True)
	if (display_all == False):
		outputFreeAlloc = subprocess.run('cat .tmp | grep "total heap usage"' ,shell=True, capture_output=True)
		outputLeaksPossible = subprocess.run('cat .tmp | grep "All heap blocks"' ,shell=True, capture_output=True)
		if (leaksMsg in str(outputLeaksPossible.stdout)):
			print(f"{BHGREEN}TEST OK !{RESET}")
		else:
			print(f"{BHRED}TEST FAILED !{RESET}")
	else:
		subprocess.run('cat .tmp', shell=True)
	subprocess.run("rm .tmp", shell=True)
	if (wait_next_map == True):
		time.sleep(1.5)
