import time
import web3
from web3 import Web3
import json
from typing import Union
from eth_typing.evm import Address, ChecksumAddress
import itertools

AddressLike = Union[Address, ChecksumAddress]

rpc_eth = 'https://eth-mainnet.nodereal.io/v1/c373ebedfe4641209a7138dca098b6e6'
rpc_polygon = 'https://polygon-mainnet.nodereal.io/v1/b491dd1e97ed43e2bbab31aa1f9f7a27'

crv_polygon = '0x172370d5Cd63279eFa6d502DAB29171933a610AF'
usdc_polygon = '0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174'

quoter_contract_uni = '0xb27308f9f90d607463bb33ea1bebb41c27ce5ab6'
quoter_contract_sushi = '0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F'

quoter_contract_uni = Web3.toChecksumAddress(quoter_contract_uni)
quoter_contract_sushi = Web3.toChecksumAddress(quoter_contract_sushi)

"""
Pools
weth/crv 0x4c83a7f819a5c37d64b4c5a2f8238ea082fa1f4e - 1.0% (tvl - 7.5kk USD)
weth/crv 0x919fa96e88d67499339577fa202345436bcdaf79 - 0.3% (tvl - 134k USD)
weth/matic 0x290a6a7460b308ee3f19023d2d00de604bcf5b42 - 0.3% (tvl - 17.4kk USD)
usdc/matic 0x07a6e955ba4345bae83ac2a6faa771fddd8a2011 - 0.3% (tvl - 401.1kk USD)
weth/usdc 0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640 - 0.05% (tvl - 300kk USD)

tokens_eth = {'usdc': (Web3.toChecksumAddress('0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48'), 6, 150),
              'weth': (Web3.toChecksumAddress('0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2'), 18, 0.1),
              'crv': (Web3.toChecksumAddress('0xD533a949740bb3306d119CC777fa900bA034cd52'), 18, 150),
              'matic': (Web3.toChecksumAddress('0x7d1afa7b718fb893db30a3abc0cfc608aacfebb0'), 18, 220)}
"""

tokens_eth = {'usdc': (Web3.toChecksumAddress('0x2791bca1f2de4661ed88a30c99a7a9449aa84174'), 6, 150),
              'weth': (Web3.toChecksumAddress('0x7ceb23fd6bc0add59e62ac25578270cff1b9f619'), 18, 0.1),
              'crv': (Web3.toChecksumAddress('0x172370d5cd63279efa6d502dab29171933a610af'), 18, 150),
              'matic': (Web3.toChecksumAddress('0x0d500b1d8e8ef31e21c99d1db9a6444d3adf1270'), 18, 220)}


tokens_matic = {}

# uni_fees = [1000, 3000, 10000]
# exchange = ['uni', 'sushi']


paths = [x for i in range(2, 4) for x in itertools.permutations(['weth', 'crv', 'matic'], i)]
paths = [('usdc', ) + x + ('usdc', ) for x in paths]

all_quotes = [x for x in itertools.permutations(['weth', 'crv', 'matic', 'usdc'], 2)]

all_quotes_test_value = [x + (tokens_eth[x[1]][2], ) for x in all_quotes]


def open_abi(w3: Web3, abi: str, address: AddressLike):
    address = Web3.toChecksumAddress(address)
    with open(f'{abi}.abi', 'r') as f:
        json_abi = json.load(f)
    return w3.eth.contract(address=address, abi=json_abi)


connection_eth = Web3(Web3.HTTPProvider(rpc_eth))
connection_polygon = Web3(Web3.HTTPProvider(rpc_polygon))


for t in range(100):
    for quote in all_quotes_test_value:

        try:
            print(quote)
            univ3_price = open_abi(connection_polygon, 'abi/quotes', quoter_contract_uni).functions.quoteExactOutputSingle(
                            tokens_eth[quote[0]][0], tokens_eth[quote[1]][0], 3000, quote[2]*10 ** tokens_eth[quote[0]][1], 0).call()
            print(univ3_price/(quote[2] * 10 ** tokens_eth[quote[0]][1]))
        except (web3.exceptions.BadFunctionCallOutput, web3.exceptions.ContractLogicError):
            pass

        try:
            print(quote)
            sushi_price = open_abi(connection_polygon, 'abi_sushi/abi_pool', quoter_contract_sushi).\
                functions.getAmountsOut(quote[2] * 10 ** tokens_eth[quote[0]][1],
                                        [tokens_eth[quote[0]][0], tokens_eth[quote[1]][0]]).call()
            print(sushi_price[0] / sushi_price[1])

        except (web3.exceptions.BadFunctionCallOutput, web3.exceptions.ContractLogicError):
            pass
    time.sleep(13)



"""    
quote_contract = Web3.toChecksumAddress(quote_contract)
univ3_price = open_abi(connection_polygon, 'abi/quotes', quote_contract).functions.quoteExactOutputSingle(
    usdc_polygon, crv_polygon, 10000, 100*10 ** decimal_token0, 0).call()
print(univ3_price / (10 ** decimal_token1))
"""