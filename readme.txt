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

4. The app will delete all current third party source list and save them in ~/third-party-sourcelist.gz.tar

5. Proceed to update/upgrade
$ sudo apt update
$ sudo apt dist-upgrade

6. Reboot
If offline repo usb drive is plugged in, remove it, plug it back when the machine finishes the reboot
