#!/bin/bash

# 1. Create image
docker buildx build --platform=linux/amd64 -t farmerselevator-image .
# 2. Push container to aws
aws lightsail push-container-image --region us-east-2 --service-name farmerselevator --label beta --image farmerselevator-image:latest
