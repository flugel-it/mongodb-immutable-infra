Feature: Test run_cmd

	@utils
	Scenario: Running echo command
		Given the command is "echo -n Hello"
		When executed the command
		Then received output "Hello"

	@utils
	Scenario: Running pwd command
		Given the command is "echo -n $(basename .)"
		When executed the command
		Then received output "."