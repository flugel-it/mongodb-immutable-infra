# Creating mongodb image

You have to create two images before start the cluster. By default, terraform will use CentOS, but you can change in terraform.tfvars (os_env) file.

First of all, we need to validate the template:

```
packer validate -var-file=mongodb-ubuntu-vars.json mongodb-ubuntu.json
packer validate -var-file=mongodb-centos-vars.json mongodb-centos.json
```

Then, to build a new image:
```
packer build -var-file=mongodb-ubuntu-vars.json mongodb-ubuntu.json
packer build -var-file=mongodb-centos-vars.json mongodb-centos.json
```

Terraform code will use the latest image created.
