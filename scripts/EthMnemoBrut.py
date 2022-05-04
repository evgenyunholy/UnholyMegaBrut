import argparse
import hashlib
import time
import sys, os
import binascii
import hmac, struct
import bit
from multiprocessing import Event, Process, Queue, Value, cpu_count
import requests
import ctypes
from bloomfilter import BloomFilter, ScalableBloomFilter, SizeGrowthRate
import platform
import secrets
from colored import fg, bg, attr
import eth_keys
from eth_keys import keys

import threading
import secp256k1 as ice
from pathlib import Path

order	= 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
textcolor = "#008000"
myself = Path(__file__).resolve()
res = myself.parents[1] / 'datafiles/wordlist/english.txt'

with open(res) as f:
    wordlist = f.read().split('\n')
    
myselff = Path(__file__).resolve()
ress = myselff.parents[1] / 'datafiles/BF/eth.bf'

with open(ress, "rb") as fp:
    bloom_filter = BloomFilter.load(fp)    
    
mys = Path(__file__).resolve()
fil = mys.parents[1] / 'found/found.txt'



entropy_bits = 128                      
derivation_total_path_to_check = 1    
    
token = ''                              #telegram token and id
method = 'sendMessage'                                     
user_id = ''

def sendBotMsg(msg):
     response = requests.post(
        url=f'https://api.telegram.org/bot{token}/{method}',
        data={'chat_id': {user_id}, 'text': {msg}}
    )

   

def check_address(addr):
    flag = False
    if addr in bloom_filter:
        flag = True
    return flag


