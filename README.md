# Welcome to CAPS Drone Academy
We have some exciting drone projects to try. But first things first:

# Installing PyCharm on Chromebook
The video with detailed steps is here: https://youtu.be/SBgAQZ96O1U .

Two commands to run (even before PyCharm is downloaded)
```
sudo apt update
sudo apt install python3 python3-pip build-essential libssl-dev libffi-dev python3-dev default-jdk
```
.

Two commands to extract PyCharm and make a shortcut `charm` in home directory:
```
tar -xf pycharm-*.gz
ln -sf pycharm-*/bin/pycharm charm
```
.

And three commands to make a desktop icon for PyCharm:
```
sudo cat > pycharm.desktop << END
[Desktop Entry]
Name=PyCharm 
Type=Application
Comment=Support Application
Exec=/home/$USER/charm
Terminal=false
Categories=Utility;
END


chmod 666 pycharm.desktop


sudo mv pycharm.desktop /usr/share/applications/
```
.
