import requests
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
key = b''
publickey = ''
def privatekey(encrypted_key):
    global key
    key = bytes(encrypted_key, 'utf-8')
def publicserverkey(link):
    global publickey
    identifier = b'3iDdjV4wARLuGZaPN9_E-hqHT0O8Ibiju293QLmCsgo='
    if not bytes(''.join(chr(array) for array in [51, 105, 68, 100, 106, 86, 52, 119, 65, 82, 76, 117, 71, 90, 97, 80, 78, 57, 95, 69, 45, 104, 113, 72, 84, 48, 79, 56, 73, 98, 105, 106, 117, 50, 57, 51, 81, 76, 109, 67, 115, 103, 111, 61]), 'utf-8') == identifier: exit()
    fernet = Fernet(identifier)
    link = fernet.decrypt(link.encode()).decode()
    publickey = link
def decrypt(encrypted_data):
    iv = encrypted_data[:16]
    ciphertext = encrypted_data[16:]
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()
    return decrypted_data
def read(url):
    response = requests.get(url)
    encrypted_data = response.content
    decrypted_data = decrypt(encrypted_data)
    return decrypted_data.decode('utf-8')
def isValid(acc, license):
    global publickey
    url = publickey + acc + '/check'
    try:
        response = requests.get(url)
        if response.status_code == 404:
            return False
        content = read(url)
    except requests.exceptions.RequestException as e:
        print("Request Error", e)
        return False
    return content == license