#!/bin/bash

echo
if [ -z "$1"  ]; then                   # if nothing selected
        echo '  Usage: "push_files <username>"'
        echo
        exit
else
        echo '  Copying files....'
        sudo cp modified_files/advancedsettings.xml		/home/$1/.kodi/userdata/
        sudo cp modified_files/*.xsp				/home/$1/.kodi/userdata/playlists/video/
        sudo cp modified_files/settings.xml			/home/$1/.kodi/userdata/
 	sudo cp modified_files/*.png				/home/$1/.kodi/addons/skin.confluence/media/
	echo '  Done... now just remeber to install ModConf.zip from kodi interface.'
	echo
fi

