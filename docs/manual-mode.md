## Manual Setup

## AWS CLI

> For this workshop, please ignore warnings about the version of pip being used.

1. Run the following command to view the current version of aws-cli:

```
aws --version
```

1. Update to the latest version:

```
pip install --user --upgrade awscli
```

1. Confirm you have a newer version:

```
aws --version
```

## Fetch source code

Clone the Github repository

```
git clone https://github.com/aws-samples/reinvent2018-dev303-code
```

## Install Kubernetes tooling

Amazon EKS clusters require kubectl and kubelet binaries and the aws-iam-authenticator
binary to allow IAM authentication for your Kubernetes cluster.

### Create the default ~/.kube directory for kubectl configuration
```
mkdir -p ~/.kube
```

### Install kubectl
**Mac**
```
curl --silent --location -o /usr/local/bin/kubectl "https://amazon-eks.s3-us-west-2.amazonaws.com/1.10.3/2018-07-26/bin/darwin/amd64/kubectl"
chmod +x /usr/local/bin/kubectl
```
>Mac users may install kubectl using homebrew using the command `brew install kubernetes-cli`.

**Windows**
```
curl -o kubectl.exe https://amazon-eks.s3-us-west-2.amazonaws.com/1.10.3/2018-07-26/bin/windows/amd64/kubectl.exe
```
Copy the binary to a folder in your PATH. If you have an existing directory in your PATH that you use for command-line utilities, copy the binary to that directory.

**Linux**
```
curl --silent --location -o /usr/local/bin/kubectl "https://amazon-eks.s3-us-west-2.amazonaws.com/1.10.3/2018-07-26/bin/linux/amd64/kubectl"
chmod +x /usr/local/bin/kubectl
```

### Install AWS IAM Authenticator
Download the AWS IAM Authenticator binary for your operating system
Linux: https://amazon-eks.s3-us-west-2.amazonaws.com/1.10.3/2018-07-26/bin/linux/amd64/aws-iam-authenticator

```
# For Linux
sudo curl --silent --location -o /usr/local/bin/aws-iam-authenticator "https://amazon-eks.s3-us-west-2.amazonaws.com/1.10.3/2018-07-26/bin/linux/amd64/aws-iam-authenticator"
sudo chmod +x /usr/local/bin/aws-iam-authenticator
```

MacOS: https://amazon-eks.s3-us-west-2.amazonaws.com/1.10.3/2018-07-26/bin/darwin/amd64/aws-iam-authenticator

```
# For OSX
curl --silent --location -o /usr/local/bin/aws-iam-authenticator "https://amazon-eks.s3-us-west-2.amazonaws.com/1.10.3/2018-07-26/bin/darwin/amd64/aws-iam-authenticator"
chmod +x /usr/local/bin/aws-iam-authenticator
```

Windows: https://amazon-eks.s3-us-west-2.amazonaws.com/1.10.3/2018-07-26/bin/windows/amd64/aws-iam-authenticator.exe


### Verify installation
To verify that both tools are installed successfully run the commands

```
$ kubectl version --short --client
$ aws-iam-authenticator help
```

## Install eksctl
Install eksctl per instructions from [eksctl.io](https://eksctl.io)

```bash
$ curl --silent --location "https://github.com/weaveworks/eksctl/releases/download/latest_release/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp
sudo mv /tmp/eksctl /usr/local/bin
```

Mac users can also use Homebrew to install eksctl
`brew install weaveworks/tap/eksctl`

Windows users can download the binary from here https://github.com/weaveworks/eksctl/releases/download/0.1.11/eksctl_Windows_amd64.zip

### Verify installation

Confirm your eksctl version is at least `0.1.11` with the command
```bash
eksctl version
```

### Install `helm`

To quickly deploy applications such as Prometheus or Grafana to a Kubernetes cluster helm can be used. It's a package manager for Kubernetes applications. We'll need to install the command line tools first, that you will interact with. To do this run the following.

```bash
curl "https://raw.githubusercontent.com/kubernetes/helm/master/scripts/get" > get_helm.sh

chmod +x get_helm.sh

./get_helm.sh
```

Make sure that helm is installed by running
```
helm version
```

### Create SSH Key

By default **eksctl** uses the **~/.ssh/id_rsa** SSH key. If this does not exist on your machine you can create it with 

```
ssh-keygen
```

Press enter 3 times to generate the key. This key is necessary if you want to log in to the EKS worker nodes.

## Install Docker
Ensure you have Docker installed if you want to rebuild the container images in the workshop.

If you're running the workshop on your own machine download Docker from [Docker.com](https://www.docker.com) for your operating system and follow the installation instructions to install.

Check if Docker is installed successfully with

```bash
docker --version
```



# Next Step

Back to [Prerequisites](prerequisites.md)