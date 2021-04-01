<!-- PROJECT INTRO -->
<br />
<p align="center">
  <a href="https://github.com/bretheskevin/SAVE-RESTORE">
    <h3 align="center">Save & Restore</h3>
  </a>


<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
  * [Description](#description)
  * [Pre-Requisite](#pre-requisite)
* [Usage](#usage)
  * [Setup rsync server side](#setup-rsync-server-side)
  * [Setup SSH Server](#setup-ssh-for-our-program)
  * [Change Root Password](#change-root-password)
  * [Necessary Scripts](#necessary-scripts)
  * [Optional](#optional)
  * [Cron Usage](#cron-usage)
* [Authors](##authors)



<!-- ABOUT THE PROJECT -->
## About The Project

### Description


Our Save & Restore project is about being able to save or restore files/folders from a computer to a server.
<br />
In this program, you will be able to save, restore, and setup an automatic save.
<br />
It works only on Linux.

### Pre-Requisite

* [Python](https://www.python.org/)
* [Bash](https://en.wikipedia.org/wiki/Bash_(Unix_shell))
* [Rsync](https://en.wikipedia.org/wiki/Rsync)
* [Cron](https://en.wikipedia.org/wiki/Cron)


<!-- USAGE EXAMPLES -->
## Usage

### Setup rsync server side
You have a choice, you can either setup the server by yourself, or use our script that you can get by using this command on your server:
```shell
wget https://www.dropbox.com/s/7n9dtaqwnd3p7av/setup.sh
sudo sh setup.sh
```

So if you want to do it by yourself you will need to follow these steps one by one. For the server, you can use a Virtual Machine, as well as another computer, or even a VPS.

First of all, create a content folder in /srv/intern:
```shell
mkdir /srv/intern/content
```
To authorize rsync to launch, you need to edit /etc/default/rsync with :
```shell
sudo nano /etc/default/rsync
```
Edit the line RSYNC_ENABLE to true.

You will then need to create the config file with:
```shell
sudo nano /etc/rsyncd.conf
```
At the top put:
```text
uid = rsync  
gid = rsync

[share_rsync]
    path = /srv/intern
    comment = Sync intern files
    read only = false
```
If you need more information, you can use man rsyncd.conf

Next, you will need to add the user and group rsync :
```text
sudo useradd rsync
sudo passwd rsync
sudo groupadd rsync
sudo gpasswd -a rsync rsync
```

After that set the /srv/intern folder to rsync :
```shell
sudo chown -R rsync:rsync /srv/intern/
``` 
You will then need to give the rights to the folder:
```shell
sudo chmod -R 775 /srv/intern
```
At last, to launch rsync you will need to type:
```shell
sudo /etc/init.d/rsync start
```
You can make rsync launch at every start of your machine by using this command:
```shell
sudo systemctl enable rsync.service
```

And here it is, your sync server is up and running!

### Cron usage
So to use the automatic save you will need to use cron.
So first, you will need to connect by SSH using our program with the third option.
When you are connected via SSH, you will need to type:
```shell
crontab -e
```
It will ask what text editor you want, it's as you like.
Next you will se a small tutorial on how to use cron, everything is in this text file, there is no other way to edit it.
So to set it up this is the example if you want to save everytime:
```shell
* * * * * rsync -az path_to_the_files root@your_server_ip:/srv/intern/content
```
You replace the stars by minutes, hours, day of the month, month, day of the week and at the end the command.
You will need to replace path_to_the_files and your ip to set the save.

#### Setup ssh for our program
First of all you will need to install openssh:
```shell
sudo apt install openssh-server
```
Then, open the /etc/ssh/sshd_config  
Uncomment the line PermitRootLogin and set the value to yes:
```text
PermitRootLogin yes
```
To make the new setting take effect, restart the ssh server:
```shell
systemctl restart sshd.service
```

#### Change Root Password
For the program to work you will need to input your password at the beggining, so change the root password:
```shell
passwd root
```
This will be your password for the whole process.

#### Necessary Scripts
You will need to create 2 scripts on your server.  
First it's a script that will check existing files:
```bash
#! /bin/bash
while :; do ls -R /srv/intern/content/ > files.txt; sleep 2; done
```
This script will be called script.sh and will need to be in /srv/intern/

And then another script that you will need to execute right after you put it:
```bash
#! /bin/bash
nohup sh /srv/intern/script.sh &
```

It will allow us to check existing files and folders on the server.
### Client usage
Before everything, you will need to edit config.json with the ip of your server.
Start the program using

```python
python3 main.py
```
Then you will be guided through the usage of the program.
### Optional
#### Add a SSH key to prevent from putting password everytime
Generate the public key, leave everything empty for default config.
```
ssh-keygen
Enter file in which to save the key (/home/$USERNAME/.ssh/id_rsa):
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
```

Copy public key to remote host:
```sh
ssh-copy-id -i ~/.ssh.id_rsa.pub root@yourserverip
```
<!-- CONTACT -->
## Authors

Kévin Brèthes - kevin.brethes@ynov.com <br />
Tom Hollingworth - tom.hollingworth@ynov.com <br />

<br /><br />
Project Link: [https://github.com/bretheskevin/SAVE-RESTORE](https://github.com/bretheskevin/SAVE-RESTORE)

