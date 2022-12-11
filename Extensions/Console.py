import os

def start(t, c, m):
	def triggers(*args):
		print("Triggers:")
		for trigger in t.trigger_datas.keys():
			print(" -", trigger) 

	def help(*args):
		print("Commands:")
		for trigger in t.trigger_datas.keys():
			if not "on_" == trigger[0:3]:
				print(" -", trigger.replace("command_", "")) 

	def plugins(*args):
		print("Plugins:")
		for p in t.plugins.imported:
			print(" -", p.Module_Name) 

	def who(text):
		print(t.whose_command(text.split(" ")[0]))

	def uknown_command(args):
		print(f"Uknown command: {args}")

	def line_empty(*args):
		print()

	def trigger_command(text):
		datas = text.split(" ")
		command = datas[0]
		del datas[0]

		if t.trigger_command(command, " ".join(datas)):
			t.trigger_event("on_command_executed", command)
		else:
			t.trigger_event("on_command_failed", command)

	t.add_listener("on_message", trigger_command)
	t.add_listener("on_command_executed", line_empty)
	t.add_listener("on_command_failed", uknown_command)
	t.add_command("help", help)
	t.add_command("triggers", triggers)
	t.add_command("execute", os.system)
	t.add_command("plugins", plugins)
	t.add_command("who", who)