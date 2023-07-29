from web3 import Web3
import json
import os

POKT_URL = "https://celo-mainnet.gateway.pokt.network/v1/lb/3a88a905b9e6d3e7a47f1187"
web3 = Web3(Web3.HTTPProvider(POKT_URL))

connected = web3.isConnected()
print(f"Connected to Celo Blockchain: {connected}")

# Address of  ubeswap factory
ubeswap_factory_address = '0x62d5b84bE28a183aBB507E125B384122D2C25fAE'
# Address of  ubeswap router
ubeswap_router_address = '0xE3D8bd6Aed4F159bc8000a9cD47CffDb95F96121'

# load ubeswap_factory_abi
with open('ubeswap_factory_abi.json') as f:
    factory_abi = json.load(f)
# load ubeswap_pair_abi
with open('ubeswap_pair_abi.json') as f:
    pair_abi = json.load(f)


def get_celo_price():
    try:
        # Get the pair address of Celo
        factory_contract = web3.eth.contract(address=ubeswap_factory_address, abi=factory_abi)
        celo_address = web3.toChecksumAddress('0x471ece3750da237f93b8e339c536989b8978a438')
        cusd_address = web3.toChecksumAddress('0x918146359264c492bd6934071c6bd31c854edbc3')
        contract_address = factory_contract.functions.getPair(celo_address, cusd_address).call()

        # Get the contract instance of the Celo pair
        pair_contract = web3.eth.contract(address=contract_address, abi=pair_abi)

        # Get the reserves from the pair contract
        reserves = pair_contract.functions.getReserves().call()
        token_reserve, cusd_reserve = reserves[0], reserves[1]

        # Calculate the  price in CUSD
        token_price = cusd_reserve / token_reserve

        return token_price
    except Exception as e:
        print("Error retrieving Celo price:", str(e))
        return None



celo_price = get_celo_price()
# Print the price 
if celo_price is not None:
        print(f"The price of celo is {celo_price:.4f} CUSD")
else:
        print("Failed to fetch celo price.")
