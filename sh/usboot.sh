#!/bin/bash
# só pra facilitar minha vida

echo "Digite o caminho para seu pendrive";
df -hT -t ext4 -t vfat

read usb_path;
echo "Você digitou $usb_path";

echo "Digite o caminho absoluto para sua iso";
read iso_path;

echo "Você digitou $iso_path";

sudo dd bs=4M if=$iso_path of=$usb_path status=progress oflag=sync;
