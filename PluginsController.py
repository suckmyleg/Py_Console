class Plugins:
	def __init__(self, logger):
		self.imported = []
		self.runned = []
		self.logger = logger

	def add(self, plug):
		self.logger.log("imported", plug.Module_Name)
		self.imported.append(plug)