import subprocess

from lettuce import step, world


@step("server address is (.*)")
def get_address(st, address):
	world.address = address


@step("trying connect to server")
def try_to_connect(st):
	world.connected = ping(world.address)


@step("connection (is|is not) successful")
def check_connection(st, success):
	success = success == "is not"
	assert world.connected ^ success, "Connected is %s" % world.connected


def ping(host):
	return_code = subprocess.call(
		["/bin/ping", "-c", "1", "-W", "3", host],
		stdout=subprocess.PIPE,
		stderr=subprocess.PIPE
	)
	return return_code == 0
