import time
import subprocess

BHGREEN = "\033[1;32m"
BHYELLOW = "\033[1;33m"
BHWHITE = "\033[1;37m"
BHBLUE = "\033[1;34m"
BHCYAN = "\033[1;36m"
RESET = "\033[0m"

def display_signature():
	subprocess.run("clear", shell=True)
	with open("ascii_signature", "r") as f:
		for line in f:
			for char in line:
				if (char == "$"):
					print(f"{BHGREEN}${RESET}", end="")
				else:
					print(f"{BHWHITE}{char}{RESET}", end="")


if __name__ == "__main__":
	display_signature()
