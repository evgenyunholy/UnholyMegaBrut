@echo off

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
