import local

class Client:
	def __init__(self):
		self.messages_sent = []
		self.messages_recv = []

		self.ableToPrint = True

		self.reciever = local.Local()

	def input(self, *args):
		self.messages_sent.append(self.reciever.input(*args))
		return self.messages_sent[::-1][0]

	def print(self, *args):
		self.messages_recv.append(args)
		
		if self.ableToPrint:
			return self.reciever.print(*args)
		return False