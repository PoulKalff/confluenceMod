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
        if [ -d "/home/$1/.kodi/addons/plugin.video.drnu" ]
        then
                sudo cp modified_files/addon.py                 /home/$1/.kodi/addons/plugin.video.drnu/resources/lib/addon.py
                echo '   ("plugin.video.drnu" was updated)'
        else
                echo '   ("plugin.video.drnu" does not exist, and was ignored!)'
        fi
        echo '     Done!'
        echo
fi
