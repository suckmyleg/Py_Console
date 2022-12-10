from time import sleep

def start(t, c, m):

	def diamante(*args):
		print("Diamante pal friv")
		return 0

	def seducir(*args):
		print("Pero bueno, que te voy a seducir mariko mamawemo")
		return "Wtf"

	def ala(*alas):
		for i in range(int(list(alas)[0])):
			sleep(0.1)
			print("ala")

	t.add_command("ala", ala)
	t.add_command("diamante", diamante)
	t.add_command("seducir", seducir)