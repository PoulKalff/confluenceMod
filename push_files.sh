#!/bin/bash

echo
if [ -z "$1"  ]; then                   # if nothing selected
        echo '  Usage: "push_files <username>"'
        echo
        exit
else
        echo '  Copying files....'
        sudo cp /home/$1/ConfluenceMod/modified_files/advancedsettings.xml             /home/$1/.kodi/userdata/
        sudo cp /home/$1/ConfluenceMod/modified_files/sources.xml                      /home/$1/.kodi/userdata/
        sudo cp /home/$1/ConfluenceMod/modified_files/*.xsp                            /home/$1/.kodi/userdata/playlists/video/
        sudo cp /home/$1/ConfluenceMod/modified_files/settings.xml                     /home/$1/.kodi/userdata/
        sudo cp /home/$1/ConfluenceMod/modified_files/*.png                            /home/$1/.kodi/addons/skin.confluence/media/
        sudo cp /home/$1/ConfluenceMod/modified_files/Home.xml                         /home/$1/.kodi/addons/skin.confluence/720p/
        sudo cp /home/$1/ConfluenceMod/modified_files/IncludesHomeMenuItems.xml        /home/$1/.kodi/addons/skin.confluence/720p/
        sudo cp /home/$1/ConfluenceMod/modified_files/VideoFullScreen.xml              /home/$1/.kodi/addons/skin.confluence/720p/
        sudo cp /home/$1/ConfluenceMod/modified_files/DialogSeekBar.xml                /home/$1/.kodi/addons/skin.confluence/720p/
        if [ -d "/home/$1/.kodi/addons/plugin.video.dr.dk.bonanza" ]
        then
                sudo cp /home/$1/ConfluenceMod/modified_files/addon.py                 /home/$1/.kodi/addons/plugin.video.dr.dk.bonanza/
        else
                echo '   ("plugin.video.dr.dk.bonanza" does not exist, and was ignored!)'
        fi
        echo '  Done!'
        echo
fi