def create_valid_mnemonics(strength=128):

    rbytes = os.urandom(strength // 8)
    h = hashlib.sha256(rbytes).hexdigest()
    
    b = ( bin(int.from_bytes(rbytes, byteorder="big"))[2:].zfill(len(rbytes) * 8) \
         + bin(int(h, 16))[2:].zfill(256)[: len(rbytes) * 8 // 32] )
    
    result = []
    for i in range(len(b) // 11):
        idx = int(b[i * 11 : (i + 1) * 11], 2)
        result.append(wordlist[idx])

    return " ".join(result)




def mnem_to_seed(words):
    salt = 'mnemonic'
    seed = hashlib.pbkdf2_hmac("sha512",words.encode("utf-8"), salt.encode("utf-8"), 2048)
    return seed


def bip39seed_to_bip32masternode(seed):

    h = hmac.new(b'Bitcoin seed', seed, hashlib.sha512).digest()
    key, chain_code = h[:32], h[32:]
    return key, chain_code


def parse_derivation_path(str_derivation_path="m/44'/60'/0'/0/0"):      # 60' is for ETH 0' is for BTC
    path = []
    if str_derivation_path[0:2] != 'm/':
        raise ValueError("Can't recognize derivation path. It should look like \"m/44'/0'/0'/0\".")
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

def bip39seed_to_private_key(bip39seed, a=0):
    const = "m/44'/60'/0'/0/"

    str_derivation_path = "m/44'/60'/0'/0/0"
    derivation_path = parse_derivation_path(str_derivation_path)
    master_private_key, master_chain_code = bip39seed_to_bip32masternode(bip39seed)
    private_key, chain_code = master_private_key, master_chain_code
    for i in derivation_path:
        private_key, chain_code = derive_bip32childkey(private_key, chain_code, i)
    return private_key





def do_work_loop(entropy_bits):
    mnem = create_valid_mnemonics(strength=128)
    seed = mnem_to_seed(mnem)
    pvk = bip39seed_to_private_key(seed, derivation_total_path_to_check)
    addr = ice.privatekey_to_ETH_address(int.from_bytes(pvk, "big"))
    flg = check_address(addr)
    return mnem, flg, addr


  

def hunt_ETH_mnemonics(cores='all'):  
    
    available_cores = cpu_count()

    if cores == 'all':
        cores = available_cores
    elif 0 < int(cores) <= available_cores:
        cores = int(cores)
    else:
        cores = 1

    counter = Value('L')
    match = Event()
    queue = Queue()

    workers = []
    for r in range(cores):
        p = Process(target=generate_mnem_address_pairs, args=(counter, match, queue, r))
        workers.append(p)
        p.start()

    for worker in workers:
        worker.join()
    
    keys_generated = 0
    while True:
        time.sleep(1)
        current = counter.value
        if current == keys_generated:
            if current == 0:
                continue
            break
        keys_generated = current
        s = 'Total Mnemonics generated: {}\r'.format(keys_generated)

        sys.stdout.write(s)
        sys.stdout.flush()

    mnem_words, address = queue.get()
    print('\n\nFinal Mnemonics Words (English): ', mnem_words)
    print('BTC Address: {}'.format(address))
    msg ='Address: {} | Mnemonic phrase:                    {}'.format(address, mnem_words)
    sendBotMsg(msg)
    f=open(fil,"a")
    f.write("\n"+address)
    f.write("\n"+mnem_words)      
    f.close()
    return
#==============================================================================
def generate_mnem_address_pairs(counter, match, queue, r):
    st = time.time()
    k = 1
    found = 0
    screen_print_after_keys = 1000
    while True:
        if match.is_set():
            return

        with counter.get_lock():
            counter.value += 1
            
        mnem, flg, addr = do_work_loop(entropy_bits)
        
        if k % screen_print_after_keys == 0:

            print('Checked: {} | Found {} | Keys/s: {} | Address: {}'.format(counter.value, found, round(counter.value/(time.time() - st)), addr), end='\r')
            ctypes.windll.kernel32.SetConsoleTitleW("                                                                                                                                 UnholyEthBrut")
            
        if flg == True:
            match.set()
            print(    '''
──────────────────██████────────────────
─────────────────████████─█─────────────
─────────────██████████████─────────────
─────────────█████████████──────────────
──────────────███████████───────────────
───────────────██████████───────────────
────────────────████████────────────────
────────────────▐██████─────────────────
────────────────▐██████─────────────────
──────────────── ▌─────▌────────────────
────────────────███─█████───────────────
────────────████████████████────────────
──────────████████████████████──────────
────────████████████─────███████────────
──────███████████─────────███████───────
─────████████████───██─███████████──────
────██████████████──────────████████────
───████████████████─────█───█████████───
──█████████████████████─██───█████████──
──█████████████████████──██──██████████─
─███████████████████████─██───██████████
████████████████████████──────██████████
███████████████████──────────███████████
─██████████████████───────██████████████
─███████████████████████──█████████████─
──█████████████████████████████████████─
───██████████████████████████████████───
───────██████████████████████████████───
───────██████████████████████████───────
─────────────███████████████────────────
    ''')
            queue.put_nowait((mnem, addr))
            found += 1
            return
        
        k += 1

def hunt_ETH_mnemonics1(cores='all'):  
    
    available_cores = cpu_count()

    if cores == 'all':
        cores = available_cores
    elif 0 < int(cores) <= available_cores:
        cores = int(cores)
    else:
        cores = 1

    counter = Value('L')
    match = Event()
    queue = Queue()

    workers = []
    for r in range(cores):
        p = Process(target=generate_mnem_address_pairs1, args=(counter, match, queue, r))
        workers.append(p)
        p.start()

    for worker in workers:
        worker.join()
    
    keys_generated = 0
    while True:
        time.sleep(1)
        current = counter.value
        if current == keys_generated:
            if current == 0:
                continue
            break
        keys_generated = current
        s = 'Total Mnemonics generated: {}\r'.format(keys_generated)

        sys.stdout.write(s)
        sys.stdout.flush()

    mnem_words, address = queue.get()
    print('\n\nFinal Mnemonics Words (English): ', mnem_words)
    print('BTC Address: {}'.format(address))
    msg ='Address: {} | Mnemonic phrase:                    {}'.format(address, mnem_words)
    sendBotMsg(msg)
    f=open(fil,"a")
    f.write("\n"+address)
    f.write("\n"+mnem_words)      
    f.close()
    return

def generate_mnem_address_pairs1(counter, match, queue, r):
    st = time.time()
    k = 1
    found = 0
    screen_print_after_keys = 1
    while True:
        if match.is_set():
            return

        with counter.get_lock():
            counter.value += 1
            
        mnem, flg, addr = do_work_loop(entropy_bits)
        
        if k % screen_print_after_keys == 0:
            print('{} Addr: {} Mnem: {}'.format(fg(textcolor), addr, mnem))
            ctypes.windll.kernel32.SetConsoleTitleW("UnholyEthBrut  Found: {} | Keys Checked : {} | Keys/s: {}  ".format(found, counter.value, round(counter.value/(time.time() - st))))
            
        if flg == True:
            print(    '''
──────────────────██████────────────────
─────────────────████████─█─────────────
─────────────██████████████─────────────
─────────────█████████████──────────────
──────────────███████████───────────────
───────────────██████████───────────────
────────────────████████────────────────
────────────────▐██████─────────────────
────────────────▐██████─────────────────
──────────────── ▌─────▌────────────────
────────────────███─█████───────────────
────────────████████████████────────────
──────────████████████████████──────────
────────████████████─────███████────────
──────███████████─────────███████───────
─────████████████───██─███████████──────
────██████████████──────────████████────
───████████████████─────█───█████████───
──█████████████████████─██───█████████──
──█████████████████████──██──██████████─
─███████████████████████─██───██████████
████████████████████████──────██████████
███████████████████──────────███████████
─██████████████████───────██████████████
─███████████████████████──█████████████─
──█████████████████████████████████████─
───██████████████████████████████████───
───────██████████████████████████████───
───────██████████████████████████───────
─────────────███████████████────────────
    ''')
            match.set()
            queue.put_nowait((mnem, addr))
            found += 1
            return
        
        k += 1


if __name__ == '__main__':
    print('=================================================== EthMnemBrut =======================================================')
    vvod = int(input("\n1 - Print only count(fast); \n2 - Print all(slow) \nChoose format and display print: "))
    if vvod == 1:
        hunt_ETH_mnemonics(cores = int(input("Cores count: ")))
        pass
    elif vvod == 2:
        hunt_ETH_mnemonics1(cores = int(input("Cores count: ")))
        pass              
    else:
        print("ERROR!!! Please input correct number")
        quit()

    