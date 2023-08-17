import json
import os
import boto3
# from aws_setup import *
import requests
import platform
import subprocess

# verifie le type d'instalation
# celon le PC redefini les commandes pour les faire fonctionner 
# return 0 si ok 1+error si echec ou problem
def install_instance(appName,typeOfInstall,path,aws,commandsToExecute):
        if typeOfInstall == "PC":
                pathInstall = path
                platform = platform.system()
                os.system(f'cd' + path)
                if platform == "Windows":
                        return 'Windows pas encore pris en charge'
                        execute_commands(appName,commandsToExecute)
                elif platform == "Linux":
                        return execute_commands(appName,commandsToExecute)
                elif platform == "Darwin":
                        return 'Darwin pas encore pris en charge'
                        execute_commands(appName,commandsToExecute)
                else:
                        return 1,'error while getting the platform'

        else:
                return "aws pas encore pris en charge"
                call_aws_function()            


# Appel des fonction de aws dans le fichier aws_setup
def call_aws_function() :
        # creation + connection ec2 manque la gestion des params pour fonctionnement
        call_ec2()
        # lambda creation + alarm :  manque la gestion des params pour fonctionnement
        call_lambda()
        # network creation : manque gestions des params pour fonctionnement
        create_network()
        # create s3 + uniq bucket : manque gestion des params pour fonctionnement
        call_s3()

# recupere dans le fichier config les languages et leurs commandes d'installation
# push les commands dans un array de format :
# [
#       angular : 'npm i .....',
#       python : 'npm i ......'
# ]
def get_commands(languagesDatas):
        languagesDatas=['angular']
        print(languagesDatas)
        commandsToExecute = []
        pth = os.path.abspath("json/config.json")
        print(pth)
        with open(pth) as json_file:
                jsoncommands = json.load(json_file)
        for language in languagesDatas:      
                commandsToExecute.append(jsoncommands[language])        
        return commandsToExecute

# execute la liste de commandes
def execute_commands(commandsToExecute):
        # execute the commands
        for commands in commandsToExecute:
                for command in commands:
                        try :
                                os.system(command)
                                return 0
                        except OSError as e:
                                print("error while executing the command")
                                return 1,e
                
# try des données d'entrées
def sort_datas(jsonData):
        appName = jsonData["nom-module"]["actions"][0]["params"]['app-name']
        typeOfInstall = jsonData["nom-module"]["actions"][0]["params"]['type-of-install']
        pathOfInstall = jsonData["nom-module"]["actions"][0]["params"]['path-of-install']
        # if typeOfInstall == "aws":
        awsDatas= jsonData["nom-module"]["actions"][0]["params"]['server-datas']
        languagesDatas = jsonData["nom-module"]["actions"][0]["params"]['which-language']
        return appName,typeOfInstall,pathOfInstall,awsDatas,languagesDatas

# main ou apppel des fonction dans le bon ordre
if __name__ == '__main__':
        pth = os.path.abspath("json/front_datas.json")
        with open(pth) as json_file:
                jsonData = json.load(json_file)
        sortedDatas =sort_datas(jsonData)       
        commandsToExecute = get_commands(sortedDatas[4])
        execute_commands(commandsToExecute)
        install_instance(sortedDatas[0],sortedDatas[1],sortedDatas[2],sortedDatas[3],commandsToExecute)
                

        