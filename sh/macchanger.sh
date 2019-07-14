#!/bin/sh
# muda o endereço MAC para um outro aleatório
# é necessário rodar cmo sudo 

SHORT_IF="$(ifconfig -s | awk '{ print $1}')"

if [ ! -x "$(command -v ifconfig)" ]; then
	printf "ifconfig não instalado\n";
	exit;
fi

declare -a if_opt;

cont=0;
printf "Choose a option:\n";

# inserir aqui o tratamento pra remover "Iface" e "lo"
for i in $SHORT_IF; do
	printf "%d - %s\n" $cont $i;
	if_opt+=($i);
	cont=$((cont+1));
done;

read opt;

printf "Opção escolhida %s\n" ${if_opt[$opt]};

MAC="$(head /dev/urandom | tr -dc A-F0-7 | head -c 12)";
MAC=${MAC:0:2}:${MAC:2:2}:${MAC:4:2}:${MAC:6:2}:${MAC:8:2}:${MAC:10:2}
echo "novo mac: $MAC";


if_="${if_opt[$opt]}"
ifconfig $if_ down
ifconfig $if_ hw ether $MAC
ifconfig $if_ up
ifconfig $if | grep HWaddr

# mais refs: https://www.ostechnix.com/change-mac-address-linux/
