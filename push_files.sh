#!/bin/bash

echo
if [ -z "$1"  ]; then                   # if nothing selected
        echo '  Usage: "push_files <username>"'
        echo
        exit
else
        echo '  Copying files....'
        sudo cp /home/$1/confluenceMod/modified_files/advancedsettings.xml             /home/$1/.kodi/userdata/
        sudo cp /home/$1/confluenceMod/modified_files/sources.xml                      /home/$1/.kodi/userdata/
        sudo cp /home/$1/confluenceMod/modified_files/*.xsp                            /home/$1/.kodi/userdata/playlists/video/
        sudo cp /home/$1/confluenceMod/modified_files/settings.xml                     /home/$1/.kodi/userdata/
        sudo cp /home/$1/confluenceMod/modified_files/*.png                            /home/$1/.kodi/addons/skin.confluence/media/
        sudo cp /home/$1/confluenceMod/modified_files/Home.xml                         /home/$1/.kodi/addons/skin.confluence/720p/
        sudo cp /home/$1/confluenceMod/modified_files/IncludesHomeMenuItems.xml        /home/$1/.kodi/addons/skin.confluence/720p/
        sudo cp /home/$1/confluenceMod/modified_files/IncludesBackgroundBuilding.xml   /home/$1/.kodi/addons/skin.confluence/720p/
        sudo cp /home/$1/confluenceMod/modified_files/Includes.xml                     /home/$1/.kodi/addons/skin.confluence/720p/
        sudo cp /home/$1/confluenceMod/modified_files/VideoFullScreen.xml              /home/$1/.kodi/addons/skin.confluence/720p/
        sudo cp /home/$1/confluenceMod/modified_files/DialogSeekBar.xml                /home/$1/.kodi/addons/skin.confluence/720p/
        sudo cp -r /home/$1/confluenceMod/modified_files/plugin.video.mod_drtv         /home/$1/.kodi/addons/
        echo '     Done!'
        echo '  Manually move, if necessary: drtv-plugin-updatedb  --->  <server>/usr/local/share'
        echo
fi
