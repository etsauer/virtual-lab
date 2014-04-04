#!/bin/bash

# Script to push local key to remote host

usage() {
	echo "Usage: $0 [keyfile] [remote-user@remote-host] [remote-user]"
}

ifsudo() {
	if [[ "$(echo ${SSH_URL} | grep -c 'root')" == "0" ]]; then
		echo "sudo"
	fi
}

#Set variables
KEYFILE=$1
KEY=`cat ${KEYFILE}`
SSH_URL=$2
REMOTE_USER=$3



# Make sure user has .ssh directory
commands+="$(ifsudo) mkdir -p /home/${REMOTE_USER}/.ssh
"
# Push Key
commands+="$(ifsudo) echo ${KEY} >> /home/${REMOTE_USER}/.ssh/authorized_keys
"
# Set proper permissions
commands+="$(ifsudo) chown -R ${REMOTE_USER}:${REMOTE_USER} /home/${REMOTE_USER}/.ssh
$(ifsudo) chmod 600 /home/${REMOTE_USER}/.ssh/authorized_keys"

#echo "$commands"

ssh ${SSH_URL} <<EOF
${commands}
EOF