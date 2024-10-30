---
date: '2024-08-30'
draft: false
title: 'AWS History 0 - The Hidden Costs of Poor Cloud Management'
summary: 'The beginning of some histories about AWS cloud. This one is about EC2, S3 configuration and a little bit of Linux server management'
cover: 
  image: "/aws_history_0/aws_synthwave_0.jpg"
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

I felt inspired to write this article because I could not believe the number of poor-quality software providers in the market. Some of them are taking advantage of people who do not have the technical background to understand the solutions proposed, and charging more money for it. By coincidence, I started working with an e-commerce shop that hosts its resources on AWS. They used to work with a software provider, but the work ethics of this provider were far from the best in the market, to put it mildly.

The issues were the following, and the reasons why I started working there:

- Billing
- Backups
- Crash of the server

Long story short, they set up Magento 2 with the necessary configurations, but due to some commercial relationship issues, they stopped providing support to the shop. Through a mutual friend, I contacted the owners of the shop to help troubleshoot the server.

The technological stack of the shop is:

- EC2 instance
- S3 bucket for the backups (in the provider’s AWS account)
- Ubuntu Server
- Apache
- Magento

When I started examining the configurations of the EC2 instance, the first thing I noticed was that the instance type was the monstrosity of a c6i.2xlarge. I call it a monstrosity because the peak CPU usage is only 20% even on the busiest days, such as Christmas or other special occasions. The owners said that the provider had only explained that they needed that instance type; otherwise, the development would not work. One important thing about public clouds is that they can be very expensive if the appropriate configurations are not made, and if you're new to AWS, it's challenging to configure it well.

# Changes

The billing of AWS was pretty high for the usage that the shop was giving to the services and mainly the server was crashing.

## Server crashed

The website was crased, so I started adding a rule to the security group of the instance to access the server via SSH, and restarting the server. In the server, I did the 101 of the linux server administration that is to check all the basic metrics: RAM, CPU, storage and logs, using some common commands like `htop`, `df -h`, `systemctl status` , `journalctl -xe` ,etc…

### Logs

In the logs of Magento it said that there was a issue with the writing of some data that was standard procedure of the CMS, and because of that, I think that the problem was not the Magento configuration, instated was a server problem related to memory/storage.

### Storage

The space available was pretty low, this was a clue of the problem. I took some data of this from Sunday in the day and it look like this:
![storage](/aws_history_0/Pasted%20image%2020240805093409.png)
And Monday morning was like this:
![storage](/aws_history_0/Pasted%20image%2020240805093430.png)

That was why the server was crashing but it was not the root cause.

### Cron

The behavior of the storage availability indicated that there was a scheduled task running on Sunday night. Therefore, I examined the crontab and discovered numerous jobs for creating database and website backups - daily, weekly, and monthly. Two of the cron jobs were key: the first was responsible for performing the cleanup, which was not occurring, and the second was the S3 backup sync. The sync command was pointing to an S3 bucket that was not owned by the shop.

![cron](/aws_history_0/Pasted%20image%2020240805093527.png)

In the cleanup script was a typo that was really easy to fix. The scripts delete recursively all the data that were in some specific directories that were already backed up.

### Backup in S3 bucket

To resolve the S3 backup issue, I created a new S3 bucket in the shop's own account and updated the sync command to point to this bucket. Additionally, modified the scheduled task timing to send data weekly on Sundays and monthly on the first day of each month.

![backup](/aws_history_0/Pasted%20image%2020240805093544.png)

To allow connection between services, I created an IAM role that allows the EC2 instance to put objects into the S3.

Finally, I attached the IAM role to the instance and proved the connection between the EC2 and the S3 bucket.

## Instance type and AWS Compute Optimizer

I used AWS Compute Optimizer to determine the optimal EC2 instance, which suggested an r6i.large. Magento documentation recommends compute-optimized instances (C-type) for best performance. However, considering the c6i.2xlarge has substantial memory and the owners mentioned custom code connecting Magento to their stock software, I opted for the r6i.large with 16 GB RAM.

Before initiating the process, I created backups of both Magento and the database. Since they were using an Elastic IP (EIP), there was no concern about DNS provider issues when stopping the instance. Then proceeded to stop the instance, change the instance type, and the process completed successfully.

![instance](/aws_history_0/Pasted%20image%2020240805093626.png)

# Conclusions

- There was a 64% cost optimization after making these configurations. Therefore, it's really important in a cloud environment to know what the proper adjustments are for your business needs. The model of AWS is pay-per-use; hence, it's the responsibility of the customer to configure the services in the best way possible.
- Sometimes if you own an e-commerce shop and your store is in the cloud, it is wise to seek a second opinion when you think there is suspicious behavior in the AWS services. Because there are many unreliable providers of cloud consulting, it's also prudent to verify if a provider is a certified partner here: [https://partners.amazonaws.com/](https://partners.amazonaws.com/)
  - I know that providers are not always partners of AWS (it has its challenges), but it is a starting point. Especially when the provider claims they are.

Enjoy your cloud journey
