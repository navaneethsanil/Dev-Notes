## 🏗️ Step-by-Step Setup Guide

### 1. Create a Virtual Private Cloud (VPC)
Define a custom VPC with an appropriate CIDR block (e.g., `10.0.0.0/16`).


### 2. Set Up an Internet Gateway (IGW)
Create and attach an Internet Gateway to the VPC for outbound internet access.


### 3. Create Subnets
Provision **public** and **private** subnets across multiple Availability Zones (AZs) to achieve **high availability** and **fault tolerance**.


### 4. Create a Route Table
Define a route table and associate it with the public subnets.  
Add a route to the Internet Gateway to allow outbound internet traffic.


### 5. Create Target Groups for EC2 Instances
Define one or more target groups that will register EC2 instances and be used by the **ALB** for routing traffic.


### 6. Create an Application Load Balancer (ALB)
Provision an **Application Load Balancer** within the VPC, configure listeners (HTTP/HTTPS), and attach target groups.


### 7. Create a Security Group for the Auto Scaling Group
Define a **security group** allowing necessary inbound and outbound traffic (e.g., HTTP, HTTPS, and SSH if needed).


### 8. Create an Auto Scaling Group (ASG)
Launch the **Auto Scaling Group** specifying:
- The AMI ID and instance type
- Subnets
- Target Groups
- Security Groups
- Desired capacity and scaling policies



## 🛡️ Best Practices

- Use **IAM roles** for EC2 and Auto Scaling Groups to securely access AWS services.
- Apply **least privilege** principles for all security groups and IAM policies.
- Enable **CloudWatch monitoring** and configure **Auto Scaling policies** based on metrics like CPU utilization.
- Use **private subnets** for backend services or databases.
- Enable **VPC Flow Logs** for network traffic monitoring.


## 📘 References

- [AWS VPC Documentation](https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html)
- [AWS ELB Documentation](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/introduction.html)
- [AWS Auto Scaling Documentation](https://docs.aws.amazon.com/autoscaling/ec2/userguide/AutoScalingGroup.html)
