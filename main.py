import time

from web3 import Web3
import json
from typing import Union
from eth_typing.evm import Address, ChecksumAddress

AddressLike = Union[Address, ChecksumAddress]

rpc_eth = 'https://eth-mainnet.nodereal.io/v1/c373ebedfe4641209a7138dca098b6e6'
rpc_polygon = 'https://polygon-mainnet.nodereal.io/v1/b491dd1e97ed43e2bbab31aa1f9f7a27'
quote_contract = '0xb27308f9f90d607463bb33ea1bebb41c27ce5ab6'
crv_eth = '0xD533a949740bb3306d119CC777fa900bA034cd52'
usdc_eth = '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48'
crv_polygon = '0x172370d5Cd63279eFa6d502DAB29171933a610AF'
usdc_polygon = '0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174'


def open_abi(w3: Web3, abi: str, address: AddressLike):
    address = Web3.toChecksumAddress(address)
    with open(f'{abi}.abi', 'r') as f:
        json_abi = json.load(f)
    return w3.eth.contract(address=address, abi=json_abi)


connection_eth = Web3(Web3.HTTPProvider(rpc_eth))
connection_polygon = Web3(Web3.HTTPProvider(rpc_polygon))


decimal_token0 = open_abi(connection_eth, 'abi/erc20', Web3.toChecksumAddress(crv_eth)).functions.decimals().call()
decimal_token1 = open_abi(connection_eth, 'abi/erc20', Web3.toChecksumAddress(usdc_eth)).functions.decimals().call()
print(decimal_token0)
print(decimal_token1)


for i in range(100):
    quote_contract = Web3.toChecksumAddress(quote_contract)
    univ3_price = open_abi(connection_eth, 'abi/quotes', quote_contract).functions.quoteExactOutputSingle(usdc_eth,
                                                                                                          crv_eth,
                                                                                                          10000,
                                                                                                          100*10 ** decimal_token0,
                                                                                                          0).call()
    print(univ3_price / (10 ** decimal_token1))
    quote_contract = Web3.toChecksumAddress(quote_contract)
    univ3_price = open_abi(connection_polygon, 'abi/quotes', quote_contract).functions.quoteExactOutputSingle(
        usdc_polygon, crv_polygon, 10000, 100*10 ** decimal_token0, 0).call()
    print(univ3_price / (10 ** decimal_token1))
    time.sleep(13)