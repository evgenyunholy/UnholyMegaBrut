import random
import hashlib
import binascii
import secp256k1 as ice
import ctypes
import multiprocessing
from multiprocessing import pool, Event, Process, Queue, Value, cpu_count
import time
import sys
import itertools
import os
from pathlib import Path
from secrets import token_bytes
from bloomfilter import BloomFilter, ScalableBloomFilter, SizeGrowthRate

mys = Path(__file__).resolve()
fil = mys.parents[1] / 'found/found.txt'
myselff = Path(__file__).resolve()
ress = myselff.parents[1] / 'datafiles/BF/btc.bf'
myselfff = Path(__file__).resolve()
resss = myselfff.parents[1] / 'datafiles/BF/eth.bf'


with open(resss, "rb") as fp:
    bloom_filter1 = BloomFilter.load(fp)   

with open(ress, "rb") as fp:
    bloom_filter = BloomFilter.load(fp)  

def brut(cores='all'):   
    
    available_cores = cpu_count()

    if cores == 'all':
        cores = available_cores
    elif 0 < int(cores) <= available_cores:
        cores = int(cores)
    else:
        cores = 1
    counter = Value('L')
    workers = []
    for r in range(cores):
        p = Process(target=main, args=(counter, r))
        workers.append(p)
        p.start()

    for worker in workers:
        worker.join()
    

    
def gen1():
    pvk = token_bytes(32)
    return pvk

    
def HASH160(pubk_bytes):
    return hashlib.new('ripemd160', hashlib.sha256(pubk_bytes).digest() ).digest()
    
def main(counter, r):
    st = time.time()
    screen_print_after_keys = 10000
    found = 0
    k = 1
    while True:
        with counter.get_lock():
            counter.value += 1
        pvk = gen1()
        pvkhex = pvk.hex()
        addr1 = ice.privatekey_to_address(0, False, (int.from_bytes(pvk, "big")))
        addr2 = ice.privatekey_to_address(0, True, (int.from_bytes(pvk, "big")))
        addr3 = ice.privatekey_to_address(1, True, (int.from_bytes(pvk, "big")))
        addr4 = ice.privatekey_to_address(2, True, (int.from_bytes(pvk, "big")))
        addr5 = ice.privatekey_to_ETH_address(int.from_bytes(pvk, "big"))
        
      
        if addr1 in bloom_filter or addr2 in bloom_filter or addr3 in bloom_filter or addr4 in bloom_filter or addr5 in bloom_filter1:
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
            g=open(fil,"a")
            g.write('===== Made by EvgenyUnholy |  Donations 35dex592mVX6EiF6ag9ZJzWAQrobz3ciDu  |   https://github.com/evgenyunholy   =====\n')
            g.write(addr1)
            g.write("\n" + addr2)
            g.write("\n" + addr3)
            g.write("\n" + addr4)
            g.write("\n" + addr5)
            g.write("\n" + pvk.hex() + "\n")      
            g.close()
        else:
            if k % screen_print_after_keys == 0:
                ctypes.windll.kernel32.SetConsoleTitleW("UnholyPrivateKeyGeneration")
                print('Checked: {} Found: {} Keys/s: {} Pvk: {}'.format(counter.value*5, found, round(counter.value/(time.time() - st)), pvkhex), end='\r')
        k += 1





if __name__ == '__main__':
    brut(cores = int(input("Cores count: ")))
        
   
   
