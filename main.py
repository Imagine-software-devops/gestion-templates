import json
import os
from aws_setup import *

def install_instance(machine,path,):
        if machine == "PC":
                pathInstall = path
                os.system("cd "+pathInstall)
        else:
                create_ec2_instance()
                key_path = 'json data'
                instance_id = 'json data'
                ssh_client = wait_for_ssh(instance_id, key_path)
                execute_commands(ssh_client, commands_to_execute)#commands to execute == json data


if __name__ == '__main__':

                

        