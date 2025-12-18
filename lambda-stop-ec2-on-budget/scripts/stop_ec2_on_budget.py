import logging
import boto3
from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_running_instances(regions=None):
    """Return a dict mapping region -> [instance ids] for running/pending instances."""
    ec2_client = boto3.client('ec2')
    if regions is None:
        regions = [r['RegionName'] for r in ec2_client.describe_regions()['Regions']]

    result = {}
    for region in regions:
        try:
            ec2 = boto3.resource('ec2', region_name=region)
            instances = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running', 'pending']}])
            ids = [i.id for i in instances]
            if ids:
                result[region] = ids
        except ClientError as e:
            logger.exception('Error listing instances in %s: %s', region, e)
    return result


def stop_instances_in_region(region, instance_ids, dry_run=False):
    client = boto3.client('ec2', region_name=region)
    try:
        logger.info('Stopping %s instances in %s', len(instance_ids), region)
        client.stop_instances(InstanceIds=instance_ids, DryRun=dry_run)
        if not dry_run:
            waiter = client.get_waiter('instance_stopped')
            waiter.wait(InstanceIds=instance_ids)
        logger.info('Stopped instances in %s: %s', region, instance_ids)
    except ClientError as e:
        if 'DryRunOperation' in str(e):
            logger.info('Dry run successful for %s: %s', region, instance_ids)
        else:
            logger.exception('Failed to stop instances in %s: %s', region, e)


def stop_all_running_instances(dry_run=False, regions=None):
    instances_by_region = get_running_instances(regions=regions)
    if not instances_by_region:
        logger.info('No running instances found.')
        return instances_by_region

    for region, ids in instances_by_region.items():
        stop_instances_in_region(region, ids, dry_run=dry_run)

    return instances_by_region


def lambda_handler(event, context):
    stop_all_running_instances()


if __name__ == '__main__':
    # quick local test (does not run in AWS Lambda)
    # set dry_run=True to avoid stopping instances accidentally
    stopped = stop_all_running_instances(dry_run=True)
    print('Found running instances (dry run):', stopped)
