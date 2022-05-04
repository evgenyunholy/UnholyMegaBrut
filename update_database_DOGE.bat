@echo off

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
