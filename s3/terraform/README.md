# Building a S3 bucket

The cluster run in a separated vpc/subnet.

You should export a bunch of env. variables before start terraform code.

```
export TF_VAR_customer="flugel"
export TF_VAR_aws_region="us-west-2"
```

**Note**: The bucket Name must be worlwide unique, please be aware of this. in case you need to change the bucket name, please go to **terraform.tfvars** and change bucket name variable.

> - **TF_VAR_customer**: The customer/client name
> - **TF_VAR_aws_region**: AWS region where the bucket will be created

Once these variables exported, you can init terraform:


```
terraform init
```

Then, check the plan of terraform changes:

```
terraform plan
```

And apply the changes:

```
terraform apply
```
