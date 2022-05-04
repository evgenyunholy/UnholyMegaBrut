@echo off

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
