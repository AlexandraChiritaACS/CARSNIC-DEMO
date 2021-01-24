cd ../rpitx
rtl_sdr -s 25000 -g 35 -f -$1 filename.iq
sudo ./sendiq -s 25000 -f $1 -t u8 -i filename.iq
cd ../carsnic
