from functions.utils.create_log import create_log


def delete_autoscalling_for_aws(autoscalling_name, client):
    try:
        create_log('Deleting all autoscalling... ({0})'.format(client.meta.region_name))
        is_empty = len(client.describe_auto_scaling_instances()['AutoScalingInstances']) == 0
        if is_empty:
            create_log('Autoscalling {0} not found! ({1})'.format(autoscalling_name, client.meta.region_name))
        else:
            client.delete_auto_scaling_group(
                AutoScalingGroupName=autoscalling_name,
                ForceDelete=True
            )
    except NameError as e:
        create_log(e)
