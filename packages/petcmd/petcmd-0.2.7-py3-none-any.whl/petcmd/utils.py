
import inspect
from typing import Callable

def get_signature(func: Callable):
	"""Returns positionals, keyword, defaults, spec"""
	spec = inspect.getfullargspec(func)
	positionals = spec.args if spec.defaults is None else spec.args[:-len(spec.defaults)]
	keyword = spec.kwonlyargs
	if spec.defaults is not None:
		keyword.extend(spec.args[-len(spec.defaults):])
	defaults = spec.kwonlydefaults or {}
	if spec.defaults is not None:
		defaults.update(dict(zip(spec.args[-len(spec.defaults):], spec.defaults)))
	return positionals, keyword, defaults, spec
