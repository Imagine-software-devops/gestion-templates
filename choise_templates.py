import inquirer
from inquirer.themes import GreenPassion

def main_choice() :
        choix = [
        inquirer.Checkbox(
            "actions",
            message="ou voulez vous effectuer l'instalation",
            choices=["Ce pc", "AWS",],
        ),
    ]
        choices = inquirer.prompt(choix, theme=GreenPassion())
        return choices

def language_choice() :
        choix = [
        inquirer.Checkbox(
            "actions",
            message="Quel languages voulez vous installer ?",
            choices=["Python", "Bash","angularjs","vuejs","symfony","C#","Java","PHP","C++","C","HTML","CSS","Javascript","React","Nodejs","Laravel","Spring","Express","Bootstrap","Swift","React-Native"]
        ),
    ]
        choices = inquirer.prompt(choix, theme=GreenPassion())
        return choices

def docker_choice():
        choix = [
        inquirer.Checkbox(
            "actions",
            message="Quel type de projet voulez vous faire",
            choices=["Dockerfile", "docker-compose","docker-swarm","docker-machine","none"],
        ),
    ]
        choices = inquirer.prompt(choix, theme=GreenPassion())
        return choices

def visual_studio_code_install():
        choix = [
              inquirer.Checkbox(
                          "actions",
            message="Voulez vous installer visual studio code ?",
            choices=["oui", "non"],

              )
       ]
        choices = inquirer.prompt(choix, theme=GreenPassion())
        return choices

def visual_studio_code_extension():
        choix = [
        inquirer.Checkbox(
            "actions",
            message="Voulez vous importer votre gonfig visual ?",
            choices=["oui", "non"],
        ),
    ]
        choices = inquirer.prompt(choix, theme=GreenPassion())
        return choices

def visual_config():
        choix = [
        inquirer.Text(
            "actions",
            message="lien de votre config visual studio code",
        ),
    ]
        choices = inquirer.prompt(choix, theme=GreenPassion())
        return choices
       

def git_link():
        choix = [
        inquirer.Checkbox(
            "actions",
            message="voulez vous link votre git",
            choices=["oui", "non"],
        ),
    ]
        choices = inquirer.prompt(choix, theme=GreenPassion())
        return choices

if __name__ == "__main__":
    mainChoise = main_choice()
    languageChoice = language_choice()
    dockerChoice = docker_choice()
    gitLink = git_link()