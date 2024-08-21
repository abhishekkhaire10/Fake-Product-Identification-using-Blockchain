import qrcode
from pyzbar.pyzbar import decode
from PIL import Image

import firebase_admin
from firebase_admin import db, credentials

import uuid

from datetime import datetime

# Authenticate to firebase

global ref
cred = credentials.Certificate("cred.json")
firebase_admin.initialize_app(cred, {'databaseURL':'https://qrcode-b9cfa-default-rtdb.asia-southeast1.firebasedatabase.app/'})
ref = db.reference("/")
    # print(ref.)


#Generate Unique Id

global uid
global fname
uid = uuid.uuid4()

fname = str(uid).split("-")[0]
# print(fname)
uid = str(uid).replace('-','')
# print(uid)



#Generate QR

qr = qrcode.QRCode(
version=1,
error_correction=qrcode.constants.ERROR_CORRECT_L,
box_size=10,
border=4,
)

#Encode data

qr.add_data(data)
qr.make(fit=True)

#Create image
img = qr.make_image(fill_color="black", back_color="white")

#Save image
img.save(filename+'.jpg')

    #Add to database




if __name__ == "__main__":
    # uniqueIdGenerator()
    # generate_qr(uid, fname)
    run_db()

