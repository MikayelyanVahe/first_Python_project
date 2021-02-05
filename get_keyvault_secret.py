import subprocess
import sys
# from datetime import datetime
from time import sleep
import json
import getpass


class Bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def main_menu():
    print("\nWelcome to KeyVault management iteractive menu, through this menu it is "
          "possible different oparations with KeyVault")
    print("You will be promted depends on oparation you want to apply")
    print("Create a Keyvault (c) / Create KeyVault secret:value/s (s)")
    print("List KeyVault secret names (ls) / Show secret/value pair (sh)")
    print("Backup/restote Keyvault (br)")
    print("Delete Keyvault (dk) / delete secret (ds)")
    print("Quit program (q)")


def azure_keyvault_set_create_secret():
    secretdict: dict = {}
    secretcount = input("Please enter how many secrets you want to create: ")
    keyvaultname = input("Please type vault name: ")
    for x in range(int(secretcount)):
        secretname = input("\nPlease type secret name: ")
        secretvalue = getpass.getpass("Enter secret value: ", stream=None)
        secretdict.update({secretname: secretvalue})

    for key, value in secretdict.items():
        txt = "az keyvault secret set --vault-name {} -n {} --value {}"
        cmd = txt.format(keyvaultname, key, value)
        command = subprocess.run(["powershell", "-Command", cmd], capture_output=True)
        if command.returncode != 0:
            print("An error occurred: %s", command.stderr)
        else:
            print("SECRET " + key + " SUCCESSFULLY CREATE IN " + value)


def azure_keyvault_delete_secret(keyvaultname: str):
    secretlist = azure_keyvault_secret_list(keyvaultname)
    print("following secrets exist in " + keyvaultname + "\n")
    i = 1
    for items in secretlist:
        print(str(i) + ". " + items)
        i = i + 1
    deletesecretsamount = input("\nPlease enter how many secrets you want to delete: ")
    for x in range(int(deletesecretsamount)):
        secretname = input("Please enter secret name do delete: ")
        txt = "az keyvault secret delete --vault-name {} -n {}"
        cmd = txt.format(keyvaultname, secretname)
        command = subprocess.run(["powershell", "-Command", cmd], capture_output=True)
        if command.returncode != 0:
            print("An error occurred: %s", command.stderr)
        else:
            print("SECRET " + secretname + " SUCCESSFULLY DELETED FROM " + keyvaultname)
        

def azure_keyvault_secret_list(keyvaultname: str):
    entrylist = []
    txt = "az keyvault secret list --vault-name {}"
    cmd = txt.format(keyvaultname)
    command = subprocess.check_output(["powershell", "-Command", cmd], text=True)
    commandoutputlist = json.loads(command)
    for items in commandoutputlist:
        keyvaultentry = items.get("name")
        entrylist.append(keyvaultentry)
    return entrylist


def azure_keyvault_secret_show_by_secret_name(keyvaultname: str):
    secretname = input("Please type secret name: ")
    txt = "az keyvault secret show --vault-name {} -n {}"
    cmd = txt.format(keyvaultname, secretname)
    commandoutput = subprocess.check_output(["powershell", "-Command", cmd], text=True)
    jsonloader = json.loads(commandoutput)
    secretvalue = jsonloader["value"]
    print("For SECRET NAME: " + secretname + "\nVALUE IS: " + secretvalue)


def azure_keyvault_secret_show(keyvaultname: str):
    inputlist = azure_keyvault_secret_list(keyvaultname)
    keyvultsecretdict = {}
    for item in inputlist:
        txt = "az keyvault secret show --vault-name {} -n {}"
        cmd = txt.format(keyvaultname, item)
        commandoutput = subprocess.check_output(["powershell", "-Command", cmd], text=True)
        jsonloader = json.loads(commandoutput)
        secret_value = jsonloader["value"]
        keyvultsecretdict[item] = secret_value
    for key, value in keyvultsecretdict.items():
        print("\nSECRET NAME: " + key + "\nSECRET VALUE IS: " + value)


def azure_keyvault_create():
    rg = input("Please type recovery group (default is cargoo-kv-rg-weu1): ") or "cargoo-kv-rg-weu1"
    keyvaultname = input("Please type vault name: ")
    location = input("Please type location (default is westeurope): ") or "westeurope"
    sku = input("Please type sku (default is standart): ") or "standard"
    txt = "az keyvault create -g {} -n {} -l {} --sku {}"
    cmd = txt.format(rg, keyvaultname, location, sku)
    command = subprocess.Popen(["powershell", "-Command", cmd], text=True)
    while command.poll() is None:
        print("--Running--")
        sleep(10)
    if command.returncode != 0:
        print("An error occurred: %s", command.stderr)
    else:
        print("KeyVault " + keyvaultname + " successfuly created!!!")


def azure_keyvault_delete(keyvaultname: str, rg: str):
    # rg = input("Please type recovery group (default is cargoo-kv-rg-weu1): ") or "cargoo-kv-rg-weu1"
    # keyvaultname = input("Please type vault name you want to delete: ")
    txt = "az keyvault delete --name {} -g {}"
    cmd = txt.format(keyvaultname, rg)
    command = subprocess.Popen(["powershell", "-Command", cmd], text=True)
    while command.poll() is None:
        print("--Running--")
        sleep(5)
    if command.returncode != 0:
        print("An error occurred: %s", command.stderr)
    else:
        print("KeyVault " + keyvaultname + " successfuly deleted!!!")


if __name__ == '__main__':

    trigger = False
    while trigger is False:
        main_menu()
        answer = input("Please choose opration: ")
        if answer == "c":
            print("Answer is c")
            trigger = False
        elif answer == "s":
            print("Answer is s")
            trigger = False
        elif answer == "q":
            print("Answer is s")
            trigger = True
        else:
            print("wrong answer is typed")
            trigger = False
    print("Script will be interrupted")
    sys.exit()



