#!/bin/sh
# muda o endereço MAC para um outro aleatório
# é necessário rodar cmo sudo
# mais refs: https://www.ostechnix.com/change-mac-address-linux/

if [ -x "$(command -v ifconfig)" ]; then
	net_command="$(ifconfig -s | awk '{ print $1}')"
	net_opt=0
elif [ ! -x "$(command -v ip link)" ]; then
	net_command="$(ip -o link show | awk -F': ' '{print $2}')"
	net_opt=1
fi


declare -a if_opt;

cont=0;
printf "escolha uma opção:\n";

# inserir aqui o tratamento pra remover "Iface" e "lo"
for i in $net_command; do
	printf "%d - %s\n" $cont $i;
	if_opt+=($i);
	cont=$((cont+1));
done;

read opt;

printf "\"%s\" escolhido\n" ${if_opt[$opt]};

MAC="$(head /dev/urandom | tr -dc A-F0-7 | head -c 12)";
MAC=${MAC:0:2}:${MAC:2:2}:${MAC:4:2}:${MAC:6:2}:${MAC:8:2}:${MAC:10:2}
echo "novo mac: $MAC";


if_="${if_opt[$opt]}"

if [[ $net_opt -eq 0 ]]; then
	ifconfig "$if_" down;
	ifconfig "$if_" hw ether "$MAC";
	ifconfig "$if_" up;
	ifconfig "$if_" | grep HWaddr;
else
	ip link set dev "$if_" down;
	ip link set dev "$if_" address "$MAC";
	ip link set dev "$if_" up;
	ip link show "$if_";
fi

exit;
