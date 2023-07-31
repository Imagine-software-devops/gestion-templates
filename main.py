import json
import os
from aws_setup import *

def install_instance(machine,path,commandsToExecute):
        if machine == "PC":
                # install on user's pc
                pathInstall = path
                os.system("cd "+pathInstall)
                # execute the commands
                execute_commands(commandsToExecute)
        else:
                # create the instance in aws 
                create_ec2_instance()
                key_path = 'json data'
                instance_id = 'json data'
                ssh_client = wait_for_ssh(instance_id, key_path)
                execute_commands_aws(ssh_client, commandsToExecute)#commands to execute == json data

def get_configs(languagedatas):
        # get datas from an s3 bucket or ec2 to get the differents configs file for the installation
        # return a json file with all the datas
        return json

def execute_commands(commandsToExecute):
        # execute the commands
        return commandsToExecute

def sort_datas(jsonData):
        # parse the entry data to get the differents type of instalation
        # parse the entry data to get the differents type of machine
        # call get_configs(languagedatas) to get the differents configs file for the installation
        # return a json file with all the datas to execute
        return jsonData

if __name__ == '__main__':
        # get the json file with all the user entries
        jsonData = json.loads('monfichier.json') 
        sortedDatas =sort_datas(jsonData)
        install_instance(machine,path,commandsToExecute)
                

        