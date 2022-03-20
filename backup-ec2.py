import json
import boto3

def lambda_handler(event, context):
    # TODO implement
    client = boto3.client('backup')
    ec2 = boto3.resource('ec2')

    for instance in ec2.instances.all():
        print(
            "Id: {0}\nTagKeyName: {1}\nTagValue: {2}\nState: {3}\n".format(
            instance.id, (instance.tags[0]).get("Key"),(instance.tags[0]).get("Value"), instance.state))
            
        if (instance.tags[0]).get("Key")=="Backup" and (instance.tags[0]).get("Value")=="true":
            print("Trueeeeee")
        response = client.start_backup_job(
            BackupVaultName='Default',
            ResourceArn='arn:aws:ec2:eu-west-1:0000000000:instance/'+instance.id,
            IamRoleArn='arn:aws:iam:::',
           
        )
    
  

    return {
        'statusCode': 200,
        'body': response
    }
