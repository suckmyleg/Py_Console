def start(t, c, m):

	def display_log(*args):
		c.print(*args)
		return None

	def display_logs(*args):
		c.print(t.trigger_datas["on_message"])

	def switch_log(*args):
		status = t.logger.status

		try:	
			if list(args)[0].lower() == "true":
				status = False
			elif list(args)[0].lower() == "false":
				status = True
		except:
			pass
			
		t.logger.status = not status

	t.add_command("print", c.print)
	t.add_command("logs", display_logs)
	t.add_command("log", switch_log)
	t.add_command("reload", m.import_plugins)