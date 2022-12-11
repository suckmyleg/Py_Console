import local

class Client:
	def __init__(self):
		self.messages_sent = []
		self.messages_recv = []

		self.reciever = local.Local()

	def input(self, *args):
		return self.reciever.input(*args)

	def print(self, *args):
		return self.reciever.print(*args)