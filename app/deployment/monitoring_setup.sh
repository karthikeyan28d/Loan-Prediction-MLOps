#!/bin/bash

# Set variables
RESOURCE_GROUP="ALY-6020-FinalProject"
CLUSTER_NAME="nbfi-loan-cluster"
LOG_ANALYTICS_WORKSPACE="nbfi-loan-log-workspace"

echo "Setting up Azure Monitor for AKS..."

# Enable Azure Monitor for AKS
az aks enable-addons --resource-group $RESOURCE_GROUP --name $CLUSTER_NAME --addons monitoring

# Retrieve Log Analytics Workspace ID
WORKSPACE_ID=$(az monitor log-analytics workspace show --resource-group $RESOURCE_GROUP --workspace-name $LOG_ANALYTICS_WORKSPACE --query id --output tsv)

# Connect AKS to Log Analytics Workspace
az aks update --resource-group $RESOURCE_GROUP --name $CLUSTER_NAME --enable-addons monitoring --workspace-resource-id $WORKSPACE_ID

echo "Azure Monitor setup complete!"
