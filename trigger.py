from Debugger import *
from PluginsController import *
import threading

class TriggerBridge:
	def __init__(self, name, t):
		self.t = t
		self.logger = self.t.logger
		self.trigger_datas = self.t.trigger_datas
		self.plugins = self.t.plugins
		self.trigger_by = self.t.trigger_by
		self.plugin_name = name

	def create_thread(self, target, args=()):
		return self.t.create_thread(target, self.plugin_name, args)

	def whose_trigger(self, trigger):
		return self.t.whose_trigger(trigger)

	def whose_command(self, command):
		return self.t.whose_command(command)

	def command_description(self, command):
		return self.t.command_description(command)

	def trigger_description(self, trigger):
		return self.t.trigger_description(trigger)

	def add_listener(self, n, f, description="No description"):
		return self.t.add_listener(n, f, self.plugin_name, description)

	def add_command(self, n, f, description="No description"):
		return self.t.add_command(n, f, self.plugin_name, description)

	def trigger_command(self, n, *args):
		return self.t.trigger_command(n, self.plugin_name, *args)

	def trigger_event(self, n, *args):
		return self.t.trigger_event(n, self.plugin_name, *args)

	def example_trigger(self, *args):
		print("Being developed!")
		return True

class Trigger:
	def __init__(self, c):
		self.c = c
		self.logger = Logger(self.c)
		self.errors = Errors(self.logger, self.c)
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

		self.descriptions = {}

	def create_thread(self, target, plugin_name, args=()):
		self.logger.log("calling", "create_thread", plugin_name)
		threading.Thread(target=target, args=args).start()

	def add_command(self, command, fun, plugin_name, description="No description"):
		return self.add_listener(f"command_{command}", fun, plugin_name, description)

	def trigger_command(self, command, plugin_name, *args):
		return self.trigger_event(f"command_{command}", plugin_name, *args)

	def add_listener(self, event, fun, plugin_name, description="No description"):
		try:
			self.data[event].append(fun)
			self.logger.log("add", event, plugin_name)
		except:
			self.logger.log("creating", event, plugin_name)
			self.trigger_by[event] = plugin_name
			self.descriptions[event] = description
			self.trigger_datas[event] = []
			self.calls_logs[event] = []
			self.data[event] = []
			self.add_listener(event, fun, plugin_name)

	def trigger_event(self, event, plugin_name, *args):
		status = True
		try:
			call_back = "Nothing returned"
			for to_call in self.data[event]:
				self.logger.log("calling", event, plugin_name, self.whose_trigger(event))
				try:
					call_back = to_call(*args)
				except Exception as e:
					call_back = "Nothing returned"
					status = f"Plugin: {self.whose_trigger(event)} Error: {e}"
					self.trigger_event("on_error", plugin_name, [to_call, args, e])
				else:
					self.calls_logs[event].append(call_back)
					self.trigger_datas[event].append(args)

			if call_back == False:
				return False
			return status
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

	def trigger_description(self, event):
		return self.descriptions[event]

	def command_description(self, command_name):
		return self.trigger_description(f"command_{command_name}")

	def whose_command(self, command_name):
		return self.whose_trigger(f"command_{command_name}")

	def whose_trigger(self, trigger_name):
		try:
			return self.trigger_by[trigger_name]
		except:
			return False