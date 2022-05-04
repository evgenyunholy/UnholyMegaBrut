@echo off

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
