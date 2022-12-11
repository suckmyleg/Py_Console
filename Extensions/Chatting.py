import os

def start(t, c, m):
	def hostChat(*args):
		c.print()

	def chat(*args):
		c.print()

	def messageRecv(*args):
		username, message = args

		c.print(f"{username}: {message}")


	
	#t.add_listener("on_extension_started", line_empty)