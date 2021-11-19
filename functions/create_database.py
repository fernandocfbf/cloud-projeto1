import boto3
from botocore.config import Config
from functions.create_instance import create_instance_for_aws
from functions.read_command import read_command
from functions.create_log import create_log

def create_database_for_aws(instance_name, region, image_id, instance_type, security_group, key_name):
    commands = read_command('install_postgres.sh')
    postgres, postgres_ip = create_instance_for_aws(instance_name, region, image_id, instance_type, security_group, key_name, user_data=commands)
    create_log('Database created with postgres!')
    return postgres, postgres_ip