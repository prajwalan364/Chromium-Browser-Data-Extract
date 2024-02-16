import os
import json
import base64
from Cryptodome.Cipher import AES
import win32crypt


def decrypt_passwords(cipher_text, path):
    # Getting the Matser key
    with open(path) as f:
        local_state = f.read()
        local_state = json.loads(local_state)

    master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    master_key = master_key[5:]  # removing DPAPI
    master_key = win32crypt.CryptUnprotectData(master_key, None, None, None, 0)[1]

    try:
        # Extracting IV
        IV = cipher_text[3:15]
        # Extract Encrypted Password
        encrypted_paswd = cipher_text[15:-16]

        cipher = AES.new(master_key, AES.MODE_GCM, IV)
        decrypted_pass = cipher.decrypt(encrypted_paswd)
        decrypted_pass = decrypted_pass.decode()
    except Exception as e:
        print(e)

    return decrypted_pass
