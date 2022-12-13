import os
import socket
import pickle

def start(t, c, m):
	t.add_command("login", t.example_trigger)
	t.add_command("logout", t.example_trigger)

	t.add_command("follow", t.example_trigger)
	t.add_command("unfollow", t.example_trigger)

	t.add_command("get", t.example_trigger)