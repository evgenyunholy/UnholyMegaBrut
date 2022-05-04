@echo off

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
