# 🏗️ AWS Infrastructure Setup Guide

This document outlines the **step-by-step process** to provision a **secure**, **scalable**, and **highly available** AWS infrastructure using **VPC**, **Application Load Balancer (ALB)**, and **Auto Scaling Groups (ASG)**.

---

## 1. Create a Virtual Private Cloud (VPC)

- Define a custom **VPC** with an appropriate CIDR block, such as `10.0.0.0/16`.
- This VPC serves as the isolated network environment for all AWS resources.

---

## 2. Set Up an Internet Gateway (IGW)

- Create an **Internet Gateway** and attach it to the VPC.  
- This enables **outbound internet access** for resources in public subnets.

---

## 3. Create Subnets

- Provision **public** and **private** subnets across multiple **Availability Zones (AZs)** to ensure **high availability** and **fault tolerance**.

**Example:**
- **Public Subnets:** For internet-facing resources (e.g., ALB, bastion hosts).  
- **Private Subnets:** For backend services (e.g., EC2 instances, databases).

---

## 4. Create a Route Table

- Define a **Route Table** and associate it with the public subnets.  
- Add a route to the **Internet Gateway (IGW)** to enable outbound internet traffic.  
- **Private subnets** should route traffic internally (e.g., via **NAT Gateway** if needed).

---

## 5. Create Target Groups for EC2 Instances

- Define one or more **Target Groups** to register EC2 instances.  
- These target groups will be used by the **Application Load Balancer (ALB)** for traffic distribution.  
- Configure **health checks** for continuous monitoring of target health.

---

## 6. Create an Application Load Balancer (ALB)

- Provision an **Application Load Balancer (ALB)** within the VPC.  
- Configure **listeners** for HTTP (`port 80`) and/or HTTPS (`port 443`).  
- Attach previously created **Target Groups**.  
- Ensure the ALB spans multiple **Availability Zones (AZs)** for high availability.

---

## 7. Create a Security Group for the Auto Scaling Group

- Define a **Security Group** allowing necessary inbound and outbound traffic:

  **Inbound:**
  - HTTP (`80`)
  - HTTPS (`443`)
  - SSH (`22`) if needed

  **Outbound:**
  - Allow all for general internet access or restrict as per security policy.

- Apply **least privilege principles** when defining security rules.

---

## 8. Create an Auto Scaling Group (ASG)

- Launch the **Auto Scaling Group (ASG)** specifying:
  - **AMI ID** and **Instance Type**
  - **Subnets** (preferably across multiple AZs)
  - **Target Groups** (for load balancing)
  - **Security Groups**
  - **Desired Capacity**, **Minimum**, and **Maximum Instances**
  - **Scaling Policies** (e.g., scale out/in based on CPU utilization or custom CloudWatch metrics)

---

## 🛡️ Best Practices

### **Use IAM Roles**
- Assign IAM roles to EC2 instances and ASGs for secure access to AWS services without embedding credentials.

### **Principle of Least Privilege**
- Restrict IAM policies and Security Groups to only what is necessary.

### **Monitoring & Metrics**
- Enable **Amazon CloudWatch** monitoring for instance and application performance.  
- Configure **Auto Scaling policies** based on metrics such as CPU utilization or request count.

### **Network Security**
- Host backend services or databases in **private subnets**.  
- Enable **VPC Flow Logs** for network traffic analysis and troubleshooting.

### **High Availability**
- Deploy resources across **multiple Availability Zones (AZs)**.  
- Use **Health Checks** for ALB and ASG to ensure self-healing infrastructure.

---

## 📘 References

- [AWS VPC Documentation](https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html)  
- [AWS Elastic Load Balancing Documentation](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/introduction.html)  
- [AWS Auto Scaling Documentation](https://docs.aws.amazon.com/autoscaling/ec2/userguide/what-is-amazon-ec2-auto-scaling.html)

---
