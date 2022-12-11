import os

def start(t, c, m):
	triggers = [
	"on_extension_before_exporting",
	"on_extension_imported"
	]

	for trigger in triggers:
		t.add_listener(trigger, print)

	def line_empty(*args):
		print()
	
	t.add_listener("on_extension_started", line_empty)