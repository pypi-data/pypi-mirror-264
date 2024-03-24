
import os
import re
import sys
import inspect
from typing import Callable, Optional

from .command import Command
from .utils import get_signature

class Interface:

	@classmethod
	def commands_list(cls, commands: list[Command]):
		toolname = os.path.basename(sys.argv[0]).rsplit(".", 1)[0]

		def view(c: Command):

			def docs_view() -> str:
				if docs := cls.__parse_doc(c.func.__doc__)[0]:
					return f"\n\t\t{"\n\t\t".join(docs)}"
				return ""

			return f"\t{", ".join(c.cmds)}{docs_view()}"

		print(f"\n{toolname} commands list:\n\n" + "\n".join(map(view, commands)) + "\n")

	@classmethod
	def command_usage(cls, command: Command):
		positionals, keyword, defaults, spec = get_signature(command.func)
		docs, args_docs = cls.__parse_doc(command.func.__doc__)

		def command_name_view() -> str:
			return command.cmds[0]

		def positionals_view() -> str:
			return " ".join(positionals)

		def keywords_list_view() -> str:
			return " ".join(f"[-{arg}]" for arg in keyword)

		def typehint_view(hint):
			if not hint:
				return ""
			if isinstance(hint, type):
				return "\t" + hint.__name__
			return f"\t{hint}"

		def default_value_view(arg: str):
			if arg not in defaults:
				return ""
			return f"\t[default: {defaults[arg]}]"

		def positional_description_view(arg: str) -> str:
			return f"{arg}{typehint_view(spec.annotations.get(arg))}\t" + "\n\t".join(args_docs.get(arg, []))

		def keyword_description_view(arg: str) -> str:
			def alias_view(alias: str):
				if len(alias) == 1:
					return f"-{alias}"
				return f"--{alias}"
			desc = " ".join(alias_view(alias) for alias, argument in command.aliases.items() if argument == arg)
			desc += typehint_view(spec.annotations.get(arg))
			if arg in args_docs:
				desc += f"\t{"\n\t".join(args_docs[arg])}"
			desc += default_value_view(arg)
			return "\t" + desc

		desc = f"Usage: {command_name_view()} {positionals_view()} {keywords_list_view()}"
		if docs:
			desc += f"\n\n\t{"\n\t".join(docs)}"
		if positionals:
			desc += "\n\n" + "\n".join(map(positional_description_view, positionals))
		if keyword:
			desc += "\n\nOptions:\n" + "\n".join(map(keyword_description_view, keyword))

		print("\n" + desc + "\n")

	@staticmethod
	def __parse_doc(doc: Optional[str]) -> tuple[list[str], dict[str, str | list[str]]]:
		"""Returns list of docs paragraphs and map of arguments to list of argument docs paragraphs"""
		if not doc:
			return [], {}
		doc = inspect.cleandoc(doc)
		desc = []
		roles = []

		lines = doc.splitlines()
		i = 0
		while i < len(lines):
			if match := re.match("^:([a-zA-Z]+) ?([^:]*): ?(.*)$", lines[i].strip()):
				role, arg, value = match.groups()
				indent = len(re.match(r"^(\s*)", lines[i]).group(0))
				content = [value]
				i += 1
				while i < len(lines) and len(re.match(r"^(\s*)", lines[i]).group(0)) > indent:
					content.append(lines[i].strip())
					i += 1
				roles.append({"name": role, "arg": arg, "content": content})
				continue
			elif not len(roles):
				desc.append(lines[i].strip())
			i += 1

		while desc and not desc[0]:
			desc.pop(0)
		while desc and not desc[-1]:
			desc.pop()

		return desc, {role["arg"]: role["content"] for role in roles if role["name"] == "param"}
