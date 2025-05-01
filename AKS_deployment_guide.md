# **Azure Kubernetes Service (AKS) Deployment Guide**

This guide provides a **step-by-step process** to deploy a Flask-based loan prediction application on **Azure Kubernetes Service (AKS)**. It includes setting up **Azure Container Registry (ACR)**, **building a Docker image**, **deploying it to AKS**, and linking all necessary services.

---

## **🚀 Step 1: Set Up Azure Resources**

Before deploying, we need the following Azure services:

1. **Azure Kubernetes Service (AKS)**
2. **Azure Container Registry (ACR)**
3. **Azure Identity (Service Principal)**

### **1.1 Create a Resource Group**

```sh
az group create --name ALY-6020-FinalProject --location uksouth
```

### **1.2 Create an Azure Container Registry (ACR)**

```sh
az acr create --resource-group ALY-6020-FinalProject --name nbfiloanacr --sku Basic
```

Verify ACR:

```sh
az acr list --resource-group ALY-6020-FinalProject --output table
```

---

## **🚀 Step 2: Build and Push Docker Image to ACR**

### **2.1 Log in to ACR**

```sh
az acr login --name nbfiloanacr
```

### **2.2 Build the Docker Image**

```sh
docker build -t nbfiloanacr.azurecr.io/nbfi-loan-app:v1 .
```

### **2.3 Push Image to ACR**

```sh
docker push nbfiloanacr.azurecr.io/nbfi-loan-app:v1
```

### **2.4 Verify Image in ACR**

```sh
az acr repository list --name nbfiloanacr --output table
az acr repository show-tags --name nbfiloanacr --repository nbfi-loan-app --output table
```

---

## **🚀 Step 3: Deploy AKS Cluster**

### **3.1 Create AKS Cluster**

```sh
az aks create --resource-group ALY-6020-FinalProject --name nbfi-loan-cluster --node-count 2 --enable-managed-identity --enable-addons monitoring --generate-ssh-keys
```

### **3.2 Connect AKS to Local Machine**

```sh
az aks get-credentials --resource-group ALY-6020-FinalProject --name nbfi-loan-cluster
```

### **3.3 Verify Cluster is Running**

```sh
kubectl get nodes
```

---

## **🚀 Step 4: Grant AKS Access to ACR**

```sh
az aks update --resource-group ALY-6020-FinalProject --name nbfi-loan-cluster --attach-acr nbfiloanacr
```

Verify:

```sh
az aks show --resource-group ALY-6020-FinalProject --name nbfi-loan-cluster --query "servicePrincipalProfile.clientId" --output tsv
```

---

## **🚀 Step 5: Create Kubernetes Deployment & Service**

### **5.1 Create Deployment YAML (**``**)**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nbfi-loan-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: nbfi-loan-app
  template:
    metadata:
      labels:
        app: nbfi-loan-app
    spec:
      containers:
        - name: nbfi-loan-container
          image: nbfiloanacr.azurecr.io/nbfi-loan-app:v1
          ports:
            - containerPort: 5000
          envFrom:
            - secretRef:
                name: nbfi-env-secret
```

### **5.2 Create Service YAML (**``**)**

```yaml
apiVersion: v1
kind: Service
metadata:
  name: nbfi-loan-service
spec:
  type: LoadBalancer
  selector:
    app: nbfi-loan-app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 5000
```

### **5.3 Apply Deployment and Service**

```sh
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```

### **5.4 Verify Deployment and Service**

```sh
kubectl get deployments
kubectl get svc
```

---

## **🚀 Step 6: Add Environment Variables as Kubernetes Secret**

### **6.1 Create a Secret from **``** File**

```sh
kubectl create secret generic nbfi-env-secret --from-env-file=.env
```

### **6.2 Update Deployment to Use Secret**

```sh
kubectl apply -f deployment.yaml
kubectl rollout restart deployment nbfi-loan-app
```

---

## **🚀 Step 7: Verify and Debug**

### **7.1 Get Pods**

```sh
kubectl get pods
```

### **7.2 Check Pod Logs**

```sh
kubectl logs <POD_NAME>
```

### **7.3 Get External IP**

```sh
kubectl get svc nbfi-loan-service
```

Test in browser or via `curl`:

```sh
curl http://<EXTERNAL-IP>
```

---

## **🚀 Step 8: Scaling and Auto-Scaling**

### **8.1 Scale Manually**

```sh
kubectl scale deployment nbfi-loan-app --replicas=3
kubectl get pods
```

### **8.2 Enable Auto-Scaling**

```sh
kubectl autoscale deployment nbfi-loan-app --cpu-percent=50 --min=2 --max=5
kubectl get hpa
```

---

## **🎯 Summary of Commands**

| **Step**   | **Action**                   | **Command**                          |
| ---------- | ---------------------------- | ------------------------------------ |
| **Step 1** | Create ACR & Resource Group  | `az acr create`                      |
| **Step 2** | Build & Push Docker Image    | `docker build & docker push`         |
| **Step 3** | Create AKS Cluster           | `az aks create`                      |
| **Step 4** | Link AKS to ACR              | `az aks update --attach-acr`         |
| **Step 5** | Deploy Kubernetes Resources  | `kubectl apply -f`                   |
| **Step 6** | Secure Environment Variables | `kubectl create secret generic`      |
| **Step 7** | Verify & Debug               | `kubectl logs`, `kubectl get svc`    |
| **Step 8** | Scale & Auto-Scale           | `kubectl scale`, `kubectl autoscale` |

---

## **🎉 What’s Next?**

✅ **Your application is now running on Azure AKS with a Load Balancer!**\
**Next Steps:**

- **Implement CI/CD** using **GitHub Actions or Jenkins**
- **Enable Monitoring** using **Azure Monitor**
- **Add a Custom Domain** using **Azure DNS**
- **Set Up HTTPS** with **Azure Application Gateway**

🚀 **Congrats on the successful AKS deployment!** 🎯

