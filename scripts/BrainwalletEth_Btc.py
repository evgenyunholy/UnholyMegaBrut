import hashlib,multiprocessing as mp
import time as timer
import time
import hashlib
import sys
import os
import bit
from bloomfilter import BloomFilter, ScalableBloomFilter, SizeGrowthRate
import secp256k1 as ice
from pathlib import Path
import ctypes
import itertools
mys = Path(__file__).resolve()
fil = mys.parents[1] / 'found/found.txt'


myselff = Path(__file__).resolve()
ress = myselff.parents[1] / 'datafiles/BF/btc.bf'
ctypes.windll.kernel32.SetConsoleTitleW('UnholyBrainFULL')
myself = Path(__file__).resolve()
file = myself.parents[1] / 'privatkeys/privatekeys.txt'

myselfff = Path(__file__).resolve()
resss = myselfff.parents[1] / 'datafiles/BF/eth.bf'

myb = Path(__file__).resolve()
dodo = myb.parents[1] / 'datafiles/BF/doge.bf'

myl = Path(__file__).resolve()
lolo = myl.parents[1] / 'datafiles/BF/ltc.bf'

myd = Path(__file__).resolve()
dada = myd.parents[1] / 'datafiles/BF/dash.bf'

with open(resss, "rb") as fp:
    bloom_filter1 = BloomFilter.load(fp)   

with open(ress, "rb") as fp:
    bloom_filter = BloomFilter.load(fp)   

with open(dodo, "rb") as fp:
    bloom_filter2 = BloomFilter.load(fp)  

with open(lolo, "rb") as fp:
    bloom_filter3 = BloomFilter.load(fp)  
    
with open(dada, "rb") as fp:
    bloom_filter4 = BloomFilter.load(fp) 
    

    
def HASH160(pubk_bytes):
    return hashlib.new('ripemd160', hashlib.sha256(pubk_bytes).digest() ).digest()


def bruteThread(chars,symb):
    st = time.time()
    count=0
    found = 0
    start = timer.time()

    for i in itertools.product(chars, repeat=symb):
        x = ''.join(i)
        pvk = hashlib.sha256(x.encode('utf-8')).hexdigest()
        
        addr1 = ice.privatekey_to_address(0, True, (int.from_bytes(pvk.encode(), "big")))
        addr2 = ice.privatekey_to_address(0, False, (int.from_bytes(pvk.encode(), "big")))
        addr3 = ice.privatekey_to_address(1, True, (int.from_bytes(pvk.encode(), "big")))
        addr4 = ice.privatekey_to_address(2, True, (int.from_bytes(pvk.encode(), "big")))
        addr5 = ice.privatekey_to_ETH_address(int.from_bytes(pvk.encode(), "big"))
        count += 1
        #print(addr1, addr2, addr3, addr4, addr5)
        print('cnt: {} fnd: {} | {} | hex: {}'.format(count*5, found, x, pvk), end='\r')
        if addr1 in bloom_filter:
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
            g.write('===== Made by EvgenyUnholy |  Donations 1AandaUm4J47BRuGeVz66jE24o3fymxT1Z  |   https://github.com/evgenyunholy   =====\n')
            g.write("BTC p2pkh comp:         \n", addr1)
            g.write("\n"+pvk + "\n")      
            g.close()
        elif addr2 in bloom_filter:
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
            g.write('===== Made by EvgenyUnholy |  Donations 1AandaUm4J47BRuGeVz66jE24o3fymxT1Z  |   https://github.com/evgenyunholy   =====\n')
            g.write("BTC p2pkh uncomp:       \n", addr2)
            g.write("\n"+pvk + "\n")      
            g.close()
        elif addr3 in bloom_filter:
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
            g.write('===== Made by EvgenyUnholy |  Donations 1AandaUm4J47BRuGeVz66jE24o3fymxT1Z  |   https://github.com/evgenyunholy   =====\n')
            g.write("BTC p2sh:               \n", addr3)
            g.write("\n"+pvk + "\n")      
            g.close()
        elif addr4 in bloom_filter:
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
            g.write('===== Made by EvgenyUnholy |  Donations 1AandaUm4J47BRuGeVz66jE24o3fymxT1Z  |   https://github.com/evgenyunholy   =====\n')
            g.write("BTC bech32:             \n", addr4)
            g.write("\n"+pvk + "\n")      
            g.close()
        elif addr5 in bloom_filter1:
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
            g.write('===== Made by EvgenyUnholy |  Donations 1AandaUm4J47BRuGeVz66jE24o3fymxT1Z  |   https://github.com/evgenyunholy   =====\n')
            g.write("ETH:                    \n", addr5)
            g.write("\n"+pvk + "\n")      
            g.close()
            found += 1
        




    
if __name__ == '__main__':
    print('================================================= BrainwalletEthBtc ===================================================')
    symb = int(input("Enter count symbols:  "))
    chars = "1234567890ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    bruteThread(chars,symb)
