import random

class background:
	DEFAULT = '\033[0m'
	SWAPCOLOR = '\033[7m'
	noSWAPCOLOR = '\033[27m'
	BBLACK = '\033[40m'
	BRED = '\033[41m'
	BGREEN = '\033[42m'
	BYELLOW = '\033[43m'
	BBLUE = '\033[44m'
	BMAGENTA = '\033[45m'
	BCYAN = '\033[46m'
	BWHITE = '\033[47m'
	BDEFAULT = '\033[49m'
	BLBLACK = '\033[100m'
	BLRED = '\033[101m'
	BLGREEN = '\033[102m'
	BLYELLOW = '\033[103m'
	BLBLUE = '\033[104m'
	BLMAGENTA = '\033[105m'
	BLCYAN = '\033[106m'
	BLWHITE = '\033[107m'

	colorList = [DEFAULT, BBLACK, BRED, BGREEN, BYELLOW, BBLUE, BMAGENTA, BCYAN, BWHITE,
					BDEFAULT, BLBLACK, BLRED, BLGREEN, BLYELLOW, BLBLUE, BLMAGENTA, BLCYAN, BLWHITE]

	def random() -> str:
		return random.choice(background.colorList)