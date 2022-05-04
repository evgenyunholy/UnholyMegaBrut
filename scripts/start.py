import os
import ctypes






if __name__ == '__main__':
    ctypes.windll.kernel32.SetConsoleTitleW("                                                                                                                                 UnholyMegaBrut")
    
    print(    '''
 █  █ █▀▀▄ █  █ █▀▀█ █   █  █  █▀▄▀█ █▀▀ █▀▀▀ █▀▀█  █▀▀█ █▀▀█ █  █ ▀▀█▀▀  Made by EvgenyUnholy  
 █  █ █  █ █▀▀█ █  █ █   █▄▄█  █ █ █ █▀▀ █ ▀█ █▄▄█  █▀▀▄ █▄▄▀ █  █   █    https://github.com/evgenyunholy         
 ▀▄▄▀ █  █ █  █ ▀▀▀▀ ▀▀▀ ▄▄▄█  █   █ ▀▀▀ ▀▀▀▀ █  █  █▄▄█ █ ▀▀  ▀▀▀   █    Donations: 1AandaUm4J47BRuGeVz66jE24o3fymxT1Z
    ''')
    symb = int(input("1 - BitcoinMnemoBrut \n2 - EthMnemoBrut \n3 - UnholyCasasciusBrut \n4 - Bitcoin Balance Checker \n5 - Checking Private keys BTC, ETH, DOGE, LTC & DASH \n6 - BrainwalletEthBtc FullGeN \n7 - UnholyBrainwalletBrut \n8 - PrivatKeyGen&check(ETH, BTC) \nChoose : "))
    if symb == 1:
        os.system("python BitcoinMnemoBrut.py")
        pass
    elif symb == 2:
        os.system("python EthMnemoBrut.py")
        pass   
    elif symb == 3:
        os.system("python Unholy_Casascius_Brut.py") 
        pass  
    elif symb == 6:
        os.system("python BrainwalletEth_Btc.py")  
        pass    
    elif symb == 4:
        os.system("python bitcoin-balance-checker.py")  
        pass   
    elif symb == 5:
        os.system("python cheking_private_keys.py")  
        pass  
    elif symb == 7:
        os.system("python BrainwalletBrut.py")  
    elif symb == 8:
        os.system("privGen.py")    
        pass
                             
    else:
        print("ERROR!!! Please input correct number")
        quit()
