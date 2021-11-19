import boto3
from botocore.config import Config
from functions.create_log import create_log

def create_instance_for_aws(instance_name, region, image_id, instance_type, security_group, key_name):
    try:
        instance_region = Config(region_name=region)
        ec2 = boto3.resource('ec2', config=instance_region)
        create_log("Creating instance...")
        instance = ec2.create_instances(
            ImageId=image_id,
            MinCount=1,
            MaxCount=1,
            InstanceType=instance_type,
            #KeyName=key_name,
            #SecurityGroupIds=[security_group.group_id],
            TagSpecifications=[{
                "ResourceType": "instance",
                "Tags": [{"Key": "Name", "Value": instance_name}]
            }]
        )
        create_log("Instance {} created!".format(instance_name))
        return instance
    except NameError as e:
        create_log(e)
        return 