import os

def start(t, c, m):
	def triggers(args):
		args = args.replace(" ", "")
		c.print("Triggers:")
		for trigger in t.trigger_datas.keys():
			if (t.whose_trigger(trigger) == args or args == ""):
				c.print(" -", trigger)

		return True

	def help2(args):
		args = args.replace(" ", "")
		c.print("\nCommands(-d for more):")
		last = False
		for trigger in t.trigger_datas.keys():
			if not "on_" == trigger[:3] and ((len(args) > 0 and args[0] == "-") or (args in [""] or t.whose_trigger(trigger) == args or args == trigger.replace("command_", ""))):
				if len(args) > 0 and not args in ["-d", "-de", "-"]:# "-" == args[0]:
					now = t.whose_trigger(trigger)
					if now != last:
						if not last == False:
							c.print("")
						c.print(" +", now)
						last = now

				if (args in ["-d", "-de"]) or (not t.whose_trigger(trigger) == args and not args == ""):
					description = t.trigger_description(trigger)
					if args == "-d" or (args == "-de" and not description == "No description"):
						c.print("  -", trigger.replace("command_", ""), "<<", t.trigger_description(trigger))
					else:
						c.print("  -", trigger.replace("command_", ""))
				else:
					c.print("  -", trigger.replace("command_", ""))

		return True

	def help(args):
		args = args.replace(" ", "")
		c.print("\nCommands(-d for more):")
		last = False
		for trigger in t.trigger_datas.keys():
			if not "on_" == trigger[:3] and ((args in [""] or t.whose_trigger(trigger) == args[1:] or args == trigger.replace("command_", ""))):
				if len(args) > 0 and "-" == args[0]:
					now = t.whose_trigger(trigger)
					if now != last:
						if not last == False:
							c.print("")
						c.print(" +", now)
						last = now

				if (len(args) > 0 and args[0] != "-"):
					c.print("  -", trigger.replace("command_", ""), "<<", t.command_description(args))
				else:
					c.print("  -", trigger.replace("command_", ""))

		return True

	def plugins(*args):
		c.print("Plugins:")
		for p in t.plugins.imported:
			c.print(" -", p.Module_Name) 

		return True

	def who(text):
		c.print(t.whose_command(text.split(" ")[0]))

		return True

	def uknown_command(args):
		c.print(f"Uknown command: {args}")

		return True

	def line_empty(*args):
		c.print()

		return True

	def trigger_command(text):
		datas = text.split(" ")
		command = datas[0]
		del datas[0]

		if t.trigger_command(command, " ".join(datas)):
			t.trigger_event("on_command_executed", command)
		else:
			t.trigger_event("on_command_failed", command)

		return True

	def push(args):
		execute_cmd_command("git add *")
		execute_cmd_command(f"git commit -m '{args}'")
		execute_cmd_command("git push")

		return True

	def pull(args):
		execute_cmd_command("git pull")

		return True

	def reload_console(args):
		m.restart_triggers()
		if args.lower().replace(" ", "") == "true":
			t.t.logger.status = True
		m.import_plugins()

	def execute_cmd_command(*args):
		c.print(f"Executing command {args}")
		os.system(*args)
		return True


	t.add_listener("on_message", trigger_command)
	t.add_listener("on_command_executed", line_empty)
	t.add_listener("on_command_failed", uknown_command)
	t.add_command("help", help2, "Shows all commands from the plugins Params:(-d, -de, command, plugin_name)")
	t.add_command("triggers", triggers)
	t.add_command("execute", execute_cmd_command)
	t.add_command("plugins", plugins)
	t.add_command("pull", pull)
	t.add_command("push", push)
	t.add_command("who", who, "Display plugin where the command comes from")
	t.add_command("reload", reload_console, "Reload all plugins")