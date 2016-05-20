#!/usr/bin/python
# -*- coding: utf-8 -*-

from prettytable import PrettyTable

import boto3

def get_unused_iam_ec2_role():

    iam_client = boto3.client('iam')
      
    unused_role_list = []
    iam_roles_profile_arn = []
    ec2_roles_profile_arn = []

    for r in iam_client.list_instance_profiles()['InstanceProfiles']:
        try:
            if r['Roles'][0]['AssumeRolePolicyDocument']['Statement'][0]['Principal'] != None and r['Roles'][0]['AssumeRolePolicyDocument']['Statement'][0]['Principal']['Service'] == 'ec2.amazonaws.com':
                iam_roles_profile_arn.append(r['Arn'])
            elif r['Roles'][0]['AssumeRolePolicyDocument']['Statement'][0]['Principal']['Service'] != None:
                print r['Arn']
            else:
                print r['Arn']
        except KeyError:
            print r['Arn']
                
    region_names = [x['RegionName'] for x in boto3.client('ec2').describe_regions()['Regions']]
    for region_name in region_names:
        
        ec2_res = boto3.resource('ec2', region_name)
    
        for i in ec2_res.instances.all():
            if i.iam_instance_profile != None:
                ec2_roles_profile_arn.append(i.iam_instance_profile['Arn'])

    iam_roles_profile_arn.sort()
    ec2_roles_profile_arn.sort()
            
    unused_role_profile_arn = set(iam_roles_profile_arn) - set(ec2_roles_profile_arn)
    
    pt = PrettyTable(['Name'])
    pt.align["Name"] = "l"
    pt.sortby = 'Name'
    
    for role in unused_role_profile_arn:
        pt.add_row([role])
    
    print pt

if __name__ == '__main__':
    get_unused_iam_ec2_role()