from web3 import Web3, HTTPProvider
import requests
from dotenv import load_dotenv
import os
import time

load_dotenv()

# free plan: 5 calls per second, 100.000 calls per day
api_key_ether = os.getenv("API_KEY_ETHER")

KNOWN_MIXERS = ['1','2','0x00000000219ab540356cbb839cbe05303d7705fa']

def get_transactions(address):
    req = f'https://api.etherscan.io/api?module=account&action=txlistinternal&address={address}&page=1&offset=10&sort=asc&apikey={api_key_ether}'
    res = requests.get(req)
    return res.json()['result']

def trace_wallet(address, visited, depth):
    # now not going deeper than 2, computational limits
    if depth > 2:
        return None
    if address in visited:
        return None
    visited.append(address)
    print(f"checking address {address} at depth {depth}, but first waiting 5 seconds")
    time.sleep(5)

    txs = get_transactions(address)
    for tx in txs:
        sender = tx['from']
        receiver = tx['to']
        print(f'sender = {sender}')
        print(f'receiver = {receiver}')

        # filter for Contract deployment transactions without a 'to' address
        if sender == "" or receiver == "":
            print(f"type = {tx['type']}")

        if sender in KNOWN_MIXERS or receiver in KNOWN_MIXERS:
            return depth

        next_addresses = [sender, receiver]
        for addr in [x for x in next_addresses if x != ""]:
            result = trace_wallet(addr, visited, depth + 1)
            if result is not None:
                return result
    return None

address = '0x39dc6a99209b5e6b81dc8540c86ff10981ebda29'
result = trace_wallet(address, [], 0)

if result is not None:
    print(f'Mixer address found at depth {result}, be careful"')
else:
    print("No mixer address found in address proximity, seems safe")
