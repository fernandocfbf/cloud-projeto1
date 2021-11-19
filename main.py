import boto3
from functions.create_instance import create_instance_for_aws
from functions.delete_instance import delete_all_instances_for_aws
from functions.create_database import create_database_for_aws

#AWS KEYS 
KEY_NAME='fernandocfbf'

# OHIO INSTANCE CONFIG
OHIO_NAME='Ohio-f'
OHIO_REGION='us-east-2'
OHIO_IMAGE_ID='ami-020db2c14939a8efb'
OHIO_INSTANCE_TYPE='t2.micro'
OHIO_SECURITY_GROUP='test'

# POSTGRES INSTANCE CONFIG
POSTGRES_NAME='Postgres-f'
POSTGRES_REGION='us-east-2'
POSTGRES_IMAGE_ID='ami-020db2c14939a8efb'
POSTGRES_INSTANCE_TYPE='t2.micro'
POSTGRES_SECURITY_GROUP='test'

# CLIENTS AND WAITERS ---------------------------------------------
ohio_client = boto3.client('ec2', region_name=OHIO_REGION)
ohio_waiter_terminate = ohio_client.get_waiter('instance_terminated')

# DELETING ALL INSTANCES ---------------------------------------------
delete_all_instances_for_aws(ohio_client, ohio_waiter_terminate)

# CRIANDO BANCO DE DADOS ---------------------------------------------
postgres, postgres_id = create_database_for_aws(POSTGRES_NAME, POSTGRES_REGION, POSTGRES_IMAGE_ID, POSTGRES_INSTANCE_TYPE, POSTGRES_SECURITY_GROUP, KEY_NAME)

# CRIANDO INSTÂNCIAS ---------------------------------------------
ohio_instance, ohio_instance_ip = create_instance_for_aws(OHIO_NAME, OHIO_REGION, OHIO_IMAGE_ID, OHIO_INSTANCE_TYPE, OHIO_SECURITY_GROUP, KEY_NAME)
