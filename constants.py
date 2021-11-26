# AWS KEYS ---------------------------------------------
KEY_NAME = 'fernandocfbf_key'

# NORTH VIRGINIA INSTANCE CONFIG ---------------------------------------------
NORTH_VIRGINIA_NAME = 'North-Virigina-f'
NORTH_VIRGINIA_REGION = 'us-east-1'
NORTH_VIRGINIA_IMAGE_ID = 'ami-0279c3b3186e54acd'
NORTH_VIRGINIA_INSTANCE_TYPE = 't2.micro'
NORTH_VIRGINIA_SECURITY_GROUP = 'test'
NORTH_VIRGINIA_SECURITY_GROUP_LD = 'load-balancer'

# POSTGRES INSTANCE CONFIG ---------------------------------------------
POSTGRES_NAME = 'Postgres-f'
POSTGRES_REGION = 'us-east-2'
POSTGRES_IMAGE_ID = 'ami-020db2c14939a8efb'
POSTGRES_INSTANCE_TYPE = 't2.micro'
POSTGRES_SECURITY_GROUP = 'database'

# LOAD BALANCER TARGET GROUP ---------------------------------------------
TARGET_GROUP_NAME = 'load-balancer-target-group'
PROTOCOL = 'HTTP'
HEALTH_CHECK_ENABLED = True
HEALTH_CHECK_PROTOCOL = 'HTTP'
HEALTH_CHECK_PORT = '8080'
HEALTH_CHECK_PATH = '/admin/'
PORT = 8080
TARGET_TYPE = 'instance'