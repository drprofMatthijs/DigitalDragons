from web3 import Web3, HTTPProvider
import requests
from dotenv import load_dotenv
import os
import time

load_dotenv()

# free plan: 5 calls per second, 100.000 calls per day
api_key_ether = os.getenv("API_KEY_ETHER")

# known Ethereum mixer wallets
KNOWN_MIXERS = ["0xd90e2f925da726b50c4ed8d0fb90ad053324f31b", "0x965274b48d51ed51edc513e3898d3d7bd501a08d", 
                "0x2aef852a7fc5bf4fe59f772f4ff31c542cde0f9b", "0x86aad66805bc6eb3c2bf6b42be9c5b6e11acabcf", 
                "0x3596ab8a5ee92cccba2bec73a46f80d6200c2431", "0x86aa28b3ffdf690753ba056261445bfe3929e6d3", 
                "0xfaa27aaa43e1a42b80a976b17e9ca40aeaaf7a75", "0xf57de72ca0e918f44af21e3703d6fd1aa6783910", 
                "0x08C6698d31A2e1b2d4Ca4f940E502feEbc9100D3", "0x52a038F3338506198d5B96F793329123162cFF4a", 
                "0x0eE0E47D025783EC7a19F016144476B6e284553C", "0x0dE5eD64046aba8D57211b6AA5610c699Ce29d47", 
                "0x00901b216F9b1D788CF19202f23E9BAaaAa4773a", "0xf1ddb09a3305c794772b1b196ea1b21e2974d182"]

twodaysago = round(time.time() - 60 * 60 * 24 * 2)
request = f'https://api.etherscan.io/v2/api?chainid=1&module=block&action=getblocknobytime&timestamp={twodaysago}&closest=after&apikey={api_key_ether}'
result = requests.get(request)

# block from two days ago
block = result.json()['result']

def get_transactions(address):
    req = f'https://api.etherscan.io/api?module=account&action=txlistinternal&address={address}&startblock={block}&page=1&offset=100&sort=asc&apikey={api_key_ether}'
    res = requests.get(req)
    return res.json()['result']

def trace_wallet(address, visited, depth):
    # now not going deeper than 2, computational limits
    if depth > 2:
        return None
    if address in visited:
        return None
    visited.append(address)
    # print(f"checking address {address} at depth {depth}, but first waiting 5 seconds")
    time.sleep(5)

    txs = get_transactions(address)
    for tx in txs:
        sender = tx['from']
        receiver = tx['to']

        if sender in KNOWN_MIXERS or receiver in KNOWN_MIXERS:
            return depth

        next_addresses = [sender, receiver]
        for addr in [x for x in next_addresses if x != ""]:
            result = trace_wallet(addr, visited, depth + 1)
            if result is not None:
                return result
    return None

def proximity_check(public_key: str):
    result = trace_wallet(public_key, [], 0)

    if result is not None:
        return f'Mixer address found at depth {result}, be careful'
    else:
        return"No mixer address found in address proximity"
