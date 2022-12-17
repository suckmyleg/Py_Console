class Errors:
	def __init__(self, logger, c):
		self.logger = logger
		self.errors = []
		self.c = c

	def add_error(self, args):
		self.errors.append(args)
		if self.logger.status:
			self.c.print(f"\nNew error:\n  - Code: {args[2]}\n  - Fun: {args[0]}\n  - Args: {args[1]}\n")

class Logger:
	def __init__(self, c):
		self.status = False
		self.c = c

	def log(self, action, event, plugin_name="Main", from_command="trigger"):
		if self.status:
			self.c.print(f"{plugin_name} => [{action}] {from_command}.{event}")