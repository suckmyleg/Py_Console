class Errors:
	def __init__(self, logger):
		self.logger = logger
		self.errors = []

	def add_error(self, args):
		self.errors.append(args)
		if self.logger.status:
			print(f"\nNew error:\n  - Code: {args[2]}\n  - Fun: {args[0]}\n  - Args: {args[1]}\n")

class Logger:
	def __init__(self):
		self.status = False

	def log(self, action, event, plugin_name="Main", from_command="trigger"):
		if self.status:
			print(f" {plugin_name} => [{action}] {from_command}.{event}")