# mongodb-immutable-infra

Each folder has a README.md with the instructions about what you need to do.

the first code you need to execute is located in **s3** folder, as it is required to have the bucket created in order to save the remote terraform config.

Then you have to execute the code that it's located in **aws** folder. There you can find instructions to build the infrastructure where the cluster will run.

Then you should create the mongodb images in **mongodb/packer** folder and start the instances in **mongodb/terraform** folder.
