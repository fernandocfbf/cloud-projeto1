import boto3
from botocore.config import Config
from functions.create_log import create_log

def create_instance_for_aws(instance_name, region, image_id, instance_type, security_group, key_name, user_data=None):
    try:
        instance_region = Config(region_name=region)
        ec2 = boto3.resource('ec2', config=instance_region)
        create_log("Creating instance...")
        if user_data:
            instance = ec2.create_instances(ImageId=image_id, MinCount=1, MaxCount=1, InstanceType=instance_type,
                # KeyName=key_name, SecurityGroupIds=[security_group.group_id],
                TagSpecifications=[{ "ResourceType": "instance", "Tags": [{"Key": "Name", "Value": instance_name}]}],
                UserData=user_data
            )
        else:
            instance = ec2.create_instances(ImageId=image_id, MinCount=1, MaxCount=1, InstanceType=instance_type,
                # KeyName=key_name, SecurityGroupIds=[security_group.group_id],
                TagSpecifications=[{ "ResourceType": "instance", "Tags": [{"Key": "Name", "Value": instance_name}]}],
            )
        instance[0].wait_until_running()
        instance[0].reload()
        create_log("Instance {0} created!".format(instance_name))
        return instance, instance[0].public_ip_address
    except NameError as e:
        create_log(e)
        return
