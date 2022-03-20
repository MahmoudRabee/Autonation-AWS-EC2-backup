import json
import boto3

def lambda_handler(event, context):

# 1- Working with AWS codecommit

    # connect to codecommit 
    codecommit = boto3.client('codecommit')

    # get data from tagged.json file from code commit
    response = codecommit.get_file(repositoryName='tagged-instanes', filePath='instances.json')
    file_content = response['fileContent'].decode()
    json_content = json.loads(file_content)

    # separate file content to two lists
    instance_IDs_true = []
    instance_IDs_false = []
    
    for key, value in json_content.items():
        if (value == "true"):
            instance_IDs_true.append(key)
        elif (value == "false"):
            instance_IDs_false.append(key)


# 2- working with AWS EC2

    #connect to ec2
    ec2 = boto3.resource('ec2') 
    EC2_RESOURCE = boto3.resource('ec2')
    
    # create tags template
    TRUE_TAGS = [
        {
            'Key': 'Backup',
            'Value': 'true'
        }
    ]
    FALSE_TAGS = [
        {
            'Key': 'Backup',
            'Value': 'false'
        }
    ]

    # make two lists of EC2 instances
    if(instance_IDs_true):
        true_instances = EC2_RESOURCE.instances.filter(InstanceIds=instance_IDs_true)
    else:
        true_instances = []
    
    if (instance_IDs_false):
        flase_instance = EC2_RESOURCE.instances.filter(InstanceIds=instance_IDs_false)
    else:
        flase_instance = []

     
    # update backup tag to true
    for instance in true_instances:
        instance.create_tags(Tags=TRUE_TAGS)
        print(f'true Tags successfully added to the instance {instance.id}')
    
    
    # update backup tag to false
    for instance in flase_instance:
        instance.create_tags(Tags=FALSE_TAGS)
        print(f'false Tags successfully added to the instance {instance.id}')
    
    
    return {
        'statusCode': 200
    }