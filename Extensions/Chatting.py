import os
import socket
import pickle

def start(t, c, m):
	SERVER = False

	CONNECTION = False

	connections = []

	def getAddr(*args):
		host = list(args)[0]
		if(len(host.split(".")) == 1 and host != "localhost"): 
			c.print("Incorrect address")
			return False
		_host = host
		return host

	def listenConnection(conn, addr):
		while True:
			data = pickle.loads(conn.recv(1024))
			for c in connections:
				if not c == conn:
					c.sendall(pickle.dumps([addr, data]))

	def listenConnections():
		while True:
			addr, conn = server.accept()
			connections.append(conn)

		threading.Thread(target=listenConnection, args=(conn, addr)).start()

	def hostChat(*args):
		host = getAddr(*args)
		if not host: return False
		c.print(f"Hosting chat {host}")

		server.bind((host, 8967))
		server.listen()

		t.create_thread(listenConnections)

		chat(*args)

		return True

	def main():
		while True:
			t.call_and_trigger("on_message_to_display", recvMessage, "Chatting", "Message: ")

	def recvMessage(*args):
		connection.recv(1024)

	def checkMessage(*args):
		if CONNECTION != False:
			return t.trigger_event("on_message_to_send", *args)
		return True

	def sendMessage(*args):
		if CONNECTION != False:
			connection.sendall(pickle.dumps(args))
		return True

	def getStatus(*args):
		if CONNECTION == False:
			c.print("No connection")
			return True

		c.print(f"Connected to {_host}")
		return True

	def chat(*args):
		host = getAddr(*args)
		if not host: return False
		c.print(f"Connecting to chat {host}")

		connection.connect((host, 8967))

	def messageRecv(*args):
		print(args)

		username, message = args

		c.print(f"{username}: {message}")


	t.add_command("hostChat", hostChat)
	t.add_command("chat", chat)
	t.add_command("chatStatus", getStatus)
	t.add_listener("on_message", checkMessage)
	t.add_listener("on_message_to_send", sendMessage)
	t.add_listener("on_message_to_display", messageRecv)
	
	#t.add_listener("on_extension_started", line_empty)