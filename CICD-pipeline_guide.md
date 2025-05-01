# CI/CD Pipeline for AKS Deployment 🚀

## **Overview**
This document explains the **CI/CD pipeline setup** for deploying the Flask-based ML model to **Azure Kubernetes Service (AKS)** using **GitHub Actions**. The pipeline automates:
- **Building** the Docker image
- **Pushing** it to Azure Container Registry (ACR)
- **Deploying** it to AKS
- **Monitoring** the deployment

---

## **CI/CD Pipeline Flow**

### **1️⃣ Code Push to GitHub**
- Developers push changes to **GitHub Repository**.
- GitHub Actions **triggers the CI/CD workflow**.

### **2️⃣ Build & Push Docker Image**
- The pipeline builds the **Docker image** of the Flask app.
- Pushes it to **Azure Container Registry (ACR)**.

### **3️⃣ Deploy to AKS**
- Pulls the latest Docker image from **ACR**.
- Deploys it to the **AKS cluster**.

### **4️⃣ Monitor & Logging**
- Uses **Azure Monitor** for logging.
- Retrieves deployment logs from **kubectl**.

---

## **🔹 Files & Scripts in Pipeline**

### **1️⃣ GitHub Actions Workflow (`.github/workflows/deploy.yml`)**
This file automates the CI/CD pipeline.
```yaml
name: Deploy to AKS

on:
  push:
    branches:
      - main

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v2
      
      - name: Login to Azure
        run: az login --service-principal -u ${{ secrets.AZURE_CLIENT_ID }} -p ${{ secrets.AZURE_CLIENT_SECRET }} --tenant ${{ secrets.AZURE_TENANT_ID }}
      
      - name: Build Docker Image
        run: docker build -t nbfiloanacr.azurecr.io/nbfi-loan-app:${{ github.sha }} .
      
      - name: Push Docker Image to ACR
        run: |
          az acr login --name nbfiloanacr
          docker push nbfiloanacr.azurecr.io/nbfi-loan-app:${{ github.sha }}
      
      - name: Deploy to AKS
        run: |
          kubectl apply -f deployment/k8s_deployment.yaml
```

### **2️⃣ Kubernetes Deployment File (`deployment/deployment.yaml`)**
Defines **how the app runs on AKS**.
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
          image: nbfiloanacr.azurecr.io/nbfi-loan-app:latest
          ports:
            - containerPort: 5000
```

### **3️⃣ AKS Setup Script (`deployment/aks_setup.sh`)**
Automates **AKS creation & ACR attachment**.
```bash
az aks create --resource-group ALY-6020-FinalProject --name nbfi-loan-cluster --node-count 2 --enable-managed-identity --generate-ssh-keys
az aks update --resource-group ALY-6020-FinalProject --name nbfi-loan-cluster --attach-acr nbfiloanacr
```

### **4️⃣ Monitoring Setup (`deployment/monitoring_setup.sh`)**
Configures **Azure Monitor** for AKS.
```bash
az aks enable-addons --resource-group ALY-6020-FinalProject --name nbfi-loan-cluster --addons monitoring
```

---

## **🚀 How to Run the Pipeline**
### **1️⃣ Set Up GitHub Secrets**
Go to **GitHub → Repository → Settings → Secrets** and add:
- `AZURE_CLIENT_ID` (Service Principal ID)
- `AZURE_CLIENT_SECRET` (Secret Key)
- `AZURE_TENANT_ID` (Azure Tenant ID)
- `ACR_NAME` (Container Registry Name)
- `AKS_CLUSTER_NAME` (Cluster Name)

### **2️⃣ Push Code & Trigger CI/CD**
```bash
git add .
git commit -m "Deploying to AKS"
git push origin main
```

### **3️⃣ Check Deployment Status**
```bash
kubectl get pods
kubectl logs -f deployment/nbfi-loan-app
kubectl get services
```

---

## **📌 Summary**
✅ **Fully automated CI/CD pipeline** for AKS deployment.  
✅ **GitHub Actions** handles **Docker build, push & deploy**.  
✅ **Azure Monitor** tracks logs & metrics.  
✅ **AKS pulls latest ML model version** from **Azure ML Workspace**.


