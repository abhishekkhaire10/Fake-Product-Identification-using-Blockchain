import json
from web3 import Web3
# get bytecode

with open("compiled_code2.json", "r") as file:
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

# Create the contract in Python
# Create a contract object
contract = w3.eth.contract(abi=c_abi, bytecode=bytecode)

# Get the number of latest transaction
nonce = w3.eth.get_transaction_count(my_address)
# print(w3.eth.gas_price)
print("Nonce Number: ",nonce)


# build transaction

# Set the gas price and gas limit (you may need to adjust these)
gas_price = w3.eth.gas_price
gas_limit = 30000000

# Build the transaction

transaction = contract.constructor().build_transaction({
    'from': my_address,
    'nonce': nonce,
		'gasPrice':gas_price

})

# Sign the transaction
signed_transaction = w3.eth.account.sign_transaction(transaction, private_key)

# Send the transaction
transaction_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)

print(f"Transaction sent: {transaction_hash.hex()}")

# # Wait for the contract to be mined
transaction_receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)
# # Get the deployed contract address
contract_address =  transaction_receipt["contractAddress"]
print(f"Contract deployed at address: {contract_address}")

with open("smart_contract_address.txt","w") as file:
    file.write(str(contract_address))


#Interacting with the contract
# products = w3.eth.contract(address=contract_address, abi=c_abi)

# add_product_tx = products.functions.setProduct(1, "Redmi", 1, "Malakar").transact({"from":my_address})

# sell_product_tx = products.functions.sellProduct(1).transact({"from":my_address})

# # Sign the transaction
# sign_contract = w3.eth.account.sign_transaction(add_product_tx, private_key)
# # Send the transaction
# send_store_contact = w3.eth.send_raw_transaction(sign_contract.rawTransaction)

# transaction_receipt = w3.eth.wait_for_transaction_receipt(add_product)

#View All Products
# Format
# [[3, 1, 1], ['iPhone', 'Redmi', 'Redmi'], [2, 2, 2], [1, 2, 2], ['Malakar', 'Malakar', 'Malakar']]
#  Product Id   Product Name 			   Status	 Seller Id   Seller name
# print(products.functions.viewAllProducts().call())

# View Seller products
# [['0', 'Redmi', 'Redmi'],  [0, 2, 2]]
# Products('0' mean no product at that index)     Status

# print(products.functions.viewSellerProducts(1).call())
