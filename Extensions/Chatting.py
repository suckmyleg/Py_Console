import os
import socket
import pickle

def start(t, c, m):


	class OnlineChatting:
		def __init__(self):
			self.SERVER = False

			self.CONNECTION = False

			self.connections = []

		def getAddr(self, *args):
			host = list(args)[0]
			if(len(host.split(".")) == 1 and host != "localhost"): 
				c.print("Incorrect address")
				return False
			_host = host
			return host

		def listenConnection(self, conn, addr):
			while True:
				data = pickle.loads(conn.recv(1024))
				for c in self.connections:
					if not c == conn:
						c.sendall(pickle.dumps([addr, data]))

		def listenConnections(self):
			while True:
				addr, conn = self.SERVER.accept()
				self.connections.append(conn)

			threading.Thread(target=self.listenConnection, args=(conn, addr)).start()

		def hostChat(self, *args):
			host = self.getAddr(*args)
			if not host: return False
			c.print(f"Hosting chat {host}")

			self.SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

			self.SERVER.bind((host, 8967))
			self.SERVER.listen()

			t.create_thread(self.listenConnections)

			self.chat(*args)

			return True

		def main(self):
			while True:
				t.call_and_trigger("on_message_to_display", self.recvMessage, "Chatting", "Message: ")

		def recvMessage(self, *args):
			self.CONNECTION.recv(1024)

		def checkMessage(self, *args):
			if self.CONNECTION != False:
				return t.trigger_event("on_message_to_send", *args)
			return True

		def sendMessage(self, *args):
			if self.CONNECTION != False:
				self.CONNECTION.sendall(pickle.dumps(args))
			return True

		def getStatus(*args):
			if self.CONNECTION == False:
				c.print("No connection")
				return True

			c.print(f"Connected to {_host}")
			return True

		def chat(self, *args):
			host = self.getAddr(*args)
			if not host: return False
			c.print(f"Connecting to chat {host}")

			self.CONNECTION = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

			self.CONNECTION.connect((host, 8967))

		def messageRecv(self, *args):
			c.print(args)

			username, message = args

			c.print(f"{username}: {message}")



	online = OnlineChatting()

	t.add_command("hostChat", online.hostChat)
	t.add_command("chat", online.chat)
	t.add_command("chatStatus", online.getStatus)
	t.add_listener("on_message", online.checkMessage)
	t.add_listener("on_message_to_send", online.sendMessage)
	t.add_listener("on_message_to_display", online.messageRecv)
	
	#t.add_listener("on_extension_started", line_empty)