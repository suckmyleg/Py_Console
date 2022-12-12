import os
import socket
import threading
import pickle

def start(t, c, m):
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	connections = []

	status = "No connection"

	_host = "Null"

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

		threading.Thread(target=listenConnections).start()

		status = "Hosting"

	def main():
		while True:
			t.call_and_trigger("on_message_to_display", recvMessage, "Chatting", "Message: ")

	def recvMessage(*args):
		connection.recv(1024)

	def sendMessage(*args):
		connection.sendall(pickle.dumps(args))
		return True

	def getStatus(*args):
		if status == "No connection":
			c.print("No connection")
			return False

		c.print(f"{status} to {_host}")
		return True

	def chat(*args):
		host = getAddr(*args)
		if not host: return False
		c.print(f"Connecting to chat {host}")

		connection.connect((host, 8967))

		status = "Connected"

	def messageRecv(*args):
		print(args)

		username, message = args

		c.print(f"{username}: {message}")


	t.add_command("hostChat", hostChat)
	t.add_command("chat", chat)
	t.add_command("chatStatus", getStatus)
	t.add_listener("on_message", sendMessage)
	t.add_listener("on_message_to_display", messageRecv)
	
	#t.add_listener("on_extension_started", line_empty)