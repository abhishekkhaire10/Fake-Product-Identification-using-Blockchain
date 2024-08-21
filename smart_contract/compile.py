from solcx import compile_standard, install_solc, get_installed_solc_versions
import json


with open("products2.sol", "r") as file:
    products2 = file.read()

install_solc("0.8.19")


# Get the Solidity compiler version
compiler_version = get_installed_solc_versions()

print(f"Solidity Compiler Version: {compiler_version}")

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"products2.sol": {"content": products2}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"] # output needed to interact with and deploy contract 
                }
            }
        },
    },
    solc_version="0.8.19",
)

print("Smart contract compiled successfully")

with open("compiled_code2.json", "w") as file:
    json.dump(compiled_sol, file)