import boto3
import paramiko
import time
import os
import json

region = 'eu-west-3'
client = boto3.client('ec2')

client = boto3.client('cloudwatch', region_name='eu-west-3')
client.put_metric_alarm(
    AlarmName='trueestcasser',
    AlarmDescription='tu tombe ou pas dans le true',
    ComparisonOperator='GreaterThanOrEqualToThreshold',
    Threshold=5,
    MetricName='Invocations',
    Namespace='AWS/Lambda',
    Period=60,
    Unit='Count',
    Statistic='Sum',
    EvaluationPeriods=1,
    Dimensions=[
        {
            'Name':'FonctionName',
            'Value':'trueestcasser',
        }
    ]
)
def create_lambda_function():
    # AWS configurations
    aws_region = 'eu-west-3'
    lambda_function_name = 'trueestcasser'
    role_name = 'arn:aws:iam::290752420795:user/hugo'  # Replace this with your role name or ARN


    # Read the Lambda function code from the zip file
    with open('login/trueorfalse.zip', 'rb') as f:
        zip_file_data = f.read()

    # Create the Lambda function using Boto3
    lambda_client = boto3.client('lambda', region_name=aws_region)

    response = lambda_client.create_function(
        FunctionName=lambda_function_name,
        Runtime='python3.8',
        Role='arn:aws:iam::290752420795:role/impot',
        Handler='trueorfalse.trueorfalse',
        Code={
            'ZipFile': zip_file_data
        },
    )

    # Print the ARN of the created Lambda function
    print('Lambda Function ARN:', response['FunctionArn'])

def ivoke_lambda_function():
    aws_region = 'eu-west-3'
    lambda_function_name = 'trueestcasser'
    lambda_client = boto3.client('lambda', region_name=aws_region)
    response = lambda_client.invoke(
        FunctionName=lambda_function_name,
        InvocationType='RequestResponse',
        Payload=b'{"key1":true}'
    )
    print(response['Payload'].read())

def create_S3():
    s3 = boto3.client('s3')
    region = 'eu-west-3'
    datas = s3.create_bucket(
        Bucket='tyjonnesbucket',
        acl='public-read',
        CreateBucketConfiguration={
            'LocationConstraint': region
        })
    return datas

def create_bucket_uniq():
    s3 = boto3.client('s3')
    region = 'eu-west-3'
    datas = s3.create_bucket(
        Bucket='tyjonnesbucket13470issou',
        acl='public-read',
        CreateBucketConfiguration={
            'LocationConstraint': region
        })
    return datas

def upload_S3():
    s3 = boto3.client('s3')
    data = s3.upload_file('file.txt', 'tyjonnesbucket', 'file.txt')
    return data

def upload_uniq_S3():
    s3 = boto3.client('s3')
    data = s3.upload_file('file.txt', 'tyjonnesbucket', 'file.txt', ExtraArgs={'ACL': 'public-read'})
    return data

def download_S3():
    s3 = boto3.client('s3')
    datas = s3.download_file('tyjonnesbucket', 'file.txt', 'file.txt')
    return datas

def list_files_S3():
    s3 = boto3.client('s3')
    datas = s3.list_objects(Bucket='tyjonnesbucket')
    return datas

def remove_files_S3():
    s3 = boto3.client('s3')
    datas = s3.delete_object(Bucket='tyjonnesbucket', Key='file.txt')
    return datas

def remove_bucket_S3():
    s3 = boto3.client('s3')
    datas = s3.delete_bucket(Bucket='tyjonnesbucket')
    return datas

def create_vpc():
    ec2_client = boto3.client('ec2')
    response = ec2_client.create_vpc(
        CidrBlock='10.66.0.0/27',
    )
    return response


def create_security_group(vpcid):
    response = client.create_security_group(
    Description="moumoumouette",
    GroupName='Security66mais42',
    VpcId=vpcid,
)
    GroupId=response['GroupId']
    return response, GroupId

def create_subnet(vpc):
    ec2_client = boto3.client('ec2')
    CidrBlocks = ['10.66.0.0/28','10.66.0.17/28']
    vpcid = vpc.get('Vpc', {}).get('VpcId')
    for CidrBlock in CidrBlocks:
        response = ec2_client.create_subnet(
            CidrBlock=CidrBlock,
            VpcId=vpcid,
        )
    return response
    
def create_internet_gateway(vpcid):
    response = client.create_internet_gateway()
    internet_gateway_id = response['InternetGateway']['InternetGatewayId']
    response = client.attach_internet_gateway(
        InternetGatewayId=internet_gateway_id,
        VpcId=vpcid,
    )
    return response, internet_gateway_id

def load_balancer(sub,vpc,secugrp):
    
    # target_group = elb_create_target_group('unbiased-coder-target-group', vpc_id)
    # target_group_arn = target_group['TargetGroups'][0]['TargetGroupArn']


    elb_client = boto3.client('elbv2')
    targetGrp = elb_client.create_target_group(
        Name='tyjonnes-targets',
        Protocol='HTTP',
        Port=80,
        VpcId=vpc,
    )

    response = elb_client.create_load_balancer(
        Name='my-load-balancer',
        Subnets=[
            sub,
        ],
        SecurityGroups=[
            secugrp,
        ],
        Scheme='internet-facing',
        Tags=[
            {
                'Key': 'Name',
                'Value': 'tyjonnes-load-balancer'
            },
        ]
    )

    return response, targetGrp

def create_network():
    vpc = create_vpc()
    subnet = create_subnet(vpc)
    subid = subnet.get('Subnet', {}).get('SubnetId')
    vpcid = vpc.get('Vpc', {}).get('VpcId')
    
    gatewayId = create_internet_gateway(vpcid)[1]
    secugroup = create_security_group(vpcid)
    load_balancer(subid,vpcid,secugroup)
    response = client.describe_route_tables(
        Filters=[
        {
            "Name": "vpc-id",
            'Values': [vpcid]
        }
        ]
    )
    route_table_id = response['RouteTables'][0]['RouteTableId']
    response = client.create_route(
    DestinationCidrBlock="0.0.0.0/0",
    RouteTableId=route_table_id,
    GatewayId=gatewayId,  # Replace this with the specific target you want to use
)
      
    return vpc,subnet,gatewayId

def create_ec2_instance():
    # Set AWS region
      

    # Create a Boto3 EC2 client
    ec2_client = boto3.client('ec2', region_name=region)

    # details de l'instance 
    instance_params = {
        'ImageId': 'ami-05b5a865c3579bbc4',   # Replace with the desired AMI ID
        'count': 1, # You can specify more than one instances
        'InstanceType': 't2.micro',  # Replace with the desired instance type
        'KeyName': 'tyjonneskey',  # Replace with the name of your EC2 key pair
        'SecurityGroupIds': [GroupId],  # Replace with the desired security group ID(s)
        'subnetId': 'subnetid',  # Replace with the desired subnet ID
        'MinCount': 1,
        'MaxCount': 1
    }

    # Launch the EC2 instance
    response = ec2_client.run_instances(**instance_params)

    # Get the instance ID of the newly created instance
    instance_id = response['Instances'][0]['InstanceId']

    print(f"EC2 instance with ID {instance_id} is being deployed.")


def wait_for_ssh(instance_id, key_path):
    ec2_client = boto3.client('ec2')

    while True:
        response = ec2_client.describe_instances(InstanceIds=[instance_id])
        state = response['Reservations'][0]['Instances'][0]['State']['Name']
        if state == 'running':
            break
        time.sleep(5)

    print("Instance is running. Waiting for SSH availability...")
    time.sleep(30)  # Give some time for SSH to be ready

    # Connect to the instance via SSH
    instance = response['Reservations'][0]['Instances'][0]
    public_ip = instance['PublicIpAddress']

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Replace 'your-key.pem' with the path to your private key file
    key = paramiko.RSAKey.from_private_key_file(key_path)
    ssh_client.connect(hostname=public_ip, username='ec2-user', pkey=key)

    return ssh_client

def call_ec2() :
    create_ec2_instance()
    wait_for_ssh()

def call_lambda():
    create_lambda_function()
    ivoke_lambda_function()
    
def call_s3() : 
    create_S3()