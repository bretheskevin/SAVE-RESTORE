#! /usr/bin/sh

echo "The script will ask you sometimes your password."
echo "Downloading rsync file .."
wget https://www.dropbox.com/s/emkvz8wjm461baz/rsync
sleep 3
echo "Modifying rsync file.."
diff -u /etc/default/rsync rsync > new.diff
sleep 3
echo "Patching rsync file.."
patch -i new.diff /etc/default/rsync
rm -rf rsync
rm -rf new.diff
sleep 3
echo "Downloading rsyncd.conf..."
wget https://www.dropbox.com/s/1owr9f3a7whl5hm/rsyncd.conf -P /etc/
sleep 3
echo "Adding user and group rsync..."
sudo useradd rsync
sleep 3
echo "You will need to insert a rsync password."
sudo passwd rsync
sudo groupadd rsync
sleep 3
sudo gpasswd -a rsync rsync
echo "Setting default folder to put backup files..."
sudo chown -R rsync:rsync /srv/intern
sudo chmod -R 775 /srv/intern
sleep 3
echo "Launching rsync..."
sudo /etc/init.d/rsync start
sudo systemctl enable rsync.service
sleep 3
wget https://www.dropbox.com/s/n4vgvs8gelsf9r7/files.sh -P /srv/intern/files.sh
sleep 3
echo "Please change your root password, or put the same so you will be able to use rsync"
sudo passwd root
echo "Installation of openssh-server ..."
sudo apt install openssh-server
sleep 3
echo "Getting sshd_config..."
wget https://www.dropbox.com/s/3fxzu6ad4vw6d6k/sshd_config
sleep 3
diff -u /etc/ssh/sshd_config sshd_config > ssh.diff
sleep 3
echo "Patching sshd_config"
patch -i ssh.diff /etc/ssh/sshd_config
rm -rf sshd_config
rm -rf ssh.diff
nohup sh /srv/intern/files.sh &
