# This script is cleaning up Azure container registry by registry name
# Script v0.4 // Corrected login part

import subprocess
import sys
from datetime import datetime
import getpass


def login(tenantid, user, userpass):
    logout_txt = "az logout"
    txt = "az login -t {} -u {} -p {}"
    cmd = txt.format(tenantid, user, userpass)
    subprocess.run(["powershell", "-Command", logout_txt], capture_output=True, text=True)
    command = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True)
    if command.returncode != 0:
        print("An error occurred: %s", command.stderr)
        f.write("\nAn error occurred: %s")
        print("incorrect credentials, please try again: ")
        f.write("\nincorrect credentials, please try again: ")
        return command.returncode
    else:
        return command.returncode


def loginmessage():
    tenand = input("\nPlease type tenand ID: Default is ac256e6a-5878-494f-8eef-4f4d4c1e5da7: ") or \
             "ac256e6a-5878-494f-8eef-4f4d4c1e5da7"
    print("Tenant id is: " + tenand)
    f.write("\nTenant id is: " + tenand)
    username = input("Please type username: Default is vahe.mikayelyan@volo.global: ") or "vahe.mikayelyan@volo.global"
    print("UserName is: " + username)
    f.write("\nUserName is: " + username)
    password = getpass.getpass("Enter your password: ", stream=None)
    loginreturncode = login(tenand, username, password)
    return loginreturncode


def listsortbylenght(e):
    return len(e)


def check_acr_repo_names(container_registry_name):
    txt = "az acr repository list -n {} -o table"
    cmd = txt.format(container_registry_name)
    commandexec = subprocess.run(["powershell", "-Command", cmd], capture_output=True)
    if commandexec.returncode != 0:
        print("An error occurred: %s", commandexec.stderr)
        f.write("\nAn error occurred: %s")
        f.write(str(commandexec.stderr))
    output_list = subprocess.check_output(["powershell", "-Command", cmd], text=True).splitlines()
    output_list = filter_output_list(output_list)
    return output_list


def check_acr_repo_tags(repository_name, container_registry_name):
    txt = "az acr repository show-tags -n {} --repository {} -o table"
    cmd = txt.format(container_registry_name, repository_name)
    commandexec = subprocess.run(["powershell", "-Command", cmd], capture_output=True)
    if commandexec.returncode != 0:
        print("An error occurred: %s", commandexec.stderr)
        f.write("\nAn error occurred: %s" + str(commandexec.stderr))
    output_list = subprocess.check_output(["powershell", "-Command", cmd], text=True).splitlines()
    output_list = filter_output_list(output_list)
    return output_list


def delete_tags_in_repository(container_registr_yname, repositoryname, tagid):
    txt = "az acr repository delete -n {} --image {}:{} --yes"
    cmd = txt.format(container_registr_yname, repositoryname, tagid)
    commandexec = subprocess.run(["powershell", "-Command", cmd], capture_output=True)
    if commandexec.returncode == 0:
        print(repositoryname + " tag/image id " + tagid + " deleted successfully")
        f.write("\n" + repositoryname + " tag/image id " + tagid + " deleted successfully")


def filter_output_list(output_list):
    output_list.pop(0)
    output_list.pop(0)
    return output_list


if __name__ == '__main__':

    filedate = datetime.now()
    fileyear = filedate.year
    filemonth = filedate.month
    fileday = filedate.day
    filehours = filedate.hour
    fileminutes = filedate.minute

    filedateformat = str("delete_tags_log_") + str(fileday) + "." + str(filemonth) + "." \
        + str(fileyear) + "_" + str(filehours) + "." + str(fileminutes) + ".txt"
    f = open(filedateformat, "x")

    print("### This script is cleaning up Azure container registry by registry name ###")
    print("### It is written by VOLO DevOps engineer Vahe Mikayelyan ###")
    print("### it is only for internal VOLO use ###")
    f.write("### This script is cleaning up Azure container registry by registry name ###")
    f.write("\n### It is written by VOLO DevOps engineer Vahe Mikayelyan ###")
    f.write("\n### it is only for internal VOLO use ###")

    while loginmessage() != 0:
        loginmessage()

    print("\nYou have successfully logged in Azure Tenant")
    f.write("\nYou have successfully logged in Azure Tenant")

    input("Press Enter to continue ")
    registry_name = input("\nContainer Registry name: ")
    f.write("\nContainer Registry name: " + registry_name)
    keeptags = int(input("Please enter amount of tags/images you want to keep: "))
    repository_list = check_acr_repo_names(registry_name)
    question = input("do you want to continue deletion of images? (y/n) ")
    scriptstartTime = datetime.now()

    if question == 'y':
        for x in repository_list:
            tag_list = check_acr_repo_tags(x, registry_name)
            tag_list.sort(key=listsortbylenght)
            if len(tag_list) <= keeptags:
                print("\nRepository " + x + " has less then " + str(keeptags) + " images/tags")
                f.write("\nRepository " + x + " has less then " + str(keeptags) + " images/tags")
            else:
                deletionstarttime = datetime.now()
                print("\nOutput of " + x + " tag list")
                f.write("\nOutput of " + x + " tag list")
                print(tag_list)
                f.write("\n" + str(tag_list))
                print("--------------------------------------------")
                f.write("\n--------------------------------------------")
                for y in range(len(tag_list) - keeptags):
                    delete_tags_in_repository(registry_name, x, tag_list[y])
                print("--------------------------------------------")
                f.write("\n--------------------------------------------")
                print("time to complete " + str(datetime.now() - deletionstarttime))
                f.write("\ntime to complete " + str(datetime.now() - deletionstarttime))
    elif question == 'n':
        print("\nScript has been interrupted")
        f.write("\nScript has been interrupted")
        f.close()
        sys.exit()
    else:
        print("wrong answer")
        f.write("wrong answer")
        f.close()
        sys.exit()

    print("\nall taks has been finished")
    print("--------------------------------------------")
    print("script complition time " + str(datetime.now() - scriptstartTime))
    f.write("\nall taks has been finished" + "\n--------------------------------------------")
    f.write("\nscript complition time " + str(datetime.now() - scriptstartTime))
    input("Press enter to close: ")
    f.close()
