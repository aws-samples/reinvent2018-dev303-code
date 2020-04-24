# Cleanup

Before deleting your Amazon EKS cluster make sure to remove any deployed applications because some of them will deploy ELBs that will bind to the VPC that was created which will cause the VPC deletion to fail.

## Cleaning up microservices

Delete the microservices and Kubernetes resources from your cluster:

```bash
kubectl delete -f deploy/monitoring
kubectl delete -f deploy/tracing
kubectl delete -f deploy/services
kubectl delete -f deploy/eks
```

## Cleaning up Metrics collection with Prometheus

Next, delete Prometheus and Grafana using helm:

```bash
helm delete prometheus
helm del --purge prometheus
helm delete grafana
helm del --purge grafana
```

## Cleaning up AWS resources

Delete the EKS cluster

```
eksctl delete cluster --name dev303-workshop --region us-west-2
```

As last step delete the Cloud9 environment. Go to the Cloud9 dashboard (not the IDE) and remove the environment.

The cleanup process is now complete.