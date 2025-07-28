from internal import vmbServicer, vmwServicer
import argparse
import configparser
import logging

desc = '''
    This is a basic command line utitlity for creating, deleting, starting, stoping, and listing VMs on this machine.
'''

opHelp = '''
    Specify what operation you want to perform from the five operaitons supported which are - start, stop, create, delete, list.
'''

stHelp = '''
    Specify the name of the VM to start.
'''

spHelp = '''
    Specify the name of the VM to stop.
'''

crHelp = '''
    Specify the name of the VM you want to create.
'''

dlHelp = '''
    Specify the name of the VM you want to delete.
'''

lsHelp= '''
    No argument. The command lists out all the VM currently created on this machine.
'''

class ConfigInteractor:
    def __init__(self):
        pass

    def readConfig(self, section, prop):
        pass

    def writeConfig(self):
        pass

class Executer:
    def __init__(self, hyperviser):
        self.hyperviser = hyperviser
        self.internal = None
        print("Your selected hyperviser is : " + self.hyperviser + ". To change run command 'set --hypserviser {hyperviser}'")

        if self.hyperviser == "vmb":
            self.internal = vmbServicer()
        else:
            raise Exception("Hyperviser not found. Please check your selected hyperviser.")
    
    def startVM(self, vmName):
        try:
            self.internal.startVM(vmName)
            return True
        except Exception as e:
            print(e)   

            return False

    def stopVM(self, vmName):
        try:
            self.internal.stopVM(vmName)

            return True
        except Exception as e:
            print(e)
        
            return False

    def createVM(self, args):
        try:
            configParser = configparser.RawConfigParser()
            configFilePath = r'config.ini'
            configParser.read(configFilePath)

            reqs = dict()

            reqs['vmname'] = args.vmname 
            reqs['cpus'] = configParser.get("default-reqs", "cpus") if args.cpus == None else args.cpus
            reqs['ram'] = configParser.get("default-reqs", "ram") if args.ram == None else args.ram
            reqs['vram'] = configParser.get("default-reqs", "vram") if args.vram == None else args.vram
            reqs['ostype'] = configParser.get("default-reqs", "ostype") if args.ostype == None else args.ostype
            
            self.internal.createVM(reqs)

            return True
        except Exception as e:
            print("There was some error while creating the VM.")
            print(e)

            return False

    def deleteVM(self, vmname):
        try:    
            self.internal.deleteVM(vmname)

            return True
        except Exception as e:
            print(e)

            return True

    def list(self):
        try:
            self.internal.listVM()

            return True
        except Exception as e:
            print("There was some error while listing all the VMs on this machine.")
            print(e)

def setConfig(args):
    configParser = configparser.ConfigParser()
    reader = configparser.RawConfigParser()
    configFilePath = r'config.ini'
    reader.read(configFilePath)

    configParser["hyperviser-config"] = {
        "hyperviser": reader['hyperviser-config']['hyperviser'] if args.hyperviser == None else args.hyperviser,
        "uname": reader['hyperviser-config']['uname'] if args.username == None else args.username,
        "pwd": reader['hyperviser-config']['pwd'] if args.password == None else args.password
    }

    configParser['default-reqs'] = {
        "ostype": reader['default-reqs']['ostype'] if args.ostype == None else args.ostype,
        "cpus": reader['default-reqs']['cpus'] if args.cpus == None else args.cpus,
        "ram": reader['default-reqs']['ram'] if args.ram == None else args.ram,
        "vram": reader["default-reqs"]['vram'] if args.vram == None else args.vram
    }
    
    with open("config.ini", 'w') as file:
        configParser.write(file)

def main():
    parser = argparse.ArgumentParser(description="VM Management CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    start_parser = subparsers.add_parser("start", help="Start a VM")

    start_parser.add_argument("vmname", type=str, help="Name of the VM to start")

    stop_parser = subparsers.add_parser("stop", help="Stop a VM")
    stop_parser.add_argument("vmname", type=str, help="Name of the VM to stop")

    create_parser = subparsers.add_parser("create", help="Create a VM")
    create_parser.add_argument("vmname", type=str, help="Name of the VM to create")
    create_parser.add_argument("--cpus", type = int, help = "Enter the number of CPUs you require", default = None)
    create_parser.add_argument("--ram", type = int, help = "Enter the amount of RAM you require in MBs", default = None)
    create_parser.add_argument("--vram", type = int, help = "Enter the amount of VRAM you require", default = None) 
    create_parser.add_argument("--ostype", type = str, help = "Enter a OS type compatible with your hyperviser.", default = None)

    delete_parser = subparsers.add_parser("delete", help="Delete a VM")
    delete_parser.add_argument("vmname", type=str, help="Name of the VM to delete")

    subparsers.add_parser("list", help="List all VMs")

    set_parser = subparsers.add_parser("set", help = "Set configurations for the utility")
    set_parser.add_argument("--hyperviser", type = str, help = "Enter the name of hyperviser", default = None)
    set_parser.add_argument("--username",type = str, help = "Enter  your username", default = None)
    set_parser.add_argument("--password", type = str, help = "Enter your password", default = None)
    set_parser.add_argument("--ostype", type = str, help = "Enter the default OS type for guest OS", default = None)
    set_parser.add_argument("--cpus", type = int, help = "Enter the default number of CPUs", default = None)
    set_parser.add_argument("--ram", type = int, help = "Enter the default amount of RAM in MBs", default = None)
    set_parser.add_argument("--vram", type = int, help = "Entert the default amount of VRAM you need", default = None)   

    args = parser.parse_args()

    if args.command == "set":
        setConfig(args)

    configParser = configparser.RawConfigParser()   
    configFilePath = r'config.ini'
    configParser.read(configFilePath)
     
    try :
        executer = Executer(configParser.get("hyperviser-config", "hyperviser"))

        if args.command == "start":
            executer.startVM(args.vmname)
        elif args.command == "stop":
            executer.stopVM(args.vmname)
        elif args.command == "create":
            executer.createVM(args)
        elif args.command == "delete":
            executer.deleteVM(args.vmname)
        elif args.command == "list":
            executer.list()

        return True
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()