import json
import os
import boto3
import distro
# from aws_setup import *
import requests
import platform
import subprocess

def install_instance(appName,typeOfInstall,path,commandsToExecute,vsInstall,jsonConfig,jsonConfigPath,dockerInstall):
        """
        The function `install_instance` installs an application instance based on the specified parameters,
        including the type of installation, path, commands to execute, Visual Studio installation, JSON
        configuration, and JSON configuration path.
        
        :param appName: The name of the application you want to install
        :param typeOfInstall: The parameter "typeOfInstall" is a string that specifies the type of
        installation. It can be either "PC" or something else (e.g., "AWS")
        :param path: The `path` parameter is the path where the installation will take place. It is the
        directory where the application will be installed or deployed
        :param commandsToExecute: The `commandsToExecute` parameter is a list of commands that you want to
        execute during the installation process. Each command in the list should be a string
        :param vsInstall: The `vsInstall` parameter is a string that specifies whether Visual Studio Code
        should be installed. It can have two possible values: "yes" or any other value. If it is set to
        "yes", the `vscode_install` function will be called to install Visual Studio Code
        :param jsonConfig: The parameter "jsonConfig" is a flag that indicates whether or not to use a JSON
        configuration file for the installation. If the value is "yes", then a JSON configuration file will
        be used. If the value is "no", then a JSON configuration file will not be used
        :param jsonConfigPath: The `jsonConfigPath` parameter is the path to the JSON configuration file
        that will be used for the installation
        :return: the string "aws pas encore pris en charge".
        """
        if typeOfInstall == "PC":
                # pathInstall = path
                platform = platform.system()
                if vsInstall == 'yes':
                        vscode_install(platform)
                execute_and_log(f'cd' + path)
                if jsonConfig == 'yes':
                        json_npm_config(jsonConfigPath,platform,path)
                if dockerInstall == 'yes':
                    docker_install(platform)
                execute_commands(commandsToExecute,platform,appName)
        else:
                return "aws pas encore pris en charge"
                call_aws_function()            


def execute_and_log(command, log_file):
    """
    The function `execute_and_log` executes a command and logs the command and its output or any errors
    to a log file.
    
    :param command: The `command` parameter is a string that represents the command you want to execute.
    It can be any valid shell command that you would normally run in a terminal
    :param log_file: The `log_file` parameter is the file object that represents the log file where you
    want to write the command and its output or error message. It should be opened in write mode before
    passing it to the `execute_and_log` function
    :return: The function `execute_and_log` returns a boolean value. It returns `True` if the command is
    executed successfully without any errors, and it returns `False` if there is an error executing the
    command.
    """
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
        """
        The function `json_npm_config` copies a JSON config file to a specified path and installs the
        necessary dependencies based on the platform (Linux, Windows, or Darwin) using npm.
        
        :param jsonConfigPath: The `jsonConfigPath` parameter is the path to the JSON configuration file
        that needs to be copied to the specified `path`
        :param plateform: The "plateform" parameter represents the platform on which the code is being
        executed. It can have one of the following values: "Linux", "Windows", or "Darwin" (for macOS)
        :param path: The `path` parameter is the destination path where the `jsonConfigPath` file will be
        copied to
        :return: either a single value of 0 or a tuple containing an error code (1) and an error message.
        """
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

def vscode_install(plateform, log_file_path):
    """
    The function `vscode_install` installs Visual Studio Code on different platforms and logs the
    installation process.
    
    :param plateform: The "platform" parameter specifies the operating system platform on which you want
    to install Visual Studio Code. It can have one of the following values: "Linux", "Windows", or
    "Darwin" (for macOS)
    :param log_file_path: The `log_file_path` parameter is the path to the log file where the
    installation process will be logged. This file will be opened in append mode, so any existing
    content will be preserved and new logs will be added to the end of the file
    :return: The function `vscode_install` returns a tuple. The first element of the tuple is an integer
    indicating the status of the installation process. A value of 0 indicates a successful installation,
    while a value of 1 indicates an error occurred during the installation.
    """
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


def vscode_extensions_install(plateform,profileVsCode):
        return 0

def get_commands(languagesDatas):
        """
        The function `get_commands` takes a list of language data as input, reads a JSON file containing
        commands, and returns a list of commands corresponding to the languages in the input data.
        
        :param languagesDatas: The parameter "languagesDatas" is expected to be a list of languages
        :return: a list of commands to execute based on the input languagesDatas.
        """
        commandsToExecute = []
        pth = os.path.abspath("json/config.json")
        print(pth)
        with open(pth) as json_file:
                jsoncommands = json.load(json_file)
        for language in languagesDatas:      
                commandsToExecute.append(jsoncommands[language])        
        return commandsToExecute

def execute_commands(commandsToExecute,platform,app_name):
    """
    The function `execute_commands` takes a list of commands to execute, a platform, and an app name,
    and executes the commands based on the platform, replacing certain strings in the commands as
    needed.
    
    :param commandsToExecute: The `commandsToExecute` parameter is a list of lists. Each inner list
    contains a set of commands to be executed
    :param platform: The "platform" parameter represents the operating system platform on which the
    commands will be executed. It can have one of the following values: "Linux", "Windows", or "Darwin"
    (for macOS)
    :param app_name: The `app_name` parameter is a string that represents the name of the application
    you want to install or execute commands for. It is used to replace the "{app-name}" placeholder in
    the commands that need to be executed
    :return: either 0 or a tuple containing 1 and an error message.
    """
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
                                

def sort_datas(jsonData):
    """
    The function `sort_datas` extracts specific data from a JSON object and returns them as individual
    variables.
    
    :param jsonData: jsonData is a JSON object that contains various parameters for a module
    :return: the following values in order: appName, typeOfInstall, pathOfInstall, awsDatas,
    languagesDatas, vsInstall, jsonConfig, jsonConfigPath.
    """
    appName = jsonData["nom-module"]["actions"][0]["params"]['app-name']
    typeOfInstall = jsonData["nom-module"]["actions"][0]["params"]['type-of-install']
    pathOfInstall = jsonData["nom-module"]["actions"][0]["params"]['path-of-install']
    awsDatas= jsonData["nom-module"]["actions"][0]["params"]['server-datas']
    languagesDatas = jsonData["nom-module"]["actions"][0]["params"]['which-language']
    vsInstall = jsonData["nom-module"]["actions"][0]["params"]['vscode']
    jsonConfig = jsonData["nom-module"]["actions"][0]["params"]['json-config']
    jsonConfigPath = jsonData["nom-module"]["actions"][0]["params"]['json-config-path']
    dockerInstall = jsonData["nom-module"]["actions"][0]["params"]['docker-install']
    return appName,typeOfInstall,pathOfInstall,awsDatas,languagesDatas,vsInstall,jsonConfig,jsonConfigPath,dockerInstall

def docker_install(plateform):
    """
    The function `docker_install` installs Docker based on the operating system (Linux, Windows, or
    macOS) using the appropriate package manager or command.
    :return: The function `docker_install()` returns either 0 or a tuple containing an error code and an
    error message.
    """
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

# The above code is a Python script that performs the following actions:
if __name__ == '__main__':
        pth = os.path.abspath("json/front_datas.json")
        logpth = os.path.abspath("logs/log.txt")
        with open(pth) as json_file:
                jsonData = json.load(json_file)
        sortedDatas =sort_datas(jsonData)   
        commandsToExecute = get_commands(sortedDatas[4])
        with open(logpth, 'a') as log_file:
                install_instance(sortedDatas[0],sortedDatas[1],sortedDatas[2],sortedDatas[3],commandsToExecute,sortedDatas[5],sortedDatas[6],sortedDatas[7],sortedDatas[8])