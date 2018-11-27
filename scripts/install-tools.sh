#
# Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this
# software and associated documentation files (the "Software"), to deal in the Software
# without restriction, including without limitation the rights to use, copy, modify,
# merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

#title           install-tools.sh
#description     This script will setup the Cloud9 IDE with the prerequisite packages and code for the workshop.
#author          @chrkas
#contributors    @buzzsurfr @dalbhanj @cloudymind
#date            2018-11-20
#version         0.1
#usage           curl -sSL https://s3.amazonaws.com/aws-tracing-workshop-artifacts/install-tools.sh | bash -s stable
#==============================================================================

# Install jq
sudo yum -y -q install jq

# Update awscli
pip install --user --upgrade awscli

# Install bash-completion
sudo yum install bash-completion -y -q

# Install kubectl
curl -o kubectl https://amazon-eks.s3-us-west-2.amazonaws.com/1.10.3/2018-06-05/bin/linux/amd64/kubectl
chmod +x kubectl && sudo mv kubectl /usr/local/bin/
echo "source <(kubectl completion bash)" >> ~/.bashrc

# Install Heptio Authenticator
curl -o aws-iam-authenticator https://amazon-eks.s3-us-west-2.amazonaws.com/1.10.3/2018-06-05/bin/linux/amd64/heptio-authenticator-aws
chmod +x ./aws-iam-authenticator && sudo mv aws-iam-authenticator /usr/local/bin/

# Configure AWS CLI
availability_zone=$(curl http://169.254.169.254/latest/meta-data/placement/availability-zone)
export AWS_DEFAULT_REGION=${availability_zone%?}

# Install eksctl
curl --silent --location "https://github.com/weaveworks/eksctl/releases/download/latest_release/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp
sudo mv /tmp/eksctl /usr/local/bin

# Install helm
curl "https://raw.githubusercontent.com/kubernetes/helm/master/scripts/get" > get_helm.sh
chmod +x get_helm.sh
./get_helm.sh

# Persist lab variables
echo "AWS_DEFAULT_REGION=$AWS_DEFAULT_REGION" >> ~/.bash_profile
echo "export AWS_REGION=${AWS_DEFAULT_REGION}" >> ~/.bash_profile
aws configure set default.region ${AWS_DEFAULT_REGION}
aws configure get default.region

# Create SSH key
ssh-keygen -t rsa -N "" -f ~/.ssh/id_rsa

if [ ! -d "reinvent2018-dev303-code/" ]; then
  # Download lab Repository
  git clone https://github.com/aws-samples/reinvent2018-dev303-code
fi