import trigger
import Client

import importlib.util
import sys
import os
import threading


class Main:
	def __init__(self):
		self.t = trigger.Trigger()
		self.c = Client.Client()

	def main(self):
		while True:
			self.t.call_and_trigger("on_message", self.c.input, "Main", "> ")

	def import_plugins(self, *args):
		self.t = trigger.Trigger()

		Extensions = os.listdir("Extensions")

		Imported = []

		for extension in Extensions:
			if extension not in ["__pycache__"]:
				try:
					self.t.trigger_event("on_extension_before_exporting", "Main", extension)

					spec = importlib.util.spec_from_file_location(extension[:-3], f"Extensions\\{extension}")
					extension_imported = importlib.util.module_from_spec(spec)
					sys.modules[extension[:-3]] = extension_imported
					spec.loader.exec_module(extension_imported)
					self.t.trigger_event("on_extension_imported", "Main", extension_imported)
					extension_imported.Module_Name = extension[:-3]
					Imported.append(extension_imported)
				except:
					print("Error importing extension:",extension)

		for extension_imported in Imported:
			self.t.trigger_event("on_extension_before_loading", "Main", extension_imported)
			threading.Thread(target=extension_imported.start, args=(trigger.TriggerBridge(extension_imported.Module_Name, self.t), self.c, self)).start()
			self.t.trigger_event("on_extension_started", "Main", extension_imported)

m = Main()

m.import_plugins()

m.main()