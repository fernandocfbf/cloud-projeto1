import boto3

from functions.create_instance import create_instance_for_aws
from functions.delete_all_AMIs import delete_all_AMIs_for_aws
from functions.delete_instance import delete_all_instances_for_aws
from functions.create_database import create_database_for_aws
from functions.create_security_group import create_security_group_for_aws
from functions.delete_all_security_groups import delete_all_security_groups_for_aws
from functions.create_AMI import create_AMI_for_aws
from functions.read_command import read_command
from constants import *

# CLIENTS AND WAITERS ---------------------------------------------
ohio_client = boto3.client('ec2', region_name=POSTGRES_REGION)
ohio_waiter_terminate = ohio_client.get_waiter('instance_terminated')

north_virginia_client = boto3.client('ec2', region_name=NORTH_VIRGINIA_REGION)
north_virginia_waiter_terminate = north_virginia_client.get_waiter('instance_terminated')
north_virginia_waiter_ami = north_virginia_client.get_waiter('image_available')

# DELETING ALL INSTANCES ---------------------------------------------
delete_all_instances_for_aws(ohio_client, ohio_waiter_terminate)
delete_all_instances_for_aws(north_virginia_client, north_virginia_waiter_terminate)

# DELETING ALL SECURITY GROUPS ---------------------------------------------
delete_all_security_groups_for_aws(ohio_client)
delete_all_security_groups_for_aws(north_virginia_client)

# DELETING ALL AMIs ---------------------------------------------
delete_all_AMIs_for_aws(north_virginia_client)
delete_all_AMIs_for_aws(ohio_client)

# CREATING SECURITY GROUPS ---------------------------------------------
postgres_protocols = read_command('protocols', 'database_security_group.txt', is_json=True)
postgres_security_group = create_security_group_for_aws(
    POSTGRES_SECURITY_GROUP,
    POSTGRES_REGION,
    'enable ports',
    'postgres',
    postgres_protocols)

django_protocols = read_command('protocols', 'django_security_group.txt', is_json=True)
django_security_group = create_security_group_for_aws(
    NORTH_VIRGINIA_SECURITY_GROUP,
    NORTH_VIRGINIA_REGION,
    'enable ports',
    'django',
    django_protocols)

# CREATING DATABASE ---------------------------------------------
postgres, postgres_ip, postgres_id = create_database_for_aws(
    POSTGRES_NAME,
    POSTGRES_REGION,
    POSTGRES_IMAGE_ID,
    POSTGRES_INSTANCE_TYPE,
    postgres_security_group,
    KEY_NAME)

# CREATING DJANGO ---------------------------------------------
django_user_data = read_command('commands', 'install_django.sh').replace("s/node1/postgres_ip/g", f"s/node1/{postgres_ip}/g", 1)
django, django_ip, django_id = create_instance_for_aws(
    NORTH_VIRGINIA_NAME,
    NORTH_VIRGINIA_REGION,
    NORTH_VIRGINIA_IMAGE_ID,
    NORTH_VIRGINIA_INSTANCE_TYPE,
    django_security_group,
    KEY_NAME,
    user_data=django_user_data)

# CREATING AMI ---------------------------------------------
ami_django, ami_django_id = create_AMI_for_aws(north_virginia_client, 'django_ami', django_id, north_virginia_waiter_ami)

# DELETING DJANGO ---------------------------------------------
delete_all_instances_for_aws(north_virginia_client, north_virginia_waiter_terminate)

