Cheap / Fast / Good ------- Pick two



Well-Architected Framework’s six pillars
https://aws.amazon.com/well-architected-tool/

1. Operational Excellence
The Operational Excellence pillar includes the ability to support development and run workloads effectively, gain insight into their operation, and continuously improve supporting processes and procedures to delivery business value. You can find prescriptive guidance on implementation in the Operational Excellence Pillar whitepaper.

Design Principles
There are five design principles for operational excellence in the cloud:

Perform operations as code
Make frequent, small, reversible changes
Refine operations procedures frequently
Anticipate failure
Learn from all operational failures
Best Practices
Operations teams need to understand their business and customer needs so they can support business outcomes. Ops creates and uses procedures to respond to operational events, and validates their effectiveness to support business needs. Ops also collects metrics that are used to measure the achievement of desired business outcomes.

Everything continues to change—your business context, business priorities, and customer needs. It’s important to design operations to support evolution over time in response to change, and to incorporate lessons learned through their performance.

2. Security
The Security pillar includes the ability to protect data, systems, and assets to take advantage of cloud technologies to improve your security. You can find prescriptive guidance on implementation in the Security Pillar whitepaper.

Design Principles
There are seven design principles for security in the cloud:

Implement a strong identity foundation
Enable traceability
Apply security at all layers
Automate security best practices
Protect data in transit and at rest
Keep people away from data
Prepare for security events
Best Practices
Before you architect any workload, you need to put in place practices that influence security. You’ll want to control who can do what. In addition, you want to be able to identify security incidents, protect your systems and services, and maintain the confidentiality and integrity of data through data protection.

You should have a well-defined and practiced process for responding to security incidents. These tools and techniques are important because they support objectives such as preventing financial loss or complying with regulatory obligations.

The AWS Shared Responsibility Model enables organizations that adopt the cloud to achieve their security and compliance goals. Because AWS physically secures the infrastructure that supports our cloud services, as an AWS customer you can focus on using services to accomplish your goals. The AWS Cloud also provides greater access to security data and an automated approach to responding to security events.

3. Reliability
The Reliability pillar encompasses the ability of a workload to perform its intended function correctly and consistently when it’s expected to. This includes the ability to operate and test the workload through its total lifecycle. You can find prescriptive guidance on implementation in the Reliability Pillar whitepaper.

Design Principles
There are five design principles for reliability in the cloud:

Automatically recover from failure
Test recovery procedures
Scale horizontally to increase aggregate workload availability
Stop guessing capacity
Manage change in automation
Best Practices
Before building any system, foundational requirements that influence reliability should be in place. For example, you must have sufficient network bandwidth to your data center. These requirements are sometimes neglected (because they are beyond a single project’s scope). With AWS, however, most of the foundational requirements are already incorporated or can be addressed as needed.

The cloud is designed to be nearly limitless, so it’s the responsibility of AWS to satisfy the requirement for sufficient networking and compute capacity, leaving you free to change resource size and allocations on demand.

A reliable workload starts with upfront design decisions for both software and infrastructure. Your architecture choices will impact your workload behavior across all six AWS Well-Architected pillars. For reliability, there are specific patterns you must follow, such as loosely coupled dependencies, graceful degradation, and limiting retries.

Changes to your workload or its environment must be anticipated and accommodated to achieve reliable operation of the workload. Changes include those imposed on your workload, like a spikes in demand, as well as those from within such as feature deployments and security patches.

Low-level hardware component failures are something to be dealt with every day in an on-premises data center. In the cloud, however, these are often abstracted away. Regardless of your cloud provider, there is the potential for failures to impact your workload. You must therefore take steps to implement resiliency in your workload, such as fault isolation, automated failover to healthy resources, and a disaster recovery strategy.

4. Performance Efficiency
The Performance Efficiency pillar includes the ability to use computing resources efficiently to meet system requirements, and to maintain that efficiency as demand changes and technologies evolve. You can find prescriptive guidance on implementation in the Performance Efficiency Pillar whitepaper.

Design Principles
There are five design principles for performance efficiency in the cloud:

