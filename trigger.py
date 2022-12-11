from Debugger import *
from PluginsController import *

class TriggerBridge:
	def __init__(self, name, t):
		self.t = t
		self.logger = self.t.logger
		self.trigger_datas = self.t.trigger_datas
		self.plugins = self.t.plugins
		self.trigger_by = self.t.trigger_by
		self.plugin_name = name

	def whose_command(self, command):
		return self.t.whose_command(command)

	def add_listener(self, n, f):
		return self.t.add_listener(n, f, self.plugin_name)

	def add_command(self, n, f):
		return self.t.add_command(n, f, self.plugin_name)

	def trigger_command(self, n, *args):
		return self.t.trigger_command(n, self.plugin_name, *args)

	def trigger_event(self, n, *args):
		return self.t.trigger_event(n, self.plugin_name, *args)

class Trigger:
	def __init__(self):
		self.logger = Logger()
		self.errors = Errors(self.logger)
		self.plugins = Plugins(self.logger)

		self.data = {
		"on_error":[self.errors.add_error], 
		"on_extension_started":[self.plugins.add], 
		"on_extension_before_exporting":[], 
		"on_extension_imported":[], 
		"on_extension_before_loading":[]
		}

		self.calls_logs = {
		"on_error":[], 
		"on_extension_started":[], 
		"on_extension_before_exporting":[], 
		"on_extension_imported":[], 
		"on_extension_before_loading":[]
		}

		self.trigger_datas = {
		"on_error":[], 
		"on_extension_started":[], 
		"on_extension_before_exporting":[], 
		"on_extension_imported":[], 
		"on_extension_before_loading":[]
		}

		self.trigger_by = {}

	def add_command(self, command, fun, plugin_name):
		return self.add_listener(f"command_{command}", fun, plugin_name)

	def trigger_command(self, command, plugin_name, *args):
		return self.trigger_event(f"command_{command}", plugin_name, *args)

	def add_listener(self, event, fun, plugin_name):
		try:
			self.data[event].append(fun)
			self.logger.log("add", event, plugin_name)
		except:
			self.logger.log("creating", event, plugin_name)
			self.trigger_by[event] = plugin_name
			self.trigger_datas[event] = []
			self.calls_logs[event] = []
			self.data[event] = []
			self.add_listener(event, fun, plugin_name)

	def trigger_event(self, event, plugin_name, *args):
		try:
			for to_call in self.data[event]:
				self.logger.log("calling", event, plugin_name, self.whose_trigger(event))
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

	def whose_command(self, command_name):
		return self.whose_trigger(f"command_{command_name}")

	def whose_trigger(self, trigger_name):
		try:
			return self.trigger_by[trigger_name]
		except:
			return False