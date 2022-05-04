import argparse
import hashlib
import time
import sys, os
import binascii
import hmac, struct
import bit
from bit import Key
from bit.format import bytes_to_wif
from multiprocessing import Event, Process, Queue, Value, cpu_count
import requests
import ctypes
import platform
import secrets

import secp256k1 as ice
import base58
import codecs
from pathlib import Path
from colored import fg, bg, attr

textcolor = "#008000"
order	= 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141



entropy_bits = 128                     
derivation_total_path_to_check = 1     

words = 'Cometomefuck1!'




def mnem_to_seed(words):
    salt = 'Melodic_death_metal-2033!'
    seed = hashlib.pbkdf2_hmac("sha512",words.encode("utf-8"), salt.encode("utf-8"), 13666)
    return seed


def bip39seed_to_bip32masternode(seed):
    h = hmac.new(b'Bitcoin seed', seed, hashlib.sha512).digest()
    key, chain_code = h[:32], h[32:]
    return key, chain_code

def parse_derivation_path(str_derivation_path="m/44'/0'/0'/13/666"):      # 60' is for ETH 0' is for BTC
    path = []
    if str_derivation_path[0:2] != 'm/':
        raise ValueError("Can't recognize derivation path. It should look like \"m/44'/0'/0'/0\".")
    for i in str_derivation_path.lstrip('m/').split('/'):
        if "'" in i:
            path.append(0x80000000 + int(i[:-1]))
        else:
            path.append(int(i))
    return path
    
def parse_derivation_path2(str_derivation_path="m/49'/0'/0'/13/666"):      
    path = []
    if str_derivation_path[0:2] != 'm/':
        raise ValueError("Can't recognize derivation path. It should look like \"m/49'/0'/0'/0\".")
    for i in str_derivation_path.lstrip('m/').split('/'):
        if "'" in i:
            path.append(0x80000000 + int(i[:-1]))
        else:
            path.append(int(i))
    return path
    
def derive_bip32childkey(parent_key, parent_chain_code, i):
    assert len(parent_key) == 32
    assert len(parent_chain_code) == 32
    k = parent_chain_code
    if (i & 0x80000000) != 0:
        key = b'\x00' + parent_key
    else:
#        key = bytes(PublicKey(parent_key))
        key = bit.Key.from_bytes(parent_key).public_key
    d = key + struct.pack('>L', i)
    while True:
        h = hmac.new(k, d, hashlib.sha512).digest()
        key, chain_code = h[:32], h[32:]
        a = int.from_bytes(key, byteorder='big')
        b = int.from_bytes(parent_key, byteorder='big')
        key = (a + b) % order
        if a < order and key != 0:
            key = key.to_bytes(32, byteorder='big')
            break
        d = b'\x01' + h[32:] + struct.pack('>L', i)
    return key, chain_code
    
def bip39seed_to_private_key2(bip39seed, n=1):
    const = "m/49'/0'/13'/666/"
#    str_derivation_path = const + str(n-1)
    str_derivation_path = "m/49'/0'/0'/13/666"
    derivation_path = parse_derivation_path2(str_derivation_path)
    master_private_key, master_chain_code = bip39seed_to_bip32masternode(bip39seed)
    private_key, chain_code = master_private_key, master_chain_code
    for i in derivation_path:
        private_key, chain_code = derive_bip32childkey(private_key, chain_code, i)
    return private_key

def bip39seed_to_private_key(bip39seed, n=1):
    const = "m/44'/0'/13'/666/"
#    str_derivation_path = const + str(n-1)
    str_derivation_path = "m/44'/0'/0'/13/666"
    derivation_path = parse_derivation_path(str_derivation_path)
    master_private_key, master_chain_code = bip39seed_to_bip32masternode(bip39seed)
    private_key, chain_code = master_private_key, master_chain_code
    for i in derivation_path:
        private_key, chain_code = derive_bip32childkey(private_key, chain_code, i)
    return private_key
    
def startt():
    seed = mnem_to_seed(words)
    pvk = bip39seed_to_private_key(seed, derivation_total_path_to_check)
    pvk2 = bip39seed_to_private_key2(seed, derivation_total_path_to_check)
    h1601 = ice.privatekey_to_address(0, True, (int.from_bytes(pvk, "big")))
    h1602 = ice.privatekey_to_address(1, True, (int.from_bytes(pvk2, "big")))
    print('addr')
    print(h1601)
    print('hex')
    print(pvk.hex())
    print('addr1')
    print(h1602)
    print('hex2')
    print(pvk2.hex())
    return 
    
    
if __name__ == '__main__':
    startt()