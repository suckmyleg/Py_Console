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

	def log(self, action, event, plugin_name="Main", *args):
		if self.status:
			print(f" {plugin_name} - [{action}] ({event})")

class Plugins:
	def __init__(self, logger):
		self.imported = []
		self.runned = []
		self.logger = logger

	def add(self, plug):
		self.logger.log("imported", plug.Module_Name)
		self.imported.append(plug)

class Trigger:
	def __init__(self):
		self.logger = Logger()
		self.errors = Errors(self.logger)
		self.plugins = Plugins(self.logger)
		self.data = {"on_error":[self.errors.add_error], "on_extension_started":[self.plugins.add]}
		self.calls_logs = {"on_error":[], "on_extension_started":[]}
		self.trigger_datas = {"on_error":[], "on_extension_started":[]}
		self.trigger_by = {}

	def add_command(self, command, fun, plugin_name):
		return self.add_listener(f"command_{command}", fun, plugin_name)

	def trigger_command(self, command, plugin_name, *args):
		return self.trigger_event(f"command_{command}", plugin_name, *args)

	def add_listener(self, event, fun, plugin_name):
		try:
			self.logger.log("add", event, plugin_name, fun)
			self.data[event].append(fun)
		except:
			self.logger.log("creating", event, plugin_name, fun)
			self.trigger_by[event] = plugin_name
			self.trigger_datas[event] = []
			self.calls_logs[event] = []
			self.data[event] = []
			self.add_listener(event, fun, plugin_name)

	def trigger_event(self, event, plugin_name, *args):
		try:
			for to_call in self.data[event]:
				self.logger.log("calling", event, plugin_name, to_call)
				try:
					call_back = to_call(*args)
				except Exception as e:
					self.trigger_event("on_error", plugin_name, [to_call, args, e])
				else:
					self.calls_logs[event].append(call_back)
					self.trigger_datas[event].append(args)
			return True
		except Exception as e:
			self.trigger_event("on_error", plugin_name, ["trigger_event", args, e])

			return False

	def call_and_trigger(self, event, fun, plugin_name, *args):
		return self.trigger_event(event, plugin_name, fun(*args))

	def trigger_on_change(self, event, args):
		try:
			if not self.trigger_datas[event] == args:
				for i in range(len(args)):
					exists = False

					try:
						if self.trigger_datas[event][i] == args[i]:
							exists = True
					except:
						pass

					if not exists:
						self.trigger_event(event, args[i])
				self.trigger_datas[event] = args
		except:
			self.trigger_datas[event] = args
			return False