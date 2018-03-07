# Deploying MongoDB with Ansible on Ubuntu


```
ansible-playbook \
	-i "host.address," \
	--private-key ~/path/to/your/key.pem \
	-e 'ansible_python_interpreter=/usr/bin/python3' \
	playbook.yml
```
