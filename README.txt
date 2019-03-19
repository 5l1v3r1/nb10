SecPoint.com Netbios share scanner


This tool could be used to check windows workstations and servers 
if they have accessible shared resources.

It works on linux/unix, and uses samba.org  smbclient tool to login.

On successful logon tool tries to retrieve list of shared disks 
and for each disk tries to get directory listing.

Set +x for script and run it as 

./netbios-shares-scanner.py  IP
or
python ./netbios-shares-scanner.py IP

You could scan not only one target machine, but all your network. 
As IP you can set subnetwork mask or plain range:
./netbios-shares-scanner.py  192.168.1.1/24
or 
./netbios-shares-scanner.py  192.168.1.1-192.168.1.255

If you want to check what's visible for specific user - you could use
username%password option (default is Guest access):
./netbios-shares-scanner.py  192.168.1.1/24  user%pass
This will scan all workstations in 192.168.1.1/24  using "user" and "pass" to login


You also could add    > log.txt   or   >> log.txt   to the command to get list of shares in the file:
./netbios-shares-scanner.py  IP > log.txt        this will create or re-create log.txt
./netbios-shares-scanner.py  IP >> log.txt        this will append to log.txt


Examples:
 1-scan 192.168.1.1 for open shares
  ./netbios-shares-scanner 192.168.1.1

 2-scan 192.168.1.1 ... 255 for open shares
  ./netbios-shares-scanner 192.168.1.1-192.168.1.255

 3-scan network range /24 for open shares
  ./netbios-shares-scanner 192.168.1.1/24

 4-scan 192.168.1.1 for password-protected shares 
  ./netbios-shares-scanner 192.168.1.1/24 yourname%yourpass

 5-scan network range for password-protected shares and save list to file
  ./netbios-shares-scanner 192.168.1.1/24 yourname%yourpass > results.txt


History: 
# ## 0.1 initial release
# ## 0.2 added Overview section to output
# ## 0.3 IP mask and range support (like 192.168.1.1/24 or 192.168.1.1-192.168.1.255)
# ## 0.5 Added username/password option in command line to login to non-anonymous shares
# ## 0.6 More friendly status codes
# ## 1.0 Examples and help, minog fixes
--
www.SecPoint.com Team

Check for more free security scan tools at http://www.secpoint.com
Try port scanner http://www.secpoint.com/free-port-scan.html
and free vulnerability scan at http://www.secpoint.com/free-vulnerability-scan.html