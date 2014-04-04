#!/bin/bash

. ./config/env.conf

VM=$1

if [[ "$(sudo virsh domstate $VM)" == "running" ]]; then
	echo "$VM is currently running. Stopping $VM..."
	sudo virsh destroy $VM
fi

sudo virsh undefine $VM
sudo rm $IMAGES_HOME/$VM.qcow2