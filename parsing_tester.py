# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    parsing_tester.py                                  :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: tajavon <tajavon@student.42.fr>            +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/01/09 15:04:36 by tajavon           #+#    #+#              #
#    Updated: 2024/01/20 17:25:17 by tajavon          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import subprocess
import time
import os
import json
import display_signature

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
	print(cub_path)
	map_directory = file["invalid_map_folder"]
	display_all = False

	fd.close()
	display_signature.display_signature()
	time.sleep(1)

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
				print(f"{BHGREEN}NO LEAKS, OK !{RESET}", end="\n\n")
			else:
				stats["nb_leaks"] += 1
				stats["map_leaks"].append([mapfolder, mapname])
				subprocess.run('cat .tmp', shell=True)
				print(f"{BHRED}SOME LEAKS FOUND, TEST FAILED !{RESET}", end="\n\n")
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
		print(output.stdout.decode('utf-8'), end="")
		if (output.stderr.decode('utf-8') == ""):
			print(f"{BHGREEN}OK !{RESET}", end="\n\n")
		else:
			stats["nb_failed"] += 1
			stats["map_failed"].append([mapfolder, mapname])
			print(output.stderr.decode('utf-8'), end="")
			print(f"{BHRED}ERROR, TEST FAILED !{RESET}", end="\n\n")




stats = {
	"nb_maps": len(get_invalid_maps()),
	"nb_failed": 0,
	"nb_leaks": 0,
	"map_failed": [],
	"map_leaks": []
}

def display_stats(fails: int, nb_maps: int, maps_failed: list):
	print("\n" * 2)

	print(BHWHITE, end="")
	print("=" * 57)
	print("=" * 20, end="")
	print(RESET, end="")
	print(f"{' ' * 5}{BHCYAN}SUMMARY{' ' * 5}{RESET}", end="")
	print(BHWHITE, end="")
	print("=" * 20)
	print("=" * 57)
	print(RESET, end="")
	print("\n")

	if (fails == 0):
		print(f"{BHWHITE}STATS : {RESET}{BHGREEN}ALL TESTS PASSED !{RESET}")
		return
	elif (fails == 1):
		print(f"{BHWHITE}STATS : {RESET}{BHRED}{fails}{RESET} test failed on {BHRED}{nb_maps}{RESET} maps")
	else:
		print(f"{BHWHITE}STATS : {RESET}{BHRED}{fails}{RESET} tests failed on {BHRED}{nb_maps}{RESET} maps")


	for map in maps_failed:
		print(f" - {BHWHITE}{map[0]}/{RESET}{BHRED}{map[1]}{RESET}")
	print("\n")
	print(BHWHITE, end="")
	print("=" * 57)
	print(RESET, end="")

def main():
	# subprocess.run("clear", shell=True)
	print("=" * 50)
	print(f"{BHCYAN}EXECUTING WITHOUT VALGRIND{RESET}")
	print("=" * 50)
	time.sleep(1.5)
	basic_exec()

	display_stats(stats["nb_failed"], stats["nb_maps"], stats["map_failed"])

	input("Press enter to continue...")


	subprocess.run("clear", shell=True)

	print("=" * 50)
	print(f"{BHGREEN}EXECUTING WITH VALGRIND{RESET}")
	print("=" * 50)
	time.sleep(1.5)
	valgrind_exec()

	display_stats(stats["nb_leaks"], stats["nb_maps"], stats["map_leaks"])

	input("Press enter to exit...")
	subprocess.run("clear", shell=True)

if __name__ == "__main__":
	main();
