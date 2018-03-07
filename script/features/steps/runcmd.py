from lettuce import step, world

import utils


@step('the command is "(.*)"')
def get_command(step_instance, command):
	world.command = command


@step("executed the command")
def execute_command(step_instance):
	world.command_output = utils.run_cmd(world.command)


@step('received output "(.*)"')
def compare_the_output(step_instance, expected_output):
	assert world.command_output == expected_output, "Got \"{}\"".format(world.command_output)
