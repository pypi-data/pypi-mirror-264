from typing import Tuple
from .Terminal import color

RESET = color.RESET
fg = color.foreground
numberColor = RESET + fg.YELLOW
boolColor   = RESET + fg.LBLUE
stringColor = RESET + fg.LGREEN
quotesColor = RESET + fg.BOLD + fg.CYAN

def _f(x: object):
	if isinstance(x, str):
		quotes = '"' if not "\n" in x else '"""'
		return f"{quotesColor}{quotes}{stringColor}{x.replace("\"", "\\\"")}{quotesColor}{quotes}{RESET}"
	elif isinstance(x, (bool, type(None))):
		return f"{boolColor}{x}{RESET}"
	elif isinstance(x, (int, float)):
		return f"{numberColor}{x}{RESET}"
	return x

def _dictOut(_dict: dict, indentationLevel: int, indentationString: str) -> str:
	indent = indentationString * indentationLevel
	output = ""
	for k, v in _dict.items():
		if isinstance(v, (dict, list, tuple, set)):
			output += f"{indent}{_f(k)}: "
			output += _iterableOut(v, indentationLevel, indentationString, indentBefore=False)
		else:
			output += f"{indent}{_f(k)}: {_f(v)}\n"
	return output

def _listOut(_list: list, indentationLevel: int, indentationString: str) -> str:
	indent = indentationString * indentationLevel
	output = ""
	for item in _list:
		if isinstance(item, (dict, list, tuple, set)):
			output += _iterableOut(item, indentationLevel, indentationString)
		else:
			output += f"{indent}{_f(item)}\n"
	return output

def _tupleOut(_tuple: tuple, indentationLevel: int, indentationString: str) -> str:
	return _listOut(list(_tuple), indentationLevel, indentationString)

def _setOut(_set: set, indentationLevel: int, indentationString: str) -> str:
	return _listOut(list(_set), indentationLevel, indentationString)

def _callFunc(brackets: str, func: callable, iterable: dict | list | tuple | set, indentationLevel: int, indentationString: str, indentBefore: bool) -> str:
	indent = indentationString * indentationLevel
	return f"{indent if indentBefore else ""}{brackets[0]}\n{func(iterable, indentationLevel+1, indentationString)}{indent}{brackets[1]}\n"

def _iterableOut(iterable: dict | list | tuple | set, indentationLevel: int, indentationString: str, *, indentBefore: bool = True) -> str:
	output = ""
	if isinstance(iterable, dict):
		output += _callFunc("{}", _dictOut, iterable, indentationLevel, indentationString, indentBefore)
	elif isinstance(iterable, list):
		output += _callFunc("[]", _listOut, iterable, indentationLevel, indentationString, indentBefore)
	elif isinstance(iterable, tuple):
		output += _callFunc("()", _tupleOut, iterable, indentationLevel, indentationString, indentBefore)
	elif isinstance(iterable, set):
		output += _callFunc("{}", _setOut, iterable, indentationLevel, indentationString, indentBefore)
	else:
		raise ValueError(f"Invalid value given for 'iterable'!\nReceived type '{type(iterable)}', expected one of the following:\n[dict, list, tuple, set]")
	return output

def repr_iter(iterable: dict | list | tuple | set, *, indentationLevel: int = 0, indentationString: str = "  ") -> Tuple[str | None, Exception | None]:
	r"""Returns a string representation of the inputted iterable

	Returns a string representation of the inputted iterable with color coding per class using the Terminal.color class, 
	correct representation of string values and indentation for sub-iterables. 
	If a RecursionError occurs, it is returned as the second element, and the first element is None

	Parameters
	----------
	iterable: dict | list | tuple | set
		the iterable to be represented

	indentationLevel: int
		the level of indentation to start at
		DEFAULT: 0

	indentationString: str
		the string used for indentation
		DEFAULT: "  " (2 Spaces)
	"""
	
	try:
		output = _iterableOut(iterable, indentationLevel, indentationString)
		return output
	except RecursionError as e:
		return None, e