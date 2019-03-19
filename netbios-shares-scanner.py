#!/usr/bin/python
# -*- coding: utf-8 -*-

# ################################################################################  
# ## Redistributions of source code must retain the above copyright notice
# ## DATE: 2011-01-19  
# ## AUTHOR: SecPoint ApS  
# ## MAIL: info@secpoint.com  
# ## SITE: http://www.secpoint.com  
# ## Other scanners: http://www.secpoint.com/free-port-scan.html
# ## Other scanners: http://www.secpoint.com/free-vulnerability-scan.html
# ##
# ## LICENSE: BSD http://www.opensource.org/licenses/bsd-license.php
# ################################################################################  
# ## 0.1 initial release
# ## 0.2 added Overview section to output
# ## 0.3 IP mask and range support (like 192.168.1.1/24 or 192.168.1.1-192.168.1.255)
# ## 0.5 Added username/password option in command line to login to non-anonymous shares
# ## 0.6 More friendly status codes
# ## 1.0 Examples and help, minog fixes

import os
import sys
import ipaddr
import socket

#usernamePasswordParam =  "-U name%pass"  #changing to that if need to scan non-guest shares
usernamePasswordParam =  "-N"

banner ="""SecPoint.com NetBios Share Scanner 1.0

 The Portable Penetrator - Wifi Recovery - Vulnerability Scanner
 http://www.secpoint.com/portable-penetrator.html
        """

def checkPort(ip,port=139):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    try:
        s.connect((ip,int(port)))
        s.shutdown(2)
        return True
    except:
        return False


def getList(ip):
  #first we should get all disks list
  #and some Overview here
  overViewF = os.popen(r'/usr/bin/smbclient -L %s %s 2>/dev/null'%(ip,usernamePasswordParam))
  overViewS = overViewF.readlines()
  overViewS = [s.strip() for s in overViewS]
  overViewString = "\n".join(overViewS) 
  overViewF.close()


  f = os.popen(r'/usr/bin/smbclient -L %s %s 2>/dev/null| grep " Disk " | sed -e "s/ Disk .*//" | sed -e "s/^[ \t]*//"'%(ip,usernamePasswordParam))
  disks = f.readlines()
  disks = filter(None, disks)
  disks = [d.strip() for d in disks]
  f.close()

  #now we will make DIR for each share and save output 
  listings = {}
  for disk in disks:
      f = os.popen(r'/usr/bin/smbclient //%s/"%s" %s -c "dir;exit" 2>/dev/null'%(ip,disk,usernamePasswordParam))
      dirlist =  f.readlines()
      dirlist = [d.strip() for d in dirlist]
      listings[disk]=dirlist
      f.close()

  #now we will prepare pretty output 

  resStrings = []

  foundString = ""
  for d in listings.keys():
      foundString = foundString + "Found share: %s\n%s\n\n\n"%(d,"\n".join(listings[d]))

  foundString = foundString.replace("NT_STATUS_ACCESS_DENIED","Share is VISIBLE but password protected")
  foundString = foundString.replace("NT_STATUS_OBJECT_PATH_NOT_FOUND","Can't access file")
  foundString = foundString.replace("NT_STATUS_NO_MEDIA_IN_DEVICE","Drive is shared but no medium accessible")
  foundString = foundString.replace("NT_STATUS_DEVICE_DATA_ERROR","Can't access share")
  

  if listings:
    return overViewString+'\n'+foundString
  else:
    return ""

if __name__ == "__main__":
    if not os.popen(r'/usr/bin/smbclient -V 2>/dev/null').read():
        print banner
        print "Error: smbclient not found in the system! Please visit www.samba.org"
        sys.exit()    
    if '-h' in sys.argv or len(sys.argv) not in [2,3]:
      print banner
      print """run with parameters:  <IP> [user%pass]

<IP> could be like: 192.168.1.1 or 192.168.1.1/24 or 192.168.1.1-192.168.1.100
user%pass used to login to Windows system if testing non-anonymous access

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

"""
      sys.exit()
    if len(sys.argv) ==3:
        usernamePasswordParam = '-U '+sys.argv[2]    
    ipToScan = sys.argv[1]
    ipList = []
    try: #preparing IPs list
        if ipToScan.find("-")==-1 and ipToScan.count('.')==3:
            ips = ipaddr.IPNetwork(sys.argv[1])
            ipList = [str(x) for x  in list(ips)]
        if ipToScan.find("-")!=-1:
                import iprange
                ip12 = ipToScan.split('-')
                ip1 = iprange.ip2int(ip12[0])
                ip2 = iprange.ip2int(ip12[1])
                for r in iprange.getrange(ip1,ip2):
                    ips = ipaddr.IPNetwork(r)
                    ipList.extend([str(x) for x  in list(ips)])

        
    except ValueError:
       print "Error in IP!"
    
    for x in ipList:
        print "Scanning ",x
        if checkPort(x):
            res = getList(x)
            print res