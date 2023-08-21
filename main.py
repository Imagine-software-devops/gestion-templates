import json
import os
import boto3
import distro
# from aws_setup import *
import requests
import platform
import subprocess

# verifie le type d'instalation
# celon le PC redefini les commandes pour les faire fonctionner 
# return 0 si ok 1+error si echec ou problem
def install_instance(appName,typeOfInstall,path,commandsToExecute,vsInstall,jsonConfig,jsonConfigPath):
        if typeOfInstall == "PC":
                # pathInstall = path
                platform = platform.system()
                if vsInstall == 'yes':
                        vscode_install(platform)
                execute_and_log(f'cd' + path)
                if jsonConfig == 'yes':
                        json_npm_config(jsonConfigPath,platform,path)
                execute_commands(commandsToExecute,platform,appName)
        else:
                return "aws pas encore pris en charge"
                call_aws_function()            


# Appel des fonction de aws dans le fichier aws_setup
# def call_aws_function() :
#         # creation + connection ec2 manque la gestion des params pour fonctionnement
#         call_ec2()
#         # lambda creation + alarm :  manque la gestion des params pour fonctionnement
#         call_lambda()
#         # network creation : manque gestions des params pour fonctionnement
#         create_network()
#         # create s3 + uniq bucket : manque gestion des params pour fonctionnement
#         call_s3()

# json config installation celon le systeme d'exploitation
# install nodejs npm 
# maybe add if folder not exist create folder

def execute_and_log(command, log_file):
    try:
        output = subprocess.check_output(command, shell=True, text=True)
        log_file.write(f'{command}\n')
        log_file.write(output)
        log_file.write('\n')
        return True
    except subprocess.CalledProcessError as e:
        log_file.write(f'Error executing command: {command}\n')
        log_file.write(f'Error message: {e}\n')
        log_file.write('\n')
        return False

def json_npm_config(jsonConfigPath, plateform, path):
        if execute_and_log('cp ' + jsonConfigPath + ' ' + path, log_file):    
            if plateform == "Linux":
                if distro.name() == 'Manjaro Linux':
                    if execute_and_log('sudo pacman -S nodejs npm', log_file):
                        execute_and_log('npm install', log_file)
                        return 0
                    else:
                        return 1, "Error installing Manjaro dependencies"
                if distro.name() == 'Ubuntu':
                    if execute_and_log('sudo apt install nodejs', log_file) and \
                       execute_and_log('sudo apt install npm', log_file):
                        execute_and_log('npm install', log_file)
                        return 0
                    else:
                        return 1, "Error installing Ubuntu dependencies"
            if plateform == "Windows":
                if execute_and_log('choco install nodejs', log_file) and \
                   execute_and_log('choco install npm', log_file):
                    execute_and_log('npm install', log_file)
                    return 0
                else:
                    return 1, "Error installing Windows dependencies"
            if plateform == "Darwin":
                if execute_and_log('brew install nodejs', log_file) and \
                   execute_and_log('brew install npm', log_file):
                    execute_and_log('npm install', log_file)
                    return 0
                else:
                    return 1, "Error installing Darwin dependencies"
        else:
            return 1, "Error copying config file"


# VScode intallation celon le systeme d'exploitation
def vscode_install(plateform, log_file_path):
    with open(log_file_path, 'a') as log_file:
        if plateform == "Linux":
            if distro.name() == 'Manjaro Linux':
                if execute_and_log('sudo pacman -S --needed git base-devel', log_file) and \
                   execute_and_log('git clone https://aur.archlinux.org/visual-studio-code-bin.git', log_file):
                    if execute_and_log('cd visual-studio-code-bin', log_file) and \
                       execute_and_log('makepkg -si', log_file):
                        return 0
                    else:
                        return 1, "Error building VSCode package"
                else:
                    return 1, "Error installing Manjaro dependencies"
                # yarn curl 
            if distro.name() == 'Ubuntu':
                if execute_and_log('sudo apt install git', log_file) and \
                   execute_and_log('sudo apt install make', log_file) and \
                   execute_and_log('sudo apt install visual-studio-code', log_file):
                    return 0
                else:
                    return 1, "Error installing Ubuntu dependencies"
        if plateform == "Windows":
            if execute_and_log('choco install git', log_file) and \
               execute_and_log('choco install make', log_file) and \
               execute_and_log('choco install visual-studio-code', log_file):
                return 0
            else:
                return 1, "Error installing Windows dependencies"
        if plateform == "Darwin":
            if execute_and_log('brew install git', log_file) and \
               execute_and_log('brew install make', log_file) and \
               execute_and_log('brew cask install visual-studio-code', log_file):
                return 0
            else:
                return 1, "Error installing Darwin dependencies"
    
        return 1, "Unsupported platform"


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
        # languagesDatas=['angular']
        # print(languagesDatas)
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
                        if platform == "Linux":
                                if distro.name() == 'Manjaro Linux':
                                        toExecute = toExecute.replace("sudo apt install", "sudo pacman -S")
                                        if execute_and_log(toExecute, log_file) :
                                                return 0
                                        else :
                                                return 1, "error executing Manjaro commands"
                                if distro.name() == 'Ubuntu':
                                        if execute_and_log(toExecute, log_file) :
                                                return 0
                                        else :
                                                return 1, "error executing Ubuntu commands"
                        if platform == "Windows":
                                toExecute = toExecute.replace("sudo apt install", "choco install")
                                if execute_and_log(toExecute, log_file) :
                                        return 0
                                else :
                                        return 1, "error executing Windows commands"
                        if platform == "Darwin":
                                toExecute = toExecute.replace("sudo apt install", "brew install")
                                if execute_and_log(toExecute, log_file) :
                                        return 0
                                else :
                                        return 1, "error executing Darwin commands"
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

def docker_install():
    if platform.system() == 'Linux':
        if distro.name() == 'Manjaro Linux':
                if execute_and_log('sudo pacman -S docker', log_file) :
                     return 0
                else :
                    return 1, "error installing docker"
        if distro.name() == 'Ubuntu':
             if execute_and_log('sudo apt-get update', log_file) and \
             execute_and_log('sudo apt install docker.io', log_file) :
                    return 0
             else :
                    return 1, "error installing docker"
        if platform.system() == 'Windows':
            if execute_and_log('choco install docker', log_file) :
                return 0
            else :
                return 1, "error installing docker"
        if platform.system() == 'Darwin':
            if execute_and_log('brew install docker', log_file) :
                return 0
            else :
                return 1, "error installing docker"



# main ou apppel des fonction dans le bon ordre
# mintlify
if __name__ == '__main__':
        pth = os.path.abspath("json/front_datas.json")
        logpth = os.path.abspath("logs/log.txt")
        with open(pth) as json_file:
                jsonData = json.load(json_file)
        sortedDatas =sort_datas(jsonData)   
        commandsToExecute = get_commands(sortedDatas[4])
        with open(logpth, 'a') as log_file:
                # execute_commands(commandsToExecute,"",sortedDatas[0],logpth)
                install_instance(sortedDatas[0],sortedDatas[1],sortedDatas[2],sortedDatas[3],commandsToExecute,sortedDatas[5],sortedDatas[6],sortedDatas[7])