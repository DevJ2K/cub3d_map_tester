# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    parsing_tester.py                                  :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: tajavon <tajavon@student.42.fr>            +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/01/09 15:04:36 by tajavon           #+#    #+#              #
#    Updated: 2024/01/19 13:04:10 by tajavon          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import subprocess
import time
import os
import json

BHGREEN = "\033[1;92m"
BHMAG = "\033[1;95m"
BHWHITE = "\033[1;97m"
BHRED = "\033[1;91m"
RESET = "\033[0m"

try:
	fd = open("config.json", "r")
	file = json.load(fd)

	valgrind = file["valgrind"]
	wait_next_map = file["wait_between_try"]
	cub_path = file["filepath"]
	map_directory = file["invalid_map_path"]
	display_all = False

	fd.close()

except:
	print("Something went wrong when trying to get config.")
	exit (1)


leaksMsg = "All heap blocks were freed -- no leaks are possible"

def get_invalid_maps():
	all_invalid = []
	for directory in map_directory:
		for file in os.listdir(directory):
			if file.endswith('.cub'):
				all_invalid.append(f"{directory}/{file}")
	return (all_invalid)

subprocess.run("clear", shell=True)


def valgrind_exec():
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


def basic_exec():
	for map in get_invalid_maps():
		if (wait_next_map == True):
			subprocess.run("clear", shell=True)

		command = f"./{cub_path} {map}"

		mapname = map.split("/")[-1]
		mapfolder = map.split("/")[-2]
		print(f"{BHWHITE}Executing in {BHMAG}{mapfolder}{RESET} of :{RESET}{BHGREEN} {mapname}{RESET}")

		subprocess.run(command, shell=True)
	
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


if (valgrind):
	valgrind_exec()
else:
	basic_exec()
