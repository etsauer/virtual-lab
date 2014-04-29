#!/bin/bash

is_available() {
	VM="$1"
	IP="$2"
	if [[ $(($(grep -c "$IP" /etc/hosts) + $(grep -c "$VM" /etc/hosts))) == 0 ]]; then
		echo "true";
	else
		echo "false";
	fi
}

add() {
	VM="$1"
	IP="$2"
	if [[ $(is_available $VM $IP) == "true" ]]; then
		echo "$IP    $VM" | sudo tee -a /etc/hosts > /dev/null
		echo "true"
	else
		echo "IP: $IP is already taken"
		exit -1
	fi
}

remove() {
	VM="$1"
	IP="$2"
	sudo sed -i "/$VM/d" /etc/hosts
}

usage() {
	echo "Usage: $0 [add|remove|is_available] [ip] [vm]"
}

ACTION=$1
IP=$2
VM=$3

case $ACTION in
	add) add $VM $IP ;;
	remove) remove $VM $IP ;;
	is_available) is_available $VM $IP ;;
	*) usage ;;
esac