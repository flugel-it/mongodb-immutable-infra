Feature: Test run_cmd

	Scenario: Running echo command
		Given the command is "echo -n Hello"
		When executed the command
		Then received output "Hello"

	Scenario: Running pwd command
		Given the command is "echo -n $(basename .)"
		When executed the command
		Then received output "."