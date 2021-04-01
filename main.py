#! /bin/python3.9

from os import system
import json

system("clear")


def presentation():
    print("""
    ██████   █████   ██████ ██   ██ ██    ██ ██████      ████████  ██████   ██████  ██      
    ██   ██ ██   ██ ██      ██  ██  ██    ██ ██   ██        ██    ██    ██ ██    ██ ██      
    ██████  ███████ ██      █████   ██    ██ ██████         ██    ██    ██ ██    ██ ██      
    ██   ██ ██   ██ ██      ██  ██  ██    ██ ██             ██    ██    ██ ██    ██ ██      
    ██████  ██   ██  ██████ ██   ██  ██████  ██             ██     ██████   ██████  ███████                                                                                                                                                                      
    """)


#IP OF THE SERVER, EDIT THE CONFIG.JSON
with open("config.json") as json_file:
    data = json.load(json_file)
    ip = data.get("ip")


while 1:
    loop = True
    #choose what to do
    presentation()

    print("Choose an option: (Press q to exit)")
    print("1. Backup")
    print("2. Restore")
    print("3. Setup an autosave")
    print("")

    try:
        answer = str(input()).lower()
        if answer not in ["1", "2", "backup", "restore", "3", "q"]:
            raise ValueError
    except ValueError:
        system("clear")
        print("Invalid input\n")
        continue
    
    if answer == "q":
        exit()

    
    system("clear")
    while loop == True:

        #BACKUP
        if answer in ["1", "backup"]:
            print("\nEnter the path of the directory/file that you want to backup. (Press q to come back)")
            path = str(input(""))

            if path.lower() == "q":
                system("clear")
                break

            system(f"sh Utils/verif_path.sh {path}")

    
            try:
                with open("Utils/checkPath", "rb") as f:                
                    content = str(f.read())
                    if "0" in content:
                        print("Invalid path!")
                        break

                system(f"rsync -az {path} root@{ip}:/srv/intern/content/")                                   
                print("File backup complete!")
            except:
                system("clear")
                print("Fatal error!")
                break
        
        
        #RESTORE
        if answer in ["2", "restore"]:
            loop = True

            system(f"rsync -az root@{ip}:/srv/intern/files.txt ./")

            print("List of the files:")
        
            with open('./files.txt') as f: #array of each lines
                lines = f.readlines()

            system("cat ./files.txt")
            system("rm -rf ./files.txt")

            index_folders = []
            for i in range(len(lines)):
                if ":" in lines[i]:
                    index_folders.append(i)

            all_path = []
            for i in range(len(lines)):
                if i in index_folders:
                    path = lines[i].replace(":\n", "")
                    if not path.endswith("/"):
                        path += "/"                  
                    continue
                else:
                    if lines[i].replace("\n", "") != "":
                        all_path.append(path + lines[i].replace("\n", ""))

            while 1:
                print("\nEnter the path of the directory/file that you want to restore. (Press q to come back)")
                path = str(input(""))

                if path.startswith("/srv/intern/content/"):
                    path = path[len("/srv/intern/content/")-1:]
                                                                                                                                                                                                                                                                 
                if path.lower() == "q":
                    loop = False
                    system("clear")
                    break

                #path error
                error = True
                for line in all_path:
                    if line.endswith(path):
                        error = False
                if error:
                    print("Invalid path!")
                    continue
                
                try:
                    system(f"rsync -az  root@{ip}:/srv/intern/content/{path} ./Restored/")                                   
                    print("File restored successfully!")
                except:
                    system("clear")
                    print("Fatal error!")
                    break
                    

        # AUTO-SAVE
        if answer in ["3"]:
            system("clear")
            print("Type exit whenever you want to close the ssh")
            system(f"ssh root@{ip}")
            break
