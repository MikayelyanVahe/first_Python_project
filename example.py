import json
import subprocess
import sys

if __name__ == '__main__':

    text = "az acr repository list -n commodity"
    cmd_output = subprocess.check_output(["powershell", "-Command", text], text=True)
    print(type(cmd_output))
#    newlist = cmd_output.split(maxsplit=1)
    for items in cmd_output:
        print(items)