# Prerequesites
 - Stable Packer Installation

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
**Note**: to build the Centos Image, you need to subscribe your account into the aws centos subscription. Go to the link the error shows and continue to subscribe to Centos.

Terraform code will use the latest image created.
