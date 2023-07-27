import csv
import os
from pathlib import Path


def create_user():
  with open('config.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
      firstname, lastname, group = row
      username = (f"{firstname[0]}{lastname}").lower()
      if group == "Compta" or group == "RH" or group == "Dev":
        os.system(
          f'adduser --disabled-password {username} {group} logiciel; passwd -e {username} '
        )
      else:
        os.system(
          f'adduser --disabled-password {username} {group}; passwd -e {username} '
        )


def create_folder_structure(data):
  # Création du dossier racine
  root = os.getcwd()
  folders = {}
  # Parcourir les données et créer un dictionnaire des dossiers avec leurs informations
  for row in data:
    parent = row['parent']
    foldername = row['foldername']
    groupe_owner = row['groupe_owner']
    rigths = row['rigths'].strip()
    if parent not in folders:
      folders[parent] = []
    folders[parent].append({
      'foldername': foldername,
      'groupe_owner': groupe_owner,
      'rigths': rigths
    })
  # Fonction récursive pour créer la structure d'arborescence
  def create_subfolders(parent_path, subfolders):
    for folder in subfolders:
      foldername = folder['foldername']
      # groupe_owner = folder['groupe_owner']
      rigths = string_to_octal(folder['rigths'])
      print(folder['rigths'])
      print(rigths)
      folder_path = os.path.join(parent_path, foldername)
      # Création du nouveau dossier
      Path(folder_path).mkdir(parents=True, exist_ok=True)
      # Modification des droits sur le dossier
      os.chmod(folder_path, int(rigths))
      # Modification du groupe propriétaire du dossier
      os.chown(folder_path, -1, groupe_owner)
      if foldername in folders:
        create_subfolders(folder_path, folders[foldername])

  # Création de la structure d'arborescence à partir du dossier racine
  if '' in folders:
    create_subfolders(root, folders[''])


def string_to_octal(droits):
  if len(droits) != 9:
    raise ValueError("La chaîne de caractères doit avoir une longueur de 9.")

  # Tableau de correspondance des permissions
  permission_mapping = {
    '---': '0',
    '--x': '1',
    '-w-': '2',
    '-wx': '3',
    'r--': '4',
    'r-x': '5',
    'rw-': '6',
    'rwx': '7'
  }

  # Conversion de la chaîne en octal
  octal = ''.join(
    permission_mapping.get(droits[i:i + 3], '') for i in range(0, 9, 3))

  return octal


if __name__ == "__main__":
  # Chemin du fichier CSV
  csv_file = 'folder.csv'
  # Lecture des données du fichier CSV
  with open(csv_file, 'r') as file:
    reader = csv.DictReader(file)
    data = list(reader)
  # Création de la structure d'arborescence
  create_folder_structure(data)
  # create_user()
