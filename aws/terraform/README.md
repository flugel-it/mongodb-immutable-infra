# Building a base infrastructure

The cluster run in a separated vpc/subnet. 

You should export a bunch of env. variables before start terraform code.

```
export TF_VAR_customer="flugel"
export TF_VAR_project_name="aws-vpc"
export TF_VAR_tf_region="us-west-2"
export TF_VAR_aws_region="us-west-2"
export TF_VAR_namespace="Cluster_Automation"
```

> - **TF_VAR_customer**: The customer/client name
> - **TF_VAR_project_name**: Terraform project name. That **must** be updated on each terraform folder
> - **TF_VAR_tf_region**: S3 region where you will store the tfstate
> - **TF_VAR_aws_region**: AWS region where the new vpc will be created
> - **TF_VAR_namespace**: Namespace of the project

Once these variables exported, you can init terraform:


```
terraform init \
    -backend-config="bucket=${TF_VAR_customer}-terraform-state" \
    -backend-config="key=${TF_VAR_project_name}/terraform.tfstate" \
    -backend-config="region=${TF_VAR_tf_region}"

```

Then, check the plan of terraform changes:

```
terraform plan
```

And apply the changes:

```
terraform apply
```

**NOTE**: You must to generate a public key of the AWS key and inform the path in terraform.tfvars file. To generate the public key:

```
ssh-keygen -y -f private_key.pem > public_key.pub
```
