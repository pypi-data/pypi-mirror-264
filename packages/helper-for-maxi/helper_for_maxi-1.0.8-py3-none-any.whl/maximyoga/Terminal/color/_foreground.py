import random

class foreground:
	DEFAULT = '\033[0m'
	BOLD = '\033[1m'
	noBOLD = '\033[22m'
	UNDERLINE = '\033[4m'
	noUNDERLINE = '\033[24m'
	SWAPCOLOR = '\033[7m'
	noSWAPCOLOR = '\033[27m'
	FBLACK = '\033[30m'
	FRED = '\033[31m'
	FGREEN = '\033[32m'
	FYELLOW = '\033[33m'
	FBLUE = '\033[34m'
	FMAGENTA = '\033[35m'
	FCYAN = '\033[36m'
	FWHITE = '\033[37m'
	FDEFAULT = '\033[39m'
	FLBLACK = '\033[90m'
	FLRED = '\033[91m'
	FLGREEN = '\033[92m'
	FLYELLOW = '\033[93m'
	FLBLUE = '\033[94m'
	FLMAGENTA = '\033[95m'
	FLCYAN = '\033[96m'
	FLWHITE = '\033[97m'

	colorList = [DEFAULT, FRED, FGREEN, FYELLOW, FBLUE, FMAGENTA, FCYAN, FWHITE, FDEFAULT, 
					FLBLACK, FLRED, FLGREEN, FLYELLOW, FLBLUE, FLMAGENTA, FLCYAN, FLWHITE]
	def random():
		return random.choice(foreground.colorList)