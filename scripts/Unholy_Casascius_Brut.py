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
from pathlib import Path
from bloomfilter import BloomFilter, ScalableBloomFilter, SizeGrowthRate
ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
myself = Path(__file__).resolve()
filename = myself.parents[1] / 'datafiles/BF/casascius.txt'



with open(filename) as file:
    add = file.read().split()
add = set(add)


def sha256(x):
    return hashlib.sha256(x).digest()




    

def brut3(cores='all'):   
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
        p = Process(target=main3, args=(counter, r))
        workers.append(p)
        p.start()

    for worker in workers:
        worker.join()
    
def brut4(cores='all'):   
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
        p = Process(target=main4, args=(counter, r))
        workers.append(p)
        p.start()

    for worker in workers:
        worker.join()       

def brut5(cores='all'):   
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
        p = Process(target=main5, args=(counter, r))
        workers.append(p)
        p.start()

    for worker in workers:
        worker.join()       
        
def gen():
    gener = random.choices(ALPHABET, k=21)
    MINIKEY = 'S'+''.join(gener)
    return MINIKEY
    
def gen1():
    gener = random.choices(ALPHABET, k=29)
    MINIKEY = 'S'+''.join(gener)
    return MINIKEY
    
def HASH160(pubk_bytes):
    return hashlib.new('ripemd160', hashlib.sha256(pubk_bytes).digest() ).digest()
    

        
def main3(counter, r):
    st = time.time()
    screen_print_after_keys = 1000
    found = 0
    k = 1
    while True:
        
        MINIKEY = gen()
        k += 1
        digest = sha256(MINIKEY.encode() + b"?")
        if digest[0] == 0:
            pvk = sha256(MINIKEY.encode())
            with counter.get_lock():
                counter.value += 1
            addr = ice.privatekey_to_address(0, False, (int.from_bytes(pvk, "big")))
            if k % screen_print_after_keys == 0:
                ctypes.windll.kernel32.SetConsoleTitleW("Unholy Casascius Brut 22 ")
                print('Checked: {} Found: {} Keys/s: {} Addr: {} Minikey: {}'.format(counter.value, found, round(counter.value/(time.time() - st)), addr, MINIKEY), end='\r')
                if addr in add:
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
                    print('\n FOUND!!!', '\nPrivateKey= ', pvk.hex(), '\nAddress = ', addr, '\nMinikey = ', MINIKEY)
                    f=open('winner.txt','a')
                    f.write('\n FOUND!!!' + '\nPrivateKey= ' + pvk.hex() + '\nAddress =' + addr, '\nMinikey = ' + MINIKEY)
                    f.write('\n===== Made by EvgenyUnholy |  Donations 1AandaUm4J47BRuGeVz66jE24o3fymxT1Z =====')
                    f.close()
                    found += 1
                    return
                else:
                    pass
            
        else:
            pass  

def main4(counter, r):
    st = time.time()
    screen_print_after_keys = 1000
    found = 0
    k = 1
    while True:
        
        MINIKEY = gen1()
        digest = sha256(MINIKEY.encode() + b"?")
        if digest[0] == 0:
            pvk = sha256(MINIKEY.encode())
            with counter.get_lock():
                counter.value += 1
            addr = ice.privatekey_to_address(0, True, (int.from_bytes(pvk, "big")))
            KKK += 1
            Kk = k-KKK
            if k % screen_print_after_keys == 0:
                ctypes.windll.kernel32.SetConsoleTitleW("Unholy Casascius Brut 30 ")
                print('Checked: {} Found: {} Keys/s: {} Addr: {} Minikey: {}'.format(counter.value, found, round(counter.value/(time.time() - st)), addr, MINIKEY), end='\r')
                if addr in add:
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
                    print('\n FOUND!!!', '\nPrivateKey= ', pvk.hex(), '\nAddress = ', addr, '\nMinikey = ', MINIKEY)
                    f=open('winner.txt','a')
                    f.write('\n FOUND!!!' + '\nPrivateKey= ' + pvk.hex() + '\nAddress =' + addr, '\nMinikey = ' + MINIKEY)
                    f.write('\n===== Made by EvgenyUnholy |  Donations 1AandaUm4J47BRuGeVz66jE24o3fymxT1Z =====')
                    f.close()
                    found += 1
                    return
                else:
                    pass
            k += 1
        else:
            pass

def main5(counter, r):
    st = time.time()
    screen_print_after_keys = 10000
    found = 0
    k = 1
    while True:
        
        #for i in itertools.product('123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz', repeat=21):
        #for i in itertools.permutations('123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz', 21):
        for i in itertools.combinations_with_replacement('123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz', 21):
        #for i in itertools.combinations('123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz', 21):
            MINIKEY = 'S'+''.join(i)
            k += 1
            digest = sha256(MINIKEY.encode() + b"?")
            if digest[0] == 0:
                with counter.get_lock():
                    counter.value += 1
                pvk = sha256(MINIKEY.encode())
                addr = ice.privatekey_to_address(0, False, (int.from_bytes(pvk, "big")))
                if k % screen_print_after_keys == 0:
                    ctypes.windll.kernel32.SetConsoleTitleW("                                                                                                                             Unholy Casascius Brut FULL")
                    print('Checked: {} Found: {} Keys/s: {} Addr: {} Minikey: {}'.format(counter.value, found, round(counter.value/(time.time() - st)), addr, MINIKEY), end='\r')
                    if addr in add:
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
                        print('\n FOUND!!!', '\nPrivateKey= ', pvk.hex(), '\nAddress = ', addr, '\nMinikey = ', MINIKEY)
                        f=open('winner.txt','a')
                        f.write('\n FOUND!!!' + '\nPrivateKey= ' + pvk.hex() + '\nAddress =' + addr, '\nMinikey = ' + MINIKEY)
                        f.write('\n===== Made by EvgenyUnholy |  Donations 1AandaUm4J47BRuGeVz66jE24o3fymxT1Z =====')
                        f.close()
                        found += 1
                        return
                    else:
                        pass

if __name__ == '__main__':
    print('================================================= UnholyCasasciusBrut =================================================')
    symb = int(input("1 - 22 symbols, print only valid keys; (random.choices) \n2 - 30 symbols, print only valid keys; (random.choices) \n3 - 22 symbols, print TRUE keys, FULL BRUT (ITERTOOLS) \nChoose format and display print: "))
    if symb == 1:
        brut3(cores = int(input("Cores count: ")))
 
    elif symb == 2:
        brut4(cores = int(input("Cores count: ")))
  
    elif symb == 3:
        brut5(cores = 1)
            
    else:
        print("ERROR!!! Please input correct number")
        quit()
        
   