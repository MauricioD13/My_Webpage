---
date: '2024-08-30'
draft: false
title: 'AWS History 1 - An attack and Three tier solution'
summary: 'The beginning of some histories about AWS cloud. This one is about EC2, S3 configuration and a little bit of Linux server management'
cover: 
  image: "/aws_history_1/aws_three_tier_arch.jpg"
categories:
- Cloud
- AWS
tags:
- AWS
- Cloud
- EC2
- S3
- Linux
---

# Introduction

**A sudden server crash can be every developer's nightmare, and that's exactly where our story begins.** One afternoon, our server went down without warning, setting off a series of unusual and challenging events. The server was configured with Nginx as a reverse proxy and PHP with Laravel for the backend—a setup that had been stable until now.

As I began to assess the problem, I discovered alarming evidence in the Nginx logs: our server was under attack. Originating from Singapore, the attack involved sophisticated port scanning and subdomain fuzzing using brute-force methods. The sheer volume of malicious traffic caused a significant spike, overloading the server and leading to multiple crashes.

Being an EC2 instance on AWS, I knew immediate action was required to mitigate the damage. I quickly modified the security groups to block incoming traffic from the malicious IP addresses and closed an open port above 6000 after verifying the services utilizing it. This rapid response helped stabilize the server, but I realized this was only a temporary fix.

To prevent future incidents, I set up a CloudWatch alarm based on the EC2 instance’s CPU utilization. Coupled with SNS notifications, this allowed our team to receive instant alerts and respond more promptly to any unusual activity. With the immediate threat under control, we recognized the need for a more resilient infrastructure leveraging AWS's native features.

## Requirements and design

Our application was built using PHP with Laravel for the backend and utilized WebSockets to connect to a mobile app. Initially, it was a monolithic application running on a single EC2 instance. The attack highlighted the vulnerabilities of this setup, and we knew it was time to rethink our architecture.

### Decoupling Components

To enhance scalability and resilience without undertaking a massive refactoring effort, I decided to decouple only the essential components needed to make the server stateless. This approach would allow us to improve the infrastructure incrementally while minimizing disruptions to the ongoing development.

#### Planning

At first, I considered implementing a two-tier architecture, which would have been a straightforward upgrade. However, I saw this challenge as an opportunity to deepen my understanding of AWS and Terraform. Despite this being a freelance project, I was eager to learn and apply Infrastructure as Code (IaC) principles. IaC would provide the flexibility to deploy and destroy infrastructure as needed, ensuring a clean and manageable environment.

### Implementing Terraform for Infrastructure Management

To manage the growing complexity of our infrastructure, I decided to use **Terraform** for Infrastructure as Code (IaC). This choice allowed us to automate the provisioning of resources, maintain version control, and facilitate collaboration among team members.

#### Setting Up Terraform with S3 Backend

I began by configuring an **S3 backend** to store the Terraform state files. Using S3 for the backend ensures that the state is stored remotely and securely, enabling team members to access and update the infrastructure state consistently. This setup also prevents state file conflicts that can occur when multiple users are working on the infrastructure.

To validate the configuration, I started deploying some foundational components, such as VPCs, subnets, and security groups. This initial deployment served as a proof of concept, confirming that the Terraform scripts and S3 backend were functioning correctly.

#### Enhancing Code Quality with Checkov

Leveraging the advantages of IaC, I set up a Python virtual environment to integrate additional tools into our workflow. I installed **Checkov**, a static code analysis tool for Terraform, which scans the codebase to detect security and compliance misconfigurations in AWS infrastructure, and wrote a bash script to run checkov as the documentation says.
Python configuration:

```
python3 -m venv .env
source .env/bin/activate
pip3 install checkov
```

Bash script:

```
#!/bin/bash
terraform plan -out tf.plan
terraform show -json tf.plan | jq > tf.json
checkov -f tf.json
```

By incorporating Checkov into our development process, we were able to:

- **Identify Security Risks**: Detect potential vulnerabilities before deploying resources.
- **Ensure Compliance**: Align with industry standards and best practices.
- **Improve Code Quality**: Maintain a high standard of code through continuous analysis.

While the configuration and in-depth usage of Checkov is an extensive topic on its own, its implementation significantly improved our infrastructure's security posture and code reliability. 
**Note:** Although it was a greenfield project and DevOps practices were not yet a comprehensive part of the team, I wanted to introduce some tools as a proof of concept to enhance the process in the future.

### Designing the Three-Tier Architecture

The primary requirement was to implement auto-scaling to handle fluctuations in network traffic effectively. This necessitated creating a server template—an AMI (Amazon Machine Image)—from which the auto-scaling service could launch instances. To ensure the AMI remained stateless, we needed to offload all files and storage data to external services.

- **Database Migration**: The application used MySQL, making it straightforward to migrate the database to Amazon RDS.
- **Static Files**: User images and other static assets were moved to S3, reducing the load on the server instances.

The updated architecture looked like this:
![Three tier architecture diagram](/aws_history_1/three_tier_arch_diag.svg)
This three-tier web application setup offered several advantages:

- **Resilience to Traffic Spikes**: Auto-scaling adjusts the number of instances based on demand.
- **Enhanced Security**: Internal IP addresses are not exposed, reducing the attack surface.
- **Managed Database Services**: Delegating database maintenance to AWS via RDS.
- **Load Distribution**: Balancing traffic across multiple instances improves performance.

#### Auto-Scaling Configuration

The auto-scaling group (ASG) required a launch template specifying:

- **Instance Type**: Selected based on performance needs.
- **New Key Pair**: For secure access and separating the credentials between servers.
- **Security Groups**: Defining inbound and outbound traffic rules.
- **AMI**: The stateless image created earlier.
To create the AMI, I launched an instance connected to the RDS, set up the necessary MySQL procedures, and performed a data dump. This instance served as the prototype for all future instances in the auto-scaling group.
![AMI Architecture](/aws_history_1/AMI_arch.svg)

### Static Assets and Public Resources

All static files and public resources were stored in an S3 bucket. This not only offloaded traffic from the EC2 instances but also leveraged S3's scalability and durability features.

### Auto-Scaling Group Settings

- **Desired Capacity**: Set to a minimum of two instances to ensure high availability.
- **Instance Refresh Strategy**: Configured as "Rolling" with a minimum healthy percentage of 50%. This strategy replaces instances gradually, maintaining service availability during updates.
- **Scaling Policy**: Implemented target tracking to maintain average CPU utilization within a specified range.

#### Understanding the Strategies

- **Rolling Updates**: Allows for zero-downtime deployments by updating instances in batches.
- **Target Tracking Scaling**: Automatically adjusts the number of instances to keep metrics like CPU utilization at desired levels.

### Database
For the Amazon RDS MySQL instance, the following configurations were applied:

- **MySQL Version**: Selected to match application compatibility.
- **Instance Class**: Chosen based on the expected workload.
- **Storage**: Allocated with automatic scaling and encryption enabled using AWS KMS.
- **Networking**: Placed within appropriate subnets and security groups for optimal performance and security.
- **Monitoring**:
    - **CloudWatch Logs**: Enabled for real-time monitoring of database activities.
    - **Enhanced Monitoring**: Activated for deeper insights.
- **Backup and Retention**:
    - **Automated Backups**: Scheduled with a 30-day retention period to meet business continuity requirements.
    - **Maintenance Window**: Defined during low-traffic periods to minimize impact.

## Deployment Process
To streamline deployments of new application versions, we established the following process:

1. **Create a New AMI**: The development team generates a new AMI from the staging server after implementing new features.
2. **Update the Launch Template**: The new AMI is attached to the launch template, automatically creating a new version.
3. **Initiate Instance Refresh**: Using the AWS console or CLI, we trigger an instance refresh. The auto-scaling group then replaces instances using the rolling update strategy.
This process ensures that updates are deployed without downtime, and the system scales efficiently to handle user demand.

## Future improvement

- **Enhanced Security Measures**:
    - **Implement AWS WAF**: To protect against common web exploits.
    - **Use AWS Shield**: For DDoS protection.
    - **Enable Multi-Factor Authentication (MFA)**: For all AWS accounts.
- **Automation Enhancements**:
    - **CI/CD Pipeline**: Set up using AWS CodePipeline and CodeDeploy for automated deployments.
    - **Infrastructure Automation**: Expand Terraform scripts to cover all infrastructure components.
- **Monitoring and Logging**:
    - **Centralized Logging**: Implement Amazon Elasticsearch Service and Kibana for log analysis.
    - **Application Performance Monitoring**: Use AWS X-Ray to trace requests and optimize performance.
- **Cost Optimization**:
    - **Reserved Instances**: Evaluate the use of reserved instances for cost savings.
    - **Right-Sizing**: Regularly assess instance types and sizes based on performance metrics.


