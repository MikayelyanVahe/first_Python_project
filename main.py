# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# Press the green button in the gutter to run the script.
import subprocess


def login(tenantid, tenantuser, tenantpass):
    txt = f"az login -t {tenantid} -u {tenantuser} -p {tenantpass}"
    cmd = txt.format(tenantid, tenantuser, tenantpass)
    command = subprocess.run(["powershell", "-Command", cmd], capture_output=True)
    if command.returncode != 0:
        print("An error occurred: %s", command.stderr)
    return command.stdout

    tenandid = input("Please type tenand ID: ")
    username = input("Please type username: ")
    password = input("Please type password: ")
    print(login(tenandid, username, password))

def myfunc(e):
    return len(e)


def run(input_list):
    value = "$secret = Get-AzureKeyVaultSecret  -VaultName d-allocation-aks-kv -name applicationInsights"
    cmd = "Write-Host $secret.SecretValueText"
    setparameter = subprocess.run(["powershell", "-Command", value], capture_output=True)
    input_list = subprocess.check_output(["powershell", "-Command", cmd], text=True).splitlines()
    print(input_list)
    return input_list


if __name__ == '__main__':

    keyvault_list = []
    keyvault_list = run(keyvault_list)

