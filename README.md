# Instrumenting Kubernetes for Observability using AWS X-Ray and Amazon CloudWatch

The goal of this workshop is to demonstrate how to build and monitor modern applications with AWS Elastic Kubernetes Services (EKS), Amazon CloudWatch Logs and AWS X-Ray.

This workshop consists of 3 labs and will walk through the following:
1. **Lab 1**
   1. Prepare your environment
   2. Create an AWS EKS cluster with eksctl
   3. Deploy eCommerce microservices demo application
2. **Lab 2**
   1. Deploy a log aggregation stack
   2. Deploy metrics collection and visualization
3. **Lab 3**
   1. Deploy AWS X-Ray and enable tracing within the sample applications

> **Note**
>
> This workshops is an advanced workshop (Level 300) and requires a deep understanding of AWS capabilities as well as know-how in software development, containers, and Kubernetes.

# Application Architecture

The architecture of the application we will be deploying looks like this:

![alt Architecture](docs/images/architecture.png "Application architecture")

The services are either build in Node.js and the Express framework or Python with the Flask framework. As data store DynamoDB is used. To store the cart and the session data a self-hosted Redis is used. The orders are put into an SQS queue, where a worker process could pick them up for order-processing.

# Labs

## Prerequisites

[Prerequisites](docs/prerequisites.md)

## Lab 1 - Deploying microservices to Amazon EKS

[Deploying microservices on EKS](docs/lab1.md)

## Lab 2 - Observability for Amazon EKS
[Observability for EKS](docs/lab2.md)

## Lab 3 - Distributed Tracing with AWS X-Ray
[Adding distributed tracing](docs/lab3.md)

## Cleaning up
[Cleanup instructions](docs/cleanup.md)

## Troubleshooting

#### Cloud9 not connecting
Make sure the Cloud9 EC2 instances is running. Check that it has a **public** IP attached, otherwise the Browser-Component will not be able to connect.

If you can not get Cloud9 to work use a regular EC2 Linux instance to run the commands.

#### EKS cluster authentication failure
Make sure that you did not create the cluster with the AWS account root user. You have to use an IAM user when creating the EKS cluster.

Doublecheck that your `kubectl` version is at least version `1.10.0`, otherwise the integration with the IAM authenticator is not yet available causing authentication to fail.

Make sure that `aws-iam-authenticator` is installed and executable, so `kubectl` can call it when authenticating against the EKS cluster.

#### Load Balancer URL not accessible

When creating new services in Kubernetes it may take a while until the Elastic Load Balancer is created and becomes available. Also, propagation within DNS may take some additional time. If you can not access a newly created service please just wait a little while and then reload in your browser.

All load balancers are also visible in the EC2 Console -> Loadbalancers, check here for additional details.

#### Traces not visible

Make sure the X-Ray daemon is running successfully. Check the log output of the daemons to see if the permissions to send traces to AWS X-Ray have been set up correctly.

#### Long cluster spin up time
Creating the EKS cluster and node group should take around 10-15 minutes. If it takes longer `eksctl` will run into a timeout. Delete the cluster and simply try again.

#### Check ELB IAM role

In AWS accounts that have never created a load balancer before, it’s possible that the service role for ELB might not exist yet.

We can check for the role, and create it if it’s missing.

```bash
aws iam get-role --role-name "AWSServiceRoleForElasticLoadBalancing" || aws iam create-service-linked-role --aws-service-name "elasticloadbalancing.amazonaws.com"
```

#### Configure Storage Class

When using the latest version of `eksctl` a StorageClass will be automatically created.

Check if a StorageClass exists for your cluster with the command

```
kubectl get storageclasses
```

If you do not have a StorageClass installed the deployment of Prometheus and Grafana will fail.

Execute the command

```bash
kubectl create -f - <<EOF
{
  "kind": "StorageClass",
  "apiVersion": "storage.k8s.io/v1",
  "metadata": {
    "name": "prometheus",
    "namespace": "prometheus"
  },
  "provisioner": "kubernetes.io/aws-ebs",
  "parameters": {
    "type": "gp2"
  },
  "reclaimPolicy": "Retain",
  "mountOptions": [
    "debug"
  ]  
}
EOF
```

This will create a StorageClass in your Amazon EKS cluster.

# References & Acknowledgements
1. [Amazon EKS Workshop](https://eksworkshop.com/)
2. [Sockshop - Weaveworks](https://github.com/weaveworks)
3. [Google Microservices Demo](https://github.com/GoogleCloudPlatform/microservices-demo)

# License Summary
This sample code is made available under a modified MIT license. See the LICENSE file.
