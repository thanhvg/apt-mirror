The Debian repository is:

http://dmz-server/r5.0/amd64

To use this repository do the following:

1. Use a web browser and fetch the file set-ivt-mirros.py from http://dmz-server  (right click save as)

2. Run the app, this app will set up both ivt offline mirror and ivt online mirror 

Option --dmz, -d to install dmz server
$ python3 set-ivt-mirros.py -dmz dmz-server/r5.0/amd64

If you are outside IVT office, use ivt mirror public ip address
$ python3 set-ivt-mirros.py --dmz 184.71.215.44/r5.0/amd64

If you don't pass any address, default public ip will be used
$ python3 set-ivt-mirros.py --dmz 

Option --usb, -u to install 
$ python3 set-ivt-mirros.py --usb 

If you run it without any param, help message will show up 

4. The app will delete all current third party source lists and save them in ~/third-party-sourcelist.gz.tar

5. Proceed to update/upgrade
$ sudo apt update
$ sudo apt dist-upgrade

6. step removed.

7. Reboot

If offline repo usb drive is plugged in, remove it
$sudo apt reboot

8.  Check if upgrade has been performed
$ lsb_release -a

look for 16.04.5, if it isn't present than the kernel was not updated.

intelliview@sam-lite-002:~/Downloads$ uname -a
Linux sam-lite-002 4.15.0-36-generic #39~16.04.1-Ubuntu SMP Tue Sep 25 08:59:23 UTC 2018 x86_64 x86_64 x86_64 GNU/Linux

9. Extra scripts in the protable hard drive
remove-flash.sh          # this one to remove Adobe Flash installer
update-nomachine.sh      # this one to update nomachine, it can take a while to finish

to use open terminal and cd to the portable disk 
$ cd /media/intelliview/apt-mirror
$ sh remove-flash.sh
$ sh update-nomachine.sh

If accessing via dmz-server run the following:

$ sudo apt-get remove flashplugin-installer
$ wget http://dmz-server/amd64/nomachine/nomachine_6.3.6_1_amd64.deb
$ sudo dpkg -i nomachine_6.3.6_1_amd64.deb 
$ rm nomachine_6.3.6_1_amd64.deb


