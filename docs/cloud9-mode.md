## Cloud9 Setup

> Ad blockers, javascript disablers, and tracking blockers should be disabled for
> the cloud9 domain, or connecting to the workspace might be impacted.
>
> Make sure to actually copy values from the Cloud9 terminal, as there is no copy-on-select!

- Create a [Cloud9 Environment](https://us-west-2.console.aws.amazon.com/cloud9/home?region=us-west-2)
  - Select **Create environment**
- Name it **tracingworkshop**, and take all other defaults
- When it comes up, customize the environment by closing the **Welcome tab**
  and **Lower work area**, and opening a new **Terminal** tab in the main work area:
  ![c9before](images/c9before.png)

- Your workspace should now look like this:
  ![c9after](images/c9after.png)


## Set up Cloud9 IAM permissions
1. Follow [this deep link to create an IAM role with Administrator access.](https://console.aws.amazon.com/iam/home#/roles$new?step=review&commonUseCase=EC2%2BEC2&selectedUseCase=EC2&policies=arn:aws:iam::aws:policy%2FAdministratorAccess)
2. Confirm that **AWS service** and **EC2** are selected, then click **Next** to view permissions.
3. Confirm that **AdministratorAccess** is checked, then click **Next** to review.
4. Enter **tracingworkshop-admin** for the Name, and select **Create Role**
![createrole](images/createrole.png)

1. Follow [this deep link to find your Cloud9 EC2 instance](https://console.aws.amazon.com/ec2/v2/home?#Instances:tag:Name=aws-cloud9-tracingworkshop*;sort=desc:launchTime)
1. Select the instance, then choose **Actions / Instance Settings / Attach/Replace IAM Role**
![c9instancerole](images/c9instancerole.png)
1. Choose **tracingworkshop-admin** from the **IAM Role** drop down, and select **Apply**
![c9attachrole](images/c9attachrole.png)

>Cloud9 normally manages IAM credentials dynamically. This isn't currently compatible with
>the aws-iam-authenticator plugin, so we will disable it and rely on the IAM role instead.

- Return to your workspace and click the sprocket, or launch a new tab to open the Preferences tab
- Select **AWS SETTINGS**
- Turn off **AWS managed temporary credentials**
- Close the Preferences tab
![c9disableiam](images/c9disableiam.png)

- To ensure temporary credentials aren't already in place we will also remove
any existing credentials file:
```
rm -vf ${HOME}/.aws/credentials
```

- We should configure our aws cli with our current region as default:
```
export AWS_REGION="us-west-2"
echo "export AWS_REGION=${AWS_REGION}" >> ~/.bash_profile
aws configure set default.region ${AWS_REGION}
aws configure get default.region
```

# Install Tools

The necessary tooling can be installed using a script. Run:

```bash
git clone https://github.com/aws-samples/reinvent2018-dev303-code
cd reinvent2018-dev303-code
bash ./scripts/install-tools.sh
```

This will install all required tools and download the Github repository.

# Next Step

Back to [Prerequisites](prerequisites.md)