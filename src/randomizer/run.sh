#!/bin/bash
set -e
trap "exit" TERM

#!/bin/bash
while true
do
	kubectl get pods --selector product=storefront -o name -n microservices-aws | shuf | head -1 | xargs kubectl delete

    sleep $(shuf -i 60-90 -n 1)
done