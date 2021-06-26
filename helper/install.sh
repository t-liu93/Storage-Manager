#!/bin/bash

# Install packages
sudo apt update
sudo apt install mariadb-server python3 python3-pip npm

# Prepare database
sudo mysql -e "CREATE DATABASE IF NOT EXISTS storagemanager;"
sudo mysql -e "CREATE USER IF NOT EXISTS 'storagemanager'@'localhost' IDENTIFIED BY 'storagemanager';"
sudo mysql -e "GRANT ALL PRIVILEGES ON storagemanager.* TO 'storagemanager'@'localhost';"
sudo mysql -e "FLUSH PRIVILEGES;"

sudo mysql storagemanager -e "CREATE TABLE items(uuid varchar(255),
                                                itemName varchar(255),
                                                amount int,
                                                modifiedDate date,
                                                comments varchar(255),
                                                PRIMARY KEY (uuid)) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

sudo mysql storagemanager -e "CREATE TABLE category(categoryName varchar(255),
                                                    description varchar(255),
                                                    PRIMARY KEY (categoryName)) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

sudo mysql storagemanager -e "CREATE TABLE itemscategory(uuid varchar(255),
                                                       category varchar(255),
                                                       PRIMARY KEY (uuid, category)) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

sudo mysql storagemanager -e "CREATE TABLE itemsexpire(uuid varchar(255),
                                                    expire date,
                                                    amount int,
                                                    PRIMARY KEY (uuid, expire)) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# Install pip packages
pip3 install -r requirements.txt

# echo 'Enter mail address for mailing service, leave empty if you want to disable mailing service.'
# echo 'Enter the mail from address for mailing service:'
# read mailFrom
# echo 'Enter the mail to address for mailing service:'
# read mailTo

if [ -f "/etc/systemd/system/storagemanager.service" ]; then
    echo 'Disable existing service'
    sudo systemctl stop storagemanager.service
    sudo systemctl disable storagemanager.service
    sudo rm /etc/systemd/system/storagemanager.service
fi

mkdir -p $HOME/.local/storagemanager

cp -r ../backend/*.py $HOME/.local/storagemanager

# sed -i 's/MAIL_FROM = ""/MAIL_FROM = "'"$mailFrom"'"/g' $HOME/.local/storagemanager/saving.py
# sed -i 's/MAIL_TO = ""/MAIL_TO = "'"$mailTo"'"/g' $HOME/.local/storagemanager/saving.py

echo 'Copy service file'
sudo cp storagemanagerbackend.service /etc/systemd/system

echo 'Alter service file'
sudo sed -i 's/User=/User='"$USER"'/g' /etc/systemd/system/storagemanagerbackend.service
sudo sed -i 's+WorkingDirectory=+WorkingDirectory='"$HOME"'/.local/storagemanager+g' /etc/systemd/system/storagemanagerbackend.service

sudo systemctl enable storagemanagerbackend.service
sudo systemctl start storagemanagerbackend.service

# Install frontend
echo 'Install frontend to /var/www/storagemanager'
sudo rm -rf /var/www/storagemanager
pushd ../frontend/StorageManager
npm install
npm run build
sudo mkdir -p /var/www/storagemanager
sudo cp -r dist/* /var/www/storagemanager
sudo chown -R www-data:www-data /var/www/storagemanager
popd

echo 'Alter your webserver (e.g. Nginx/Apache) to this address.'