Democratize advanced technologies
Go global in minutes
Use serverless architectures
Experiment more often
Consider mechanical sympathy
Best Practices
Take a data-driven approach to building a high-performance architecture. Gather data on all aspects of the architecture, from the high-level design to the selection and configuration of resource types.

Reviewing your choices on a regular basis ensures you are taking advantage of the continually evolving AWS Cloud. Monitoring ensures you are aware of any deviance from expected performance. Make trade-offs in your architecture to improve performance, such as using compression or caching, or relaxing consistency requirements

The optimal solution for a particular workload varies, and solutions often combine multiple approaches. AWS Well-Architected workloads use multiple solutions and enable different features to improve performance

5. Cost Optimization
The Cost Optimization pillar includes the ability to run systems to deliver business value at the lowest price point. You can find prescriptive guidance on implementation in the Cost Optimization Pillar whitepaper.

Design Principles
There are five design principles for cost optimization in the cloud:

Implement cloud financial management
Adopt a consumption model
Measure overall efficiency
Stop spending money on undifferentiated heavy lifting
Analyze and attribute expenditure
Best Practices
As with the other pillars, there are trade-offs to consider. For example, do you want to optimize for speed to market or for cost? In some cases, it’s best to optimize for speed—going to market quickly, shipping new features, or simply meeting a deadline—rather than investing in up-front cost optimization.

Design decisions are sometimes directed by haste rather than data, and as the temptation always exists to overcompensate rather than spend time benchmarking for the most cost-optimal deployment. This might lead to over-provisioned and under-optimized deployments.

Using the appropriate services, resources, and configurations for your workloads is key to cost savings

6. Sustainability
The discipline of sustainability addresses the long-term environmental, economic, and societal impact of your business activities. You can find prescriptive guidance on implementation in the Sustainability Pillar whitepaper.

Design Principles
There are six design principles for sustainability in the cloud:

Understand your impact
Establish sustainability goals
Maximize utilization
Anticipate and adopt new, more efficient hardware and software offerings
Use managed services
Reduce the downstream impact of your cloud workloads
Best Practices
Choose AWS Regions where you will implement workloads based on your business requirements and sustainability goals.

User behavior patterns can help you identify improvements to meet sustainability goals. For example, scale infrastructure down when not needed, position resources to limit the network required for users to consume them, and remove unused assets.

Implement software and architecture patterns to perform load smoothing and maintain consistent high utilization of deployed resources. Understand the performance of your workload components, and optimize the components that consume the most resources.

Analyze data patterns to implement data management practices that reduce the provisioned storage required to support your workload. Use lifecycle capabilities to move data to more efficient, less performant storage when requirements decrease, and delete data that’s no longer required.

Analyze hardware patterns to identify opportunities that reduce workload sustainability impacts by minimizing the amount of hardware needed to provision and deploy. Select the most efficient hardware for your individual workload.

In your development and deployment process, identify opportunities to reduce your sustainability impact by making changes, such as updating systems to gain performance efficiencies and manage sustainability impacts. Use automation to manage the lifecycle of your development and test environments, and use managed device farms for testing.



https://c4model.com/
The C4 Model:

The C4 model is introduced as a way to describe and communicate software architecture effectively. It's designed to create maps of code at different levels of detail, similar to zooming in and out on Google Maps.
The four levels of the C4 model are:
Level 1: System Context diagram
Level 2: Container diagram
Level 3: Component diagram
Level 4: Code (e.g., UML class) diagram
Abstractions in the C4 Model:

The model defines several abstractions to create a ubiquitous language for describing software systems. These include:
Person: Represents users of the software system.
Software System: The highest level of abstraction, describing something delivering value.
Container: Represents applications or data stores.
Component: Represents a grouping of related functionality.



AWS Service endpoints and quotas
https://docs.aws.amazon.com/general/latest/gr/aws-service-information.html




Ludichart
https://lucid.app/lucidchart/a718841a-2e2d-4052-9a2a-5f8c633ce9b4/edit?beaconFlowId=9591EE4C1C8D62EA&invitationId=inv_938c540f-61fe-4201-b081-ded42fbd8433&page=0_0#




