from web3 import Web3

w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))

c_abi = [
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "sProductId",
				"type": "uint256"
			}
		],
		"name": "sellProduct",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "productId",
				"type": "uint256"
			},
			{
				"internalType": "string",
				"name": "pOwner",
				"type": "string"
			}
		],
		"name": "setProduct",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "vProductId",
				"type": "uint256"
			}
		],
		"name": "verifyFakeness",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			},
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "viewProducts",
		"outputs": [
			{
				"internalType": "uint256[]",
				"name": "",
				"type": "uint256[]"
			},
			{
				"internalType": "string[]",
				"name": "",
				"type": "string[]"
			},
			{
				"internalType": "uint256[]",
				"name": "",
				"type": "uint256[]"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]

my_address = "0xe2abeBd2857d978b5b26f6370122b3e91ec40D07"

private_key = "0x3f494d9d6b092a470b94c78cdfa862fbb85ab2cae13e040117ecbd42d7ad5e1a"

nonce = w3.eth.get_transaction_count(my_address)

print(w3.eth.gas_price)
print(nonce)

gas_price = w3.eth.gas_price
gas_limit = 30000000

contract_address = "0xab537A1772F1ADb068082911FA2f14B8D3812D20"

#Interacting with the contract

products = w3.eth.contract(address=contract_address, abi=c_abi)

# add_product = products.functions.setProduct(12, "Redmi").transact({'from': my_address})

# sell_product = products.functions.sellProduct(12).transact({'from': my_address})

# verify_fakeness = products.functions.verifyFakeness(12).transact({'from': my_address})

# # Sign the transaction
# sign_contract = w3.eth.account.sign_transaction(add_product, private_key)
# # Send the transaction
# send_store_contact = w3.eth.send_raw_transaction(sign_contract.rawTransaction)

# transaction_receipt = w3.eth.wait_for_transaction_receipt(verify_fakeness)

print(products.functions.verifyFakeness(12).call())
