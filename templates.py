import boto3
import paramiko
import time
import json

def create_ec2_instance():
    # Set AWS region
    region = 'us-west-2'  

    # Create a Boto3 EC2 client
    ec2_client = boto3.client('ec2', region_name=region)

    # details de l'instance 
    instance_params = {
        'ImageId': 'ami-xxxxxxxx',   # Replace with the desired AMI ID
        'InstanceType': 't2.micro',  # Replace with the desired instance type
        'KeyName': 'your-key-pair',  # Replace with the name of your EC2 key pair
        'SecurityGroupIds': ['sg-xxxxxxxx'],  # Replace with the desired security group ID(s)
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

def execute_commands(ssh_client):
    for command in commands:
        print(f"Executing command: {command}")
        stdin, stdout, stderr = ssh_client.exec_command(command)
        print(stdout.read().decode())
        print(stderr.read().decode())

    ssh_client.close()

if __name__ == '__main__':
    create_ec2_instance()
    key_path = '/path/to/your-key.pem'
    instance_id = '<your-instance-id>'
    ssh_client = wait_for_ssh(instance_id, key_path)

    with open('nomDuJson') as f:
        commands_data = json.load(f)
        commands_to_execute = commands_data['commands']

    execute_commands(ssh_client, commands_to_execute)