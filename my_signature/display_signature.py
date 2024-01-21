import time
import subprocess

BHGREEN = "\033[7;32m"
BHYELLOW = "\033[1;33m"
BHWHITE = "\033[1;37m"
BHBLUE = "\033[1;34m"
BHCYAN = "\033[7;36m"
BHPINK = "\033[1;35m"
UNDERLINE = "\033[4;1;37m"
RESET = "\033[0m"

def display_signature():
	toggle = False
	subprocess.run("clear", shell=True)
	with open("my_signature/ascii_signature", "r") as f:
		for line in f:
			for char in line:
				if (char == "$"):
					print(f"{BHCYAN} {RESET}", end="")
				elif (char == "6"):
					toggle = True
					print(f" {UNDERLINE}", end="")
				elif (char == "7"):
					toggle = True
					print(f"{BHYELLOW} ", end="")
				elif (char == "8"):
					toggle = True
					print(f"{BHBLUE} ", end="")
				elif (char == "9"):
					toggle = True
					print(f"{BHPINK} ", end="")
				elif (char == ":"):
					toggle = False
					print(f":{RESET}{BHWHITE}", end="")
				else:
					if toggle == False:
						print(f"{BHWHITE}{char}{RESET}", end="")
					else:
						print(f"{char}", end="")



if __name__ == "__main__":
	display_signature()
