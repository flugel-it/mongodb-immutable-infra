import subprocess


def run_cmd(cmd):
	"""
	runs a shell command
	:param cmd: shell command
	:return: output of the command
	"""
	process = subprocess.Popen(
		cmd,
		shell=True,
		stdin=subprocess.PIPE,
		stdout=subprocess.PIPE,
		stderr=subprocess.PIPE,
		close_fds=False
	)
	out, err = process.communicate()
	return out
