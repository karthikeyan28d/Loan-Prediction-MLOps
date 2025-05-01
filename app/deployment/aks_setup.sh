#!/bin/bash

# Set variables
RESOURCE_GROUP="ALY-6020-FinalProject"
CLUSTER_NAME="nbfi-loan-cluster"
ACR_NAME="nbfiloanacr"

echo "Creating Azure Kubernetes Service (AKS) Cluster..."

# Create AKS cluster
az aks create --resource-group $RESOURCE_GROUP --name $CLUSTER_NAME \
    --node-count 2 --enable-managed-identity --generate-ssh-keys --enable-addons monitoring

echo "Attaching Azure Container Registry (ACR)..."
# Attach ACR to AKS
az aks update --resource-group $RESOURCE_GROUP --name $CLUSTER_NAME --attach-acr $ACR_NAME

echo "Retrieving AKS Credentials..."
# Get credentials to connect to AKS cluster
az aks get-credentials --resource-group $RESOURCE_GROUP --name $CLUSTER_NAME

echo "AKS Cluster Setup Complete!"
