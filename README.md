# Autonation-AWS-EC2-backup
This is a short project that automate specific EC2 instances based on EC2 tags


## Table of content Content
1.**[Project discription](##Project-discription)**<br>

2.**[Create AWS codecommit repository.](##Create-AWS-codecommit-repository)**<br>

3.**[Create AWS IAM Role.](##Create-AWS-IAM-Role)**<br>

4.**[Create Lambda Function.](##Create_Lambda_Function)**

5.**[Schedule Lambda Function](##Schedule_Lambda_Function)**
## Project discription
This project to use `AWS Backup` service to bakup EC2 instances automatically Every day.
<br>
We will Backup only EC2 instances With tag `Backup:true`, Instances with tag `Backup:false` will not be backed up.
<br>
There is an AWS codecommit repository contain a JSON file that have a list of EC2 instances IDs and the value of tag `true` or `false`, and any change to this JSON file will automatically update the tags of EC2 instances.

## Create AWS codecommit repository
Create `AWS codeCommit` repository with name `tagged-instanes`.

To create an AWS codecommit repository you can do it with:
- AWS console: [Create an AWS CodeCommit repository
](https://docs.aws.amazon.com/codecommit/latest/userguide/how-to-create-repository.html#how-to-create-repository-cli)
- AWS CLI: **follow steps below** 👇 
    
    * Make sure that you have configured the AWS CLI with the your AWS account :
    ``` 
    aws configure
    ```
    * specify the name of your repository-I'll write tagged-instanes-and discription for it and run this command:
    
    
    ```
    aws codecommit create-repository --repository-name tagged-instanes --repository-description "this repo contain a list of EC2 instances"
    ```
    * Add `instances.json` file to your repository contains the list of EC2 IDs and the value of Backup tag like this:
    ```
    {
    "EC2 instance ID":"True or false" 
    }
    ```
    
## Create AWS IAM Role
Two `AWS Lambda` finctions created in this project, we need to give them the right permission to do the job

### 1- read and tag Role
* First Role attached to The `Lambda` Function that read`instances.json` file and update EC2 tags. so we need two policy:
1. **codecommit GetFile** : to read file from codecommit repo.

2. **ec2 CreateTags and list instances** : to create or update tag of EC2 instances.

**Role name:** read-tag-ec2

**IAM JSON policy**:
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "ec2:DescribeInstances",
                "ec2:CreateTags",
                "codecommit:GetFile"
            ],
            "Resource": "*"
        }
    ]
}
```

### 2- backup-ec2 Role
* Second Role attached to The `Lambda` Function that read Tags of all EC2 instances andbackup EC2 instances with With tag `Backup:true` .

 We need three policy:
 1. **EC2 list instances**: list instances to check the tags.
 2. **Backup:** to start backup job.
 3. **IAM PassRole:** allow lambda to pass IAM role to AWS Backup [More information about passRole](https://docs.aws.amazon.com/iot/latest/developerguide/pass-role.html)

 **Role name:** backup-ec2

**IAM JSON policy**:
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "iam:PassRole",
                "ec2:DescribeInstances",
                "backup:StartBackupJob"
            ],
            "Resource": "*"
        }
    ]
}
```
### 3- Attached-backup Role
Last Role that Role will passed from Lambda function to AWS backup.

Create New Role With name **Attached-backup** with policy `AWSBackupServiceRolePolicyForBackup`.



## Create Lambda Functions
### 1. read and tag Function
This lambda function Triggered after any modification (after Commit) and read this `instances.json` and Update tags of EC2 instances.
 - Create Lambda function and copy the code from `read-tag.py`, change `repositoryName` and `filePath` to names that you wrote.
 - Attach `read-tag-ec2` Role to this function,change `ResourceArn` and `IamRoleArn` to valid value.
 - Create an AWS CodeCommit trigger for an AWS Lambda function. **Example:** [click here](https://docs.aws.amazon.com/codecommit/latest/userguide/how-to-notify-lambda.html)

### 2. Backup EC2 Function
This lambda function creates backup of EC2 instances based on its tags
 - Create Lambda function and copy the code from `backup-ec2.py`.
 - Attach `backup-ec2` Role to this function.

## Schedule Lambda Function
**Backup EC2** Lambda Function will invoked once every day.
1. create **AWS eventBridge** rule to schedule cron job to run every day.

Using AWS CLI:
```  
aws events put-rule --schedule-expression "rate(1 day)" --event-bus-name default --name DailyLambdaJob

```
2. Add **Backup EC2** Lambda Function as a terget to **runEveryDay** Rule.

Using AWS CLI:
```
aws events put-targets --rule DailyLambdaJob --targets "Id"="1","Arn"="Lambda function ARN"
```

