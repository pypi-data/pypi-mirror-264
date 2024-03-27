import random

class foreground:
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'
	SWAPCOLOR = '\033[7m'
	BLACK = '\033[30m'
	RED = '\033[31m'
	GREEN = '\033[32m'
	YELLOW = '\033[33m'
	BLUE = '\033[34m'
	MAGENTA = '\033[35m'
	CYAN = '\033[36m'
	WHITE = '\033[37m'
	DEFAULT = '\033[39m'
	LBLACK = '\033[90m'
	LRED = '\033[91m'
	LGREEN = '\033[92m'
	LYELLOW = '\033[93m'
	LBLUE = '\033[94m'
	LMAGENTA = '\033[95m'
	LCYAN = '\033[96m'
	LWHITE = '\033[97m'

	colorList = [RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, DEFAULT, 
					LBLACK, LRED, LGREEN, LYELLOW, LBLUE, LMAGENTA, LCYAN, LWHITE]
	def random():
		return random.choice(foreground.colorList)