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
def install_instance(appName,typeOfInstall,path,aws,commandsToExecute,vsInstall,jsonConfig,jsonConfigPath):
        if typeOfInstall == "PC":
                pathInstall = path
                platform = platform.system()
                if vsInstall == 'yes':
                        vscode_install(platform)
                os.system(f'cd' + path)
                if jsonConfig == 'yes':
                        json_config(jsonConfigPath,platform,path)
                execute_commands(commandsToExecute,platform,appName)
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

# json config installation celon le systeme d'exploitation
# install nodejs npm 
# maybe add if folder not exist create folder
def json_config(jsonConfigPath,plateform,path):
        os.system("cp"+jsonConfigPath + path)
        if plateform == "Linux":
                try : 
                        os.system('sudo pacman -S nodejs npm')
                        os.system('npm install')
                        return 0
                except OSError as e:
                        print("error installing dependencies")
                        return 1,e
        if plateform == "Windows":
                try :
                        os.system('choco install nodejs')
                        os.system('choco install npm')
                        os.system('npm install')
                        return 0
                except OSError as e:
                        print("error installing dependencies")
                        return 1,e
        if plateform == "Darwin":
                try :
                        os.system('brew install nodejs')
                        os.system('brew install npm')
                        os.system('npm install')
                        return 0
                except OSError as e:
                        print("error installing dependencies")
                        return 1,e
        


# VScode intallation celon le systeme d'exploitation
def vscode_install(plateform):
        if plateform == "Linux":
                try : 
                        os.system('sudo pacman -S --needed git base-devel')
                        os.system('git clone https://aur.archlinux.org/visual-studio-code-bin.git')
                        os.system('cd visual-studio-code-bin')
                        os.system('makepkg -si')
                        return 0
                except OSError as e:
                        print("error while installing vscode")
                        return 1,e
        if plateform == "Windows":
                try :
                        os.system('choco install git')
                        os.system('choco install make')
                        os.system('choco install visual-studio-code')
                        return 0
                except OSError as e:
                        print("error while installing vscode")
                        return 1,e
        if plateform == "Darwin":
                try :
                        os.system('brew install git')
                        os.system('brew install make')
                        os.system('brew cask install visual-studio-code')
                        return 0
                except OSError as e:
                        print("error while installing vscode")
                        return 1,e


# Need to find settings.json path
def vscode_extensions_install(plateform,profileVsCode):
        return 0

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
def execute_commands(commandsToExecute,platform,app_name):
        # execute the commands
        for commands in commandsToExecute:
                for command in commands:
                        toExecute = command.replace("{app-name}", app_name)
                        try :
                                os.system(toExecute)                               
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
        vsInstall = jsonData["nom-module"]["actions"][0]["params"]['vscode']
        jsonConfig = jsonData["nom-module"]["actions"][0]["params"]['json-config']
        jsonConfigPath = jsonData["nom-module"]["actions"][0]["params"]['json-config-path']
        return appName,typeOfInstall,pathOfInstall,awsDatas,languagesDatas,vsInstall,jsonConfig,jsonConfigPath

# main ou apppel des fonction dans le bon ordre
if __name__ == '__main__':
        pth = os.path.abspath("json/front_datas.json")
        with open(pth) as json_file:
                jsonData = json.load(json_file)
        sortedDatas =sort_datas(jsonData)   
        commandsToExecute = get_commands(sortedDatas[4])
        # execute_commands(commandsToExecute,"",sortedDatas[0])
        install_instance(sortedDatas[0],sortedDatas[1],sortedDatas[2],sortedDatas[3],commandsToExecute,sortedDatas[5],sortedDatas[6],sortedDatas[7])
                

        