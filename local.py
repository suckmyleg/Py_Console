class Local:
	def __init__(self):
		pass

	def input(self, *args):
		return input(*args)

	def print(self, *args):
		print(*args)
		return True