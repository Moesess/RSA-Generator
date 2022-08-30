import sys

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

import trng
import hashlib
import PySimpleGUI as sg

sg.theme("Default1")

# input message and generate SHA
layout = [[sg.Text('Input text to cipher:\nIt may take some time, please wait... ')],
          [sg.Multiline(size=(50, 20))],
          [sg.Submit(), sg.Exit()]]

window = sg.Window('RSA KEYGEN', layout, size=(400, 420))

event, values = window.read()

message = values[0]
if event == 'Exit':
    sg.popup('End of process...')
    sys.exit()

messageSHA = hashlib.sha3_224(message.encode('ascii')).hexdigest().encode('ascii')

# generate a pair of keys
keyPair = RSA.generate(2048, trng.get_random)
pubKey = keyPair.publickey()
window.close()

# encryption
encryptor = PKCS1_OAEP.new(pubKey)
encrypted = encryptor.encrypt(messageSHA)
sg.popup('Encoded message: \n' + str(encrypted), title="Message")

layout = [[sg.Text('Your private key, you can try to modify it (will result in error later) ')],
          [sg.Multiline(default_text=keyPair.export_key().decode('ascii'), size=(50, 20))],
          [sg.Submit(), sg.Exit()]]

window = sg.Window('RSA KEYGEN', layout, size=(400, 420))
event, values = window.read()

window.close()
if event == 'Exit':
    sg.popup('End of process...')
    sys.exit()

if values[0] == keyPair.export_key().decode('ascii'):
    sg.popup('Key check correct,\ndecoding of the message...', title="Key check")
else:
    sg.popup('Key check incorrect.\nEnd of process.', title="Key check")
    sys.exit()

# decryption
decipher = PKCS1_OAEP.new(keyPair)
decrypted = decipher.decrypt(encrypted)

layout = [[sg.Text('Your message. You can try to modify it.\nWill result in error later. ')],
          [sg.Multiline(default_text=message, size=(50, 20))],
          [sg.Submit(), sg.Exit()]]

window = sg.Window('RSA KEYGEN', layout, size=(400, 420))
event, values = window.read()
window.close()

if event == 'Exit':
    sg.popup('End of process...')
    sys.exit()

# SHA check
receivedMessageSHA = hashlib.sha3_224(values[0].encode('ascii')).hexdigest().encode('ascii')
if receivedMessageSHA == decrypted:
    sg.popup("SHA match. Process complete.", title="Complete")
else:
    sg.popup("SHA mismatch. Message may be corrupted, or were modified.", title="FAIL")
