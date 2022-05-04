@echo off

ccd %~dp0

set database_filename=Bitcoin_addresses_LATEST.txt.gz
set database_url=http://addresses.loyce.club/Bitcoin_addresses_LATEST.txt.gz

echo Downloading database from %database_url%

datafiles\utils\wget.exe -O %database_filename% %database_url%

echo Unpacking database...

datafiles\utils\gzip.exe -d -f %database_filename%



del datafiles\BF\btc.bf
python datafiles\Cbloom.py Bitcoin_addresses_LATEST.txt btc.bf
del Bitcoin_addresses_LATEST.txt
move btc.bf %~dp0\datafiles\BF

echo Done!

cd %~dp0

set database_filename=blockchair_bitcoin-cash_addresses_latest.tsv.gz
set database_url=https://gz.blockchair.com/bitcoin-cash/addresses/blockchair_bitcoin-cash_addresses_latest.tsv.gz --no-check-certificate

echo Downloading database from %database_url% 

datafiles\utils\wget.exe -O %database_filename% %database_url%

echo Unpacking database...

datafiles\utils\gzip.exe -d -f %database_filename%

del datafiles\BF\bch.bf
python datafiles\pd.py bitcoin-cash_addresses_latest.tsv bch_tmp
del bitcoin-cash_addresses_latest.tsv
python datafiles\red.py bch_tmp bch.txt
del bch_tmp
python datafiles\Cbloom.py bch.txt bch.bf
del bch.txt
move bch.bf %~dp0\datafiles\BF

echo Done!

cd %~dp0

set database_filename=blockchair_dash_addresses_latest.tsv.gz
set database_url=https://gz.blockchair.com/dash/addresses/blockchair_dash_addresses_latest.tsv.gz --no-check-certificate

echo Downloading database from %database_url% 

datafiles\utils\wget.exe -O %database_filename% %database_url%

echo Unpacking database...

datafiles\utils\gzip.exe -d -f %database_filename%

del datafiles\BF\dash.bf
python datafiles\pd.py blockchair_dash_addresses_latest.tsv dash_tmp
del blockchair_dash_addresses_latest.tsv
python datafiles\red.py dash_tmp dash.txt
del dash_tmp
python datafiles\Cbloom.py dash.txt dash.bf
del dash.txt
move dash.bf %~dp0\datafiles\BF

echo Done!

cd %~dp0

set database_filename=blockchair_dogecoin_addresses_latest.tsv.gz
set database_url=https://gz.blockchair.com/dogecoin/addresses/blockchair_dogecoin_addresses_latest.tsv.gz --no-check-certificate

echo Downloading database from %database_url% 

datafiles\utils\wget.exe -O %database_filename% %database_url%

echo Unpacking database...

datafiles\utils\gzip.exe -d -f %database_filename%

del datafiles\BF\doge.bf
python datafiles\pd.py blockchair_dogecoin_addresses_latest.tsv doge_tmp
del blockchair_dogecoin_addresses_latest.tsv
python datafiles\red.py doge_tmp doge.txt
del doge_tmp
python datafiles\Cbloom.py doge.txt doge.bf
del doge.txt
move doge.bf %~dp0\datafiles\BF

echo Done!

cd %~dp0

set database_filename=blockchair_litecoin_addresses_latest.tsv.gz
set database_url=https://gz.blockchair.com/litecoin/addresses/blockchair_litecoin_addresses_latest.tsv.gz --no-check-certificate

echo Downloading database from %database_url% 

datafiles\utils\wget.exe -O %database_filename% %database_url%

echo Unpacking database...

datafiles\utils\gzip.exe -d -f %database_filename%

del datafiles\BF\ltc.bf
python datafiles\pd.py blockchair_litecoin_addresses_latest.tsv ltc_tmp
del blockchair_litecoin_addresses_latest.tsv
python datafiles\red.py ltc_tmp ltc.txt
del ltc_tmp
python datafiles\Cbloom.py ltc.txt ltc.bf
del ltc.txt
move ltc.bf %~dp0\datafiles\BF


echo Done!



cd %~dp0

set database_filename=blockchair_zcash_addresses_latest.tsv.gz
set database_url=https://gz.blockchair.com/zcash/addresses/blockchair_zcash_addresses_latest.tsv.gz --no-check-certificate

echo Downloading database from %database_url% 

datafiles\utils\wget.exe -O %database_filename% %database_url%

echo Unpacking database...

datafiles\utils\gzip.exe -d -f %database_filename%

del datafiles\BF\zec.bf
python datafiles\pd.py blockchair_zcash_addresses_latest.tsv zec_tmp
del blockchair_zcash_addresses_latest.tsv
python datafiles\red.py zec_tmp zec.txt
del zec_tmp
python datafiles\Cbloom.py zec.txt zec.bf
del zec.txt
move zec.bf %~dp0\datafiles\BF

echo Done!


cd %~dp0

set database_filename=blockchair_ethereum_addresses_latest.tsv.gz
set database_url=https://gz.blockchair.com/ethereum/addresses/blockchair_ethereum_addresses_latest.tsv.gz --no-check-certificate

echo Downloading database from %database_url% 

datafiles\utils\wget.exe -O %database_filename% %database_url%

echo Unpacking database...

datafiles\utils\gzip.exe -d -f %database_filename%

del datafiles\BF\eth.bf
python datafiles\pd.py ethereum_addresses_latest.tsv eth_tmp
del ethereum_addresses_latest.tsv
python datafiles\red.py eth_tmp eth.txt
del eth_tmp
python datafiles\Cbloom.py eth.txt eth.bf
del eth.txt
move eth.bf %~dp0\datafiles\BF

echo Done!!!!