Billing and cost
can setup budget (threshold) based on charges and on things like hours used of a particular service.
Can setup alerts (email)


generate passwords
https://passwordsgenerator.net/



AWS CLI auto-prompt

[cloudshell-user@ip-10-140-98-140 ~]$ aws --cli-auto-prompt
> aws sts get-caller-identity
{
    "UserId": "AIDA2YOXE7Z6BWWISXNG3",
    "Account": "739722460796",
    "Arn": "arn:aws:iam::739722460796:user/bhanu"
}
[cloudshell-user@ip-10-140-98-140 ~]$ 




AWS CLI Reference
https://docs.aws.amazon.com/cli/latest/


Understanding diff directories
https://docs.freebsd.org/en/books/handbook/basics/#dirstructure

/usr/bin have installations that comes with os

/usr/local/bin have installations that you install











![1a](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/d1ce2b14-1bae-4842-95de-0e6aa66e027b)
![1b](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/ff3b9678-1450-432d-a24c-72d4cba3fadd)
![1c](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/36d85541-e538-447d-822f-40e22ecdfda3)
![1d](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/685fa221-291f-4839-977a-996575b48045)
![1e](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/6efa9253-d54e-4cec-9e2b-ecd999967c80)
![1f](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/43ba4414-063e-4fc5-9756-07a1ffb422ca)
![scp](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/bbc89f35-58a1-41ad-80b0-ac089c651a32)
![1h](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/63c2e675-892f-4570-b169-786323b94011)

  





Was able to setup gitpod and added the configuration to download aws-cli whenever gitpod is launched.

![1](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/a6553859-1406-4f99-b94e-b5e2eba86a73)



  





Recreated Logical Architecture Design in Ludichart.

![2](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/2f2b6c85-0b39-4edf-aab5-8cee7e5297f1)


[Ludi Charts Share Link](https://lucid.app/lucidchart/29a2bc3b-92f6-4cd1-ae2f-5296873b761b/edit?invitationId=inv_64938dd2-b1c3-4b51-b837-3ad8d5dfba80)


Also understood how to setup budget and alarms by following the cli commands given in journal/week0.md



How to resolve the issue of pushing the sensitive info to remote bymistake?

Using trufflehog and bfg


The primary purpose of BFG Repo-Cleaner is to remove specific files or content from the Git history, not from the working directory or the latest commit. When you use BFG Repo-Cleaner with options like --delete-files or --replace-text, it modifies the Git history by removing or replacing the specified content in the commits.

If you get to know your creds were being exposed, firstly go to aws and deactivate and delete them.

  
brew install trufflesecurity/trufflehog/trufflehog


  
brew install bfg

  
We can test using test-repo
   
trufflehog git https://github.com/trufflesecurity/test_keys --only-verified
  
then you test your own repo
  
trufflehog git https://github.com/bhanumalhotra123/repo_name --only-verified
  
Now once you have found the security issues, to replace those values we use tool called bfg

  
https://rtyley.github.io/bfg-repo-cleaner/
  
Remember to keep the requirements file out of the project repo so that it is not pushed to remote by mistake as it contains the sensitive data.

$ bfg --replace-text ../passwords.txt  my-repo.git

 ![3](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/1ab982df-30ec-4a9a-b7f5-066063798fcc)


If you want to remove specific strings from the actual content of files in the working directory or the latest commit, you need to manually modify the files, commit the changes, and push the new commit to the remote repository.




  Implemented cloudwatch logs

![1i](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/fc1b9122-8c5b-4c67-a5bc-45480fc696bb)


Implemented x-ray and x-ray subsegment
  
![1j](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/e69994a0-e76c-44ef-a7f5-8b54529ed1ce)
  
![1k](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/af7a808e-81c1-43dd-9d72-9b6c881e9385)
  
![1l](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/66d9949d-2d7e-48bf-88bd-17fc6eca2679)
  
![1m](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/9114a4ff-a69b-4df0-8132-4b1de1ac3256)

![1o](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/acd96495-5fc5-4293-92e3-1046e2d04360)
