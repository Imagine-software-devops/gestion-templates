import json
import os
from aws_setup import *
import requests

def install_instance(machine,path,commandsToExecute):
        if machine == "PC":
                # install on user's pc
                pathInstall = path
                os.system("cd "+pathInstall)
                # execute the commands
                execute_commands(commandsToExecute)
        else:
                # create the instance in aws 
                #commands to execute == json data
                print()

def get_configs(languagedatas):
        # get datas from an s3 bucket or ec2 to get the differents configs file for the installation
        # return a json file with all the datas
        api_url = "enter api url here"
        try:
        # Send a GET request to the API endpoint
                response = requests.get(api_url)
        # Check if the request was successful (status code 200)
                if response.status_code == 200:
                # Parse the JSON response
                        data = response.json()
                        print("API Response:")
                        print(data)
                else:
                        print(f"Failed to call API. Status code: {response.status_code}")
                        print("Error Response:")
                        print(response.text)
        except requests.exceptions.RequestException as e:
                print("Error: Failed to make the API request.")
                print(e)



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
                

        