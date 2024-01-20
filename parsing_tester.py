# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    parsing_tester.py                                  :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: tajavon <tajavon@student.42.fr>            +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/01/09 15:04:36 by tajavon           #+#    #+#              #
#    Updated: 2024/01/20 15:19:10 by tajavon          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import subprocess
import time
import os
import json

BHGREEN = "\033[1;92m"
BHMAG = "\033[1;95m"
BHWHITE = "\033[1;97m"
BHCYAN = "\033[1;96m"
BHRED = "\033[1;91m"
RESET = "\033[0m"

try:
	fd = open("config.json", "r")
	file = json.load(fd)

	cub_path = file["filepath"]
	map_directory = file["invalid_map_folder"]
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


def valgrind_exec():
	for map in get_invalid_maps():

		command = f'valgrind --leak-check=full --log-file=".tmp" {cub_path} {map}'

		mapname = map.split("/")[-1]
		mapfolder = map.split("/")[-2]
		print(f"{BHWHITE}Executing in {BHMAG}{mapfolder}{RESET} of :{RESET}{BHGREEN} {mapname}{RESET}")

		subprocess.run(command, shell=True)
		if (display_all == False):
			outputFreeAlloc = subprocess.run('cat .tmp | grep "total heap usage"' ,shell=True, capture_output=True)
			outputLeaksPossible = subprocess.run('cat .tmp | grep "All heap blocks"' ,shell=True, capture_output=True)
			if (leaksMsg in str(outputLeaksPossible.stdout)):
				print(f"{BHGREEN}NO LEAKS, OK !{RESET}")
			else:
				stats["nb_leaks"] += 1
				stats["map_leaks"].append([mapfolder, mapname])
				subprocess.run('cat .tmp', shell=True)
				print(f"{BHRED}SOME LEAKS FOUND, TEST FAILED !{RESET}")
		else:
			subprocess.run('cat .tmp', shell=True)
		subprocess.run("rm .tmp", shell=True)


def basic_exec():
	for map in get_invalid_maps():

		command = f"{cub_path} {map}"

		mapname = map.split("/")[-1]
		mapfolder = map.split("/")[-2]
		print(f"{BHWHITE}Executing in {BHMAG}{mapfolder}{RESET} of :{RESET}{BHGREEN} {mapname}{RESET}")

		output = subprocess.run(command, shell=True, capture_output=True)
		if (output.stderr.decode('utf-8') == ""):
			print(f"{BHGREEN}OK !{RESET}")
		else:
			print(f"{BHRED}ERROR, TEST FAILED !{RESET}")
		print(output.stdout.decode('utf-8'))


stats = {
	"nb_maps": 0,
	"nb_leaks": 0,
	"map_leaks": []
}

stats["nb_maps"] = len(get_invalid_maps())

subprocess.run("clear", shell=True)
print("=" * 50)
print(f"{BHCYAN}EXECUTING WITHOUT VALGRIND{RESET}")
print("=" * 50)
time.sleep(1.0)
basic_exec()
input("Press enter to continue...")
subprocess.run("clear", shell=True)
print("=" * 50)
print(f"{BHGREEN}EXECUTING WITH VALGRIND{RESET}")
print("=" * 50)
time.sleep(1.0)
valgrind_exec()

print("=" * 50)
print(f"{BHWHITE}SUMMARY{RESET}")
print(f"STATS : {stats['nb_leaks']} memory test failed on {stats['nb_maps']}")
for map in stats["map_leaks"]:
	print(f" - {BHWHITE}{map[0]}/{RESET}{BHRED}{map[1]}{RESET}")
