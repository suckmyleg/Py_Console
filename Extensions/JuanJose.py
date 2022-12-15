def start(t, c, m):

	def fun_(args):
		print(f"Luis se come {args} pollas")
		try:
			for i in range(int(args)):
				print("olo")
			return True
		except:
			return False

	t.add_command("juan_jose", fun_)
