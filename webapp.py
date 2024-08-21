from flask import Flask, render_template, request, redirect, url_for

import qrcode
from pyzbar.pyzbar import decode
from PIL import Image
from io import BytesIO

# import firebase_admin
# from firebase_admin import db, credentials

import uuid

from datetime import datetime

from web3 import Web3
import json

app = Flask(__name__,static_folder="./static")

# Connect  to Ethereum
with open("./smart_contract/compiled_code2.json", "r") as file:
    compiled_sol = json.load(file) 

bytecode = compiled_sol["contracts"]["products2.sol"]["Product"]["evm"]["bytecode"]["object"]

c_abi = json.loads(compiled_sol["contracts"]["products2.sol"]["Product"]["metadata"])["output"]["abi"]

# set up connection
w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))

# Check if connected to the node
if Web3.is_connected(w3):
    print("Connected to Ethereum node")
    # print("Web3 version:", w3.)
    print("Network ID:", w3.net.version)
    print("Node version:", w3.client_version)
else:
    print("Not connected to Ethereum node")

#Add view address functionality
my_address = "0xA058721E74D0cc75FeC36E85375B12ab1a4B3F31"
#private_key = os.getenv("PRIVATE_KEY")
private_key = '0x0815417aedd18600b6d0058dad868cdfecb875b46c12bcc6b2f374fec06a7134'
# Create a contract object
contract = w3.eth.contract(abi=c_abi, bytecode=bytecode)
# Get the number of latest transaction
nonce = w3.eth.get_transaction_count(my_address)
# print(w3.eth.gas_price)
print("Current Nonce: ", nonce)

with open("./smart_contract/smart_contract_address.txt", 'r') as file:
    contract_address = file.read()

contract_address =  '0x4f242E95ee667547a6DcED8A495098B50b1C8502'
products = w3.eth.contract(address=contract_address, abi=c_abi)


@app.route('/', methods=['GET','POST'])
def home():

    global p_name, s_id, s_name 
    if request.method == "POST":
        p_id = request.form["product_id"]
        p_name = request.form["product_name"]
        s_id = request.form["seller_id"]
        s_name= request.form["seller_name"]

    # #Generate Unique Id

    #     global p_id 
    #     p_id = uuid.uuid4().int

    #     fname = str(p_id).split("-")[0]
    #     # # print(fname)
    #     p_id = str(fname).replace('-','')

        #Add to Blockchain
        sell_product_tx = products.functions.setProduct(int(p_id),
                                                        p_name, int(s_id), s_name).transact({"from":my_address})

        #Generate QR

        qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
        )
        #Encode data

        url = "http://127.0.0.1:5000/"+p_id
        print(url)
        qr.add_data(url)
        qr.make(fit=True)

        #Create image
        img = qr.make_image(fill_color="black", back_color="white")

        #Save image
        img.save(p_name+'.jpg')

        # add redirect

    return render_template("manufacturer.html")


@app.route("/customer", methods=["GET","POST"])
def customer():
    if request.method == 'POST':
        file = request.files['file']

        # Read the image and decode QR codes
        image = Image.open(BytesIO(file.read()))
        qr_codes = decode(image)
        

        # Get the decoded data
        qr_data = [qr_code.data.decode('utf-8') for qr_code in qr_codes]
        print(qr_data)
        qr_data = qr_data[0].split("/")[-1]
        print(qr_data)

        if qr_data:
            return redirect(url_for("verification", p_id = qr_data))
    
    return render_template("customer.html")

@app.route("/seller", methods=["GET","POST"])
def seller():
    
    if request.method == "POST":    
        print(list(request.form.keys()))
        method_called = list(request.form.keys())[0]

        if method_called == 'product_id_sell':
            product_id = request.form['product_id_sell'] 
            print(products.functions.sellProduct(int(product_id)).transact({'from':my_address}))

        if method_called == 'product_id_view':
            product_id = request.form['product_id_view'] 
            view_products = products.functions.viewSellerProducts(int(product_id)).call()
            print(view_products)

            # Format Data
            view_products_updated = [[],[],[]]

            for x in range(len(view_products[0])):

                if view_products[0][x] != "0" and view_products[0][x] != 0:
                    view_products_updated[0].append(view_products[0][x])
                    view_products_updated[1].append(view_products[1][x])
                    if view_products[2][x] == 2:
                        product_status = "Not Sold"
                    else:
                        product_status = "Sold"
                    view_products_updated[2].append(product_status) 
                    # view_products_updated[0].append(x) 

            final_products = []

            for x in range(len(view_products_updated[0])):
                temp_list = []
                for y in range(3):
                    temp_list.append(view_products_updated[y][x])

                final_products.append(temp_list)
            print(temp_list)

            return render_template("seller.html", content = final_products)
    return render_template("seller.html")



@app.route("/verification/<p_id>", methods=["GET"])
def verification(p_id):
    ver_result = products.functions.verifyFakeness(int(p_id)).call()
    print(ver_result)


    
    if ver_result[1] == 1 :
        manSel = [ver_result[0], ver_result[3], ver_result[2]]
        print(manSel)

        sell_product = products.functions.sellProduct(int(p_id)).transact({"from":my_address})
        message = "Product is AUTHENTIC"
        return render_template("result.html", data = message, mansel = manSel)

    if ver_result[0] == "Invalid":
        sell_product = products.functions.sellProduct(int(p_id)).transact({"from":my_address})
        message = "Product not Tagged in the Blockchain"
        return render_template("result.html", data = message)
    
    else :

        message = """Product Scanned more than once
                    NOT AUTHENTIC"""
        return render_template("result.html", data = message)
    
# @app.route("/result", methods=["POST","GET"])
# def result(data):
#     return render_template("result.html", data = data)
    
if __name__ == '__main__':
    app.run(debug=True)