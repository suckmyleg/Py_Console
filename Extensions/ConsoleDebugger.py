from time import *

def start(t, c, m):

	def testFun(text):
		start = time()
		status = "Success"
		output = None
		try:

			datas = text.split(" ")
			command = datas[0]
			del datas[0]

			output = t.trigger_command(command, " ".join(datas))
		except:
			status = "Failed"

		if not output:
			status = "Failed"

		c.print(f"\nTest:\n  Timelapsed: {time()-start}\n  Status: {status}\n  Output: {output}")
	t.add_command("test", testFun)