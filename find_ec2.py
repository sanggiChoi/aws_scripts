from datetime import datetime, timedelta
from prettytable import PrettyTable

import boto3

RETENTION_DAY = 180

def find_old_running_instance(region_name):
    """
    A tool for retrieving basic information from the running EC2 instances.
    """
    now = datetime.now()
    timegap = timedelta(days = RETENTION_DAY)
    day_ago = now - timegap

    # Connect to EC2
    ec2 = boto3.resource('ec2', region_name)

    # Get information for all running instances
    running_instances = ec2.instances.filter(Filters=[{
                            'Name': 'instance-state-name',
                            'Values': ['running']}])

    pt = PrettyTable(['Name', 'Type', 'State', 'Launch Time'])
    pt.align["Name"] = "l"  # Left align city names
    pt.sortby = 'Launch Time'

    for instance in running_instances:
        for tag in instance.tags:
            if 'Name'in tag['Key']:
                name = tag['Value']
    
        launch_date = instance.launch_time.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        #launch_date = datetime.strptime(instance.launch_time, "%Y-%m-%dT%H:%M:%S.000Z")
    
        # Add instance info to a dictionary
        if launch_date < unicode(day_ago):
            #t.add_row(name, instance.instance_type, instance.state['Name'], unicode(instance.launch_time))
            pt.add_row([name, instance.instance_type, instance.state['Name'], unicode(instance.launch_time)])

    #pt.printt(sortby="Launch Time")
    print pt
    
def find_running_instance(region_name):
    """
    A tool for retrieving basic information from the running EC2 instances.
    """
    # Connect to EC2
    ec2 = boto3.resource('ec2', region_name)

    # Get information for all running instances
    running_instances = ec2.instances.filter(Filters=[{
                            'Name': 'instance-state-name',
                            'Values': ['running']}])

    pt = PrettyTable(['Name', 'Type', 'OS', 'Role', 'Private IP', 'Public IP'])
    pt.align["Name"] = "l"  # Left align
    pt.align["Type"] = "l"  # Left align
    pt.align["Private IP"] = "l"  # Left align
    pt.align["Public IP"] = "l"  # Left align
    pt.sortby = 'Name'

    for instance in running_instances:
        if instance.instance_lifecycle == 'spot':
            continue
        
        for tag in instance.tags:
            if tag['Key'] == 'Name':
                name = tag['Value']
            
            if tag['Key'] == 'Role':
                role = tag['Value']
        
        platform = instance.platform        
        if platform == None:
            platform = 'Linux'
    
        pt.add_row([name, instance.instance_type, platform, role, instance.private_ip_address, instance.public_ip_address])
    if(len(pt._rows) > 0):
        print region_name
        print pt

if __name__ == '__main__':
    region_names = [x['RegionName'] for x in boto3.client('ec2').describe_regions()['Regions']]
    for region_name in region_names:
        find_running_instance(region_name)
        #find_old_running_instance(region_name)
