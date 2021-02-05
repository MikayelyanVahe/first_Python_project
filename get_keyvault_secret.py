import subprocess
# import sys
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


def azure_keyvault_delete_secret():
    keyvaultname = input("Please type vault name: ")
    secretlist = azure_keyvault_secret_list(keyvaultname)
    print("following secrets exist")
    i = 1
    for items in secretlist:
        print(str(i) + ". " + items)
        i = i + 1
    deletesecretsamount = input("Please enter how many secrets you want to delete: ")
    for x in range(deletesecretsamount):
        

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


def azure_keyvault_secret_show_by_secret_name():
    keyvaultname = input("Please type vault name: ")
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
    vaultname = input("Please type vault name: ")
    location = input("Please type location (default is westeurope): ") or "westeurope"
    sku = input("Please type sku (default is standart): ") or "standard"
    txt = "az keyvault create -g {} -n {} -l {} --sku {}"
    cmd = txt.format(rg, vaultname, location, sku)
    command = subprocess.Popen(["powershell", "-Command", cmd], text=True)
    while command.poll() is None:
        print("--Running--")
        sleep(10)
    if command.returncode != 0:
        print("An error occurred: %s", command.stderr)
    else:
        print("KeyVault " + vaultname + " successfuly created!!!")


if __name__ == '__main__':

    azure_keyvault_delete_secret()
