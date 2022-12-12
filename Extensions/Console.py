import os

def start(t, c, m):
	def triggers(args):
		args = args.replace(" ", "")
		c.print("Triggers:")
		for trigger in t.trigger_datas.keys():
			if (t.whose_trigger(trigger) == args or args == ""):
				c.print(" -", trigger) 

	def help(args):
		args = args.replace(" ", "")
		c.print("Commands:")
		for trigger in t.trigger_datas.keys():
			if not "on_" == trigger[0:3] and (t.whose_trigger(trigger) == args or args == ""):
				c.print(" -", trigger.replace("command_", "")) 

	def plugins(*args):
		c.print("Plugins:")
		for p in t.plugins.imported:
			c.print(" -", p.Module_Name) 

	def who(text):
		c.print(t.whose_command(text.split(" ")[0]))

	def uknown_command(args):
		c.print(f"Uknown command: {args}")

	def line_empty(*args):
		c.print()

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