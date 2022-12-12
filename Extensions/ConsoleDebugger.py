from time import *

def start(t, c, m):

	def retryAndReloading(test):
		t.trigger_event("command_reload")
		for i in range(10):
			try:
				last_command = c.messages_sent[::-1][2+i]
				if last_command != "retry":
					c.print(f"> {last_command}")
					t.trigger_event("on_message", last_command)
					return True
			except:
				break
		return False

	def testTrigger(text):
		status = "Success"
		output = False
		startRecv = len(c.messages_recv)

		c.ableToPrint = False

		t.trigger_command("log", "true")

		start = time()
		try:
			datas = text.split(" ")
			event = datas[0]
			del datas[0]

			start = time()
			output = t.trigger_event(event, " ".join(datas))
		except:
			status = "Failed"
		end = time()

		t.trigger_command("log")

		c.ableToPrint = True

		printed = [" ".join([str(b) for b in list(a)]) for a in c.messages_recv[startRecv:len(c.messages_recv)]]

		if not output:
			status = "Failed"

		c.print(f"\nTest:\n  Timelapsed: {end-start}\n  Status: {status}\n  Output: {output}\n  Printed:")
		for p in printed:
			print(f"    - {p}")
		return True

	def testFun(text):
		return testTrigger(f"command_{text}")


	t.add_command("test", testFun)
	t.add_command("retry", retryAndReloading)
	t.add_command("testT", testTrigger)