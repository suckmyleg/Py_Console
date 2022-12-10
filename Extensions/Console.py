import os

def start(t, c, m):
	def triggers(*args):
		print("Triggers:")
		for trigger in t.trigger_datas.keys():
			print(" -", trigger) 

	def help(*args):
		print("Commands:")
		for trigger in t.trigger_datas.keys():
			if "command_"in trigger:
				print(" -", trigger.replace("command_", "")) 

	def plugins(*args):
		print("Plugins:")
		for p in t.plugins.imported:
			print(" -", p.Module_Name) 

	def who(*args):
		print(t.trigger_by[f"command_{list(args)[0]}"])

	t.add_command("help", help)
	t.add_command("triggers", triggers)
	t.add_command("execute", os.system)
	t.add_command("plugins", plugins)
	t.add_command("who", who)