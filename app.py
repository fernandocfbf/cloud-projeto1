import boto3
import time

from functions.autoscalling.create_autoscalling import create_autoscalling_for_aws
from functions.autoscalling.delete_autoscalling import delete_autoscalling_for_aws
from functions.instances.create_instance import create_instance_for_aws
from functions.instances.create_database import create_database_for_aws
from functions.instances.delete_instance import delete_all_instances_for_aws
from functions.load_balancer.create_load_balancer import create_load_balancer_for_aws
from functions.load_balancer.delete_all_load_balancer import delete_all_load_balancer_for_aws
from functions.security_groups.create_security_group import create_security_group_for_aws
from functions.security_groups.delete_all_security_groups import delete_all_security_groups_for_aws
from functions.ami.create_AMI import create_AMI_for_aws
from functions.ami.delete_all_AMIs import delete_all_AMIs_for_aws
from functions.target_groups.create_target_group import create_target_group_for_aws
from functions.target_groups.delete_target_group import delete_target_groups_for_aws
from functions.launch_configuration.create_launch_configuration import create_launch_configuration_for_aws
from functions.launch_configuration.delete_launch_configuration import delete_launch_configuration_for_aws
from functions.listeners.create_listener import create_listener_for_aws
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
time.sleep(5)

# DELETING ALL AUTOSCALLING ---------------------------------------------
delete_autoscalling_for_aws(AT_GROUP_NAME, auto_scalling_client)
time.sleep(5)

# DELETING LAUNCH CONFIGURATION ---------------------------------------------
delete_launch_configuration_for_aws(auto_scalling_client, LC_NAME)
time.sleep(5)

# DELETING ALL AMIs ---------------------------------------------
delete_all_AMIs_for_aws(north_virginia_client)
time.sleep(5)

# DELETING ALL INSTANCES ---------------------------------------------
delete_all_instances_for_aws(north_virginia_client, north_virginia_waiter_terminate)
delete_all_instances_for_aws(ohio_client, ohio_waiter_terminate)
time.sleep(5)

# DELETING ALL TARGET GROUPS ---------------------------------------------
delete_target_groups_for_aws(LB_TARGET_GROUP_NAME, load_balancer_client)
time.sleep(5)

# DELETING ALL SECURITY GROUPS ---------------------------------------------
delete_all_security_groups_for_aws(ohio_client)
delete_all_security_groups_for_aws(north_virginia_client)
time.sleep(5)

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

load_balancer_protocols = read_command('protocols', 'load_balancer_security_group.txt', is_json=True)
load_balancer_security_group = create_security_group_for_aws(
    NORTH_VIRGINIA_SECURITY_GROUP_LD,
    NORTH_VIRGINIA_REGION,
    'enable ports',
    'load_balancer',
    load_balancer_protocols)

time.sleep(5)

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
   user_data=django_user_data,
   sleep=True)

time.sleep(5)

# CREATING AMI ---------------------------------------------
ami_django, ami_django_id = create_AMI_for_aws(north_virginia_client, 'django-ami', django_id, north_virginia_waiter_ami)

# DELETING DJANGO ---------------------------------------------
delete_all_instances_for_aws(north_virginia_client, north_virginia_waiter_terminate)

# CREATING TARGET GROUP ---------------------------------------------
target_group = create_target_group_for_aws(
  LB_TARGET_GROUP_NAME,
  LB_PROTOCOL,
  LB_HEALTH_CHECK_ENABLED,
  LB_HEALTH_CHECK_PROTOCOL,
  LB_HEALTH_CHECK_PORT,
  LB_HEALTH_CHECK_PATH,
  LB_PORT,
  LB_TARGET_TYPE,
  north_virginia_client,
  load_balancer_client)

# CREATING LOAD BALANCER ---------------------------------------------
load_balancer, amazon_resource_name = create_load_balancer_for_aws(
    north_virginia_client,
    load_balancer_client,
    'load-balancer-north-viriginia',
    load_balancer_security_group,
    load_balancer_waiter_available)

# CREATING AUTOSCALLIING ---------------------------------------------
create_launch_configuration_for_aws(
   auto_scalling_client,
   LC_NAME,
   ami_django_id,
   django_security_group,
   LC_INSTANCE_TYPE,
   KEY_NAME)

create_autoscalling_for_aws(
   AT_GROUP_NAME,
   AT_LAUNCH_CONFIGURATION_NAME,
   AT_MIN_SIZE,
   AT_MAX_SIZE,
   auto_scalling_client,
   north_virginia_client,
   target_group)

# CREATING LISTENER ---------------------------------------------
create_listener_for_aws(
   LT_PROTOCOL,
   LT_PORT,
   LT_DEFAULT_ACTIONS_TYPE,
   target_group,
   amazon_resource_name,
   load_balancer_client)