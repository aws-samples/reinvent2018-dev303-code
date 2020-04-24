## Manual Setup

## AWS CLI

> For this workshop, please ignore warnings about the version of pip being used.

1. Run the following command to view the current version of aws-cli:

```
aws --version
```

2. Update to the latest version:

## Install eksctl
Install eksctl per instructions from [eksctl.io](https://eksctl.io)

```bash
$ curl --silent --location "https://github.com/weaveworks/eksctl/releases/download/latest_release/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp
sudo mv /tmp/eksctl /usr/local/bin
```

Mac users can also use Homebrew to install eksctl
`brew install weaveworks/tap/eksctl`

Windows users can download the binary from here https://github.com/weaveworks/eksctl/releases/

## Fetch source code

Clone the Github repository

```
git clone https://github.com/aws-samples/reinvent2018-dev303-code
```

## Install Kubernetes tooling

Amazon EKS clusters require kubectl and the aws-iam-authenticator
binary to allow IAM authentication for your Kubernetes cluster.

Follow the instructions [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/) to install kubectl on your machine.

### Verify installation
To verify that both tools are installed successfully run the commands

```
$ eksctl version
$ kubectl version --short --client
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