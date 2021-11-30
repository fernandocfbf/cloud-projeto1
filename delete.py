import boto3
from functions.autoscalling.delete_autoscalling import delete_autoscalling_for_aws

from functions.instances.create_instance import create_instance_for_aws
from functions.instances.delete_instance import delete_all_instances_for_aws
from functions.instances.create_database import create_database_for_aws
from functions.launch_configuration.delete_launch_configuration import delete_launch_configuration_for_aws
from functions.load_balancer.create_load_balancer import create_load_balancer_for_aws
from functions.load_balancer.delete_all_load_balancer import delete_all_load_balancer_for_aws
from functions.security_groups.create_security_group import create_security_group_for_aws
from functions.security_groups.delete_all_security_groups import delete_all_security_groups_for_aws

from functions.ami.create_AMI import create_AMI_for_aws
from functions.ami.delete_all_AMIs import delete_all_AMIs_for_aws
from functions.target_groups.create_target_group import create_target_group_for_aws
from functions.target_groups.delete_target_group import delete_target_groups_for_aws

from functions.utils.initialize_log_file import initialize_log_file
from functions.utils.read_command import read_command
from constants import *

# CLIENTS AND WAITERS ---------------------------------------------
ohio_client = boto3.client('ec2', region_name=POSTGRES_REGION)
ohio_waiter_terminate = ohio_client.get_waiter('instance_terminated')

north_virginia_client = boto3.client('ec2', region_name=NORTH_VIRGINIA_REGION)
north_virginia_waiter_terminate = north_virginia_client.get_waiter('instance_terminated')
north_virginia_waiter_ami = north_virginia_client.get_waiter('image_available')

load_balancer_client = boto3.client('elbv2', region_name=NORTH_VIRGINIA_REGION)
load_balancer_waiter_available = load_balancer_client.get_waiter('load_balancer_available')
load_balancer_waiter_delete = load_balancer_client.get_waiter('load_balancers_deleted')

auto_scalling_client = boto3.client('autoscaling', region_name=NORTH_VIRGINIA_REGION)

# INITIALIZE LOG FILE ---------------------------------------------
initialize_log_file('log.txt')

# DELETING ALL LOAD BALANCERS ---------------------------------------------
delete_all_load_balancer_for_aws(load_balancer_client, load_balancer_waiter_delete)

# DELETING ALL INSTANCES ---------------------------------------------
delete_all_instances_for_aws(north_virginia_client, north_virginia_waiter_terminate)
delete_all_instances_for_aws(ohio_client, ohio_waiter_terminate)

# DELETING ALL AMIs ---------------------------------------------
delete_all_AMIs_for_aws(north_virginia_client)
delete_all_AMIs_for_aws(ohio_client)

# DELETING ALL TARGET GROUPS ---------------------------------------------
delete_target_groups_for_aws(LB_TARGET_GROUP_NAME, load_balancer_client)

# DELETING ALL SECURITY GROUPS ---------------------------------------------
delete_all_security_groups_for_aws(ohio_client)
delete_all_security_groups_for_aws(north_virginia_client)

# DELETING ALL AUTOSCALLING ---------------------------------------------
delete_autoscalling_for_aws(AT_GROUP_NAME, auto_scalling_client)

# DELETING LAUNCH CONFIGURATION ---------------------------------------------
delete_launch_configuration_for_aws(auto_scalling_client, LC_NAME)
