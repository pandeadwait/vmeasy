import subprocess
import configparser

class VMException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class vmbServicer:
    def __init__(self):
        pass

    def startVM(self, vmname):
        print(f"Starting {vmname}...")
        
        result = subprocess.run(["VBoxManage", "startvm", vmname], capture_output = True, text = True)

        if result.returncode == 1:
            raise VMException(f"No VM found with the name {vmname}. Please recheck the VM name.")
        else:
            print("The VM has successfully started!")
    
        return True
    
    def stopVM(self, vmname):
        print(f"Powering off {vmname}...")

        result = subprocess.run(["VBoxManage", "controlvm", vmname, "poweroff"], capture_output = True, text = True)

        if result.returncode == 1:
            raise VMException(f"No VM found with the name {vmname} or the VM is not in running state. Please recheck the VM name")
        else:
            print("The VM is powered off!")

        return True

    def createVM(self, reqs):
        print(f"creating a VM with the name : {reqs['vmname']}, OS : {reqs['ostype']}, CPUs : {reqs['cpus']}, ram : {reqs['ram']}MB")

        cmd1 = subprocess.run(["VBoxManage", "createvm", "--name", reqs['vmname'], "--ostype", reqs['ostype'], "--register", "--basefolder", "D:\Program Files\VirtualBox VMs"], capture_output = True, text = True)

        errMsg = (
            "Could not create a VM.\n"
            "Please check the VM name and make sure that it is unique and valid.\n"
            "Also check the OS type and make sure that the OS type is valid."
            )

        if cmd1.returncode == 1:
            raise VMException(errMsg)
        else:
            print("Successfully created the VM.")
        
        cmd1 = subprocess.run(["VBoxManage", "modifyvm", reqs['vmname'], "--ioapic", "on"], capture_output = True, text = True)
        cmd2 = subprocess.run(["VBoxManage", "modifyvm", reqs['vmname'], "--memory", reqs['ram'], "--vram", reqs['vram'], "--cpus", reqs['cpus']])
        cmd3 = subprocess.run(["VBoxManage", "modifyvm", reqs['vmname'], "--nic1", "nat"])

        if cmd1.returncode == 1 or cmd2.returncode == 1 or cmd3.returncode == 1:
            raise VMException(f"Error while modifying the VM.")
        else:
            print("Successfully alocatted memory and networkin.")
        
        cmd1 = subprocess.run(["VBoxManage", "createhd", "--filename", f"D:\Program Files\VirtualBox VMs/{reqs['vmname']}/{reqs['vmname']}.vdi", "--size", "80000", "--format", "VDI"])
        cmd2 = subprocess.run(["VBoxManage", "storagectl", reqs['vmname'], "--name", "SATA Controller", "--add", "sata", "--controller", "IntelAhci"])
        cmd3 = subprocess.run(["VBoxManage", "storageattach", reqs['vmname'], "--storagectl", "SATA Controller", "--port", "0", "--device", "0", "--type", "hdd", "--medium",  f"D:\Program Files\VirtualBox VMs/{reqs['vmname']}/{reqs['vmname']}.vdi"])
        cmd4 = subprocess.run(["VBoxManage", "storagectl", reqs['vmname'], "--name", "IDE Controller", "--add", "ide", "--controller", "PIIX4"])
        cmd5 = subprocess.run(["VBoxManage", "storageattach", reqs['vmname'], "--storagectl", "IDE Controller", "--port", "1", "--device", "0", "--type", "dvddrive", "--medium", r"D:\ProdInno SetUp\ubuntu-20.04.6-desktop-amd64.iso"])
        cmd6 = subprocess.run(["VBoxManage", "modifyvm", reqs['vmname'], "--boot1", "dvd", "--boot2", "disk", "--boot3", "none", "--boot4", "none"])

        if cmd1.returncode == 1 or cmd2.returncode == 1 or cmd3.returncode == 1 or cmd4.returncode == 1 or cmd5.returncode == 1 or cmd6.returncode == 1:
            raise VMException(f"Error while creating and attaching hard drives.")
        else:
            print("successfully created and attached hard disks. Attached iso file.")
        
        cmd1 = subprocess.run(["VBoxManage", "modifyvm", reqs['vmname'], "--vrde", "on"])
        cmd2 = subprocess.run(["VBoxManage", "modifyvm", reqs['vmname'], "--vrdemulticon", "on", "--vrdeport", "10001"])

        if cmd1.returncode == 1 or cmd2.returncode == 1:
            raise VMException(f"Errot while enabling RDP.")
        else:
            print("Successfully enabled RDP.")
        
        print("Now you can start the VM!")

        return True

    def deleteVM(self, vmname):
        cmd1 = subprocess.run(["VBoxManage", "unregistervm", vmname, "--delete-all"])

        if cmd1.returncode == 1:
            raise VMException("Error while deleting the VM.")
        else:
            print("Successfully deleted the VM and all itd associated files.")

    def listVM(self):
        output = subprocess.check_output(["VBoxManage", "list", 'vms'], text=True)
        print("these are the VM currently created on this machine : ")
        print(output)
        print("------------------------------------------------------")
    
        return True


class vmwServicer:
    def __init__(self):
        pass