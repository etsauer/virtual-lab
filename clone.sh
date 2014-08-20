#!/bin/bash
 
. ./config/env.conf

VM=$1

# Set up logging
mkdir -p log
echo "### Clone Log for $VM ###" > $LOG

### Below is for using LVM
# size=`sudo lvs -o lv_size --unit=b --noheadings /dev/vg_vms/ubuntu-base-vm | sed 's/^ *//'`
# echo size=$size
# sudo lvcreate --size=$size --name=vms-$VM vg_vms
# sudo virt-resize --expand sda1 \
#     /dev/vg_vms/ubuntu-base-vm /dev/vg_vms/vms-$VM

### Basic qcow2 clone
echo "Cloning base image" | tee $LOG
sudo qemu-img create -f qcow2 -b $BASE_IMAGE $IMAGES_HOME/$VM.qcow2 >> $LOG

# Define VM
mkdir -p tmp
sudo virsh dumpxml base-vm > tmp/base-vm.xml
network_info=$(python ./get-ip.py --name $VM < tmp/${BASE_NAME}.xml)
IFS=',' read -ra net_array <<< "$network_info"
mac=${net_array[1]}
#mac=`egrep "^$VM"'\s' tmp/ips.txt | awk '{print $3}'`; echo "Using Mac Address: $mac" | tee $LOG
python ./modify-domain.py \
    --name $VM \
    --new-uuid \
    --device-path=$IMAGES_HOME/$VM.qcow2 \
    --mac-address $mac \
    < tmp/base-vm.xml > tmp/$VM.xml | tee $LOG
sudo virsh define tmp/$VM.xml
sudo virsh dumpxml $VM
 
#ip=`egrep "^$VM\s" tmp/ips.txt | awk '{print $2}'`; echo "Using IP Address: $ip" | tee $LOG
ip=${net_array[0]}
sed -e "s/IP_ADDRESS_GOES_HERE/$ip/g" -e "s/VM_NAME_GOES_HERE/$VM/g" < templates/hosts > tmp/hosts.$VM
sed -e "s/IP_ADDRESS_GOES_HERE/$ip/g" -e "s/VM_NAME_GOES_HERE/$VM/g" -e "s/MAC_ADDRESS_GOES_HERE/$mac/g" < templates/ifcfg-eth0 > tmp/ifcfg-eth0.$VM
sed -e "s/IP_ADDRESS_GOES_HERE/$ip/g" -e "s/VM_NAME_GOES_HERE/$VM/g" -e "s/MAC_ADDRESS_GOES_HERE/$mac/g" < templates/network > tmp/network.$VM
sed -e "s/IP_ADDRESS_GOES_HERE/$ip/g" -e "s/VM_NAME_GOES_HERE/$VM/g" < templates/configure.sh > tmp/configure.sh.$VM
chmod a+x tmp/configure.sh.$VM
sudo virt-sysprep -d $VM \
  --verbose \
  --enable udev-persistent-net,bash-history,hostname,logfiles,utmp,script \
  --hostname $VM \
  --script `pwd`/tmp/configure.sh.$VM | tee $LOG
echo "Starting $VM" | tee $LOG
sudo virsh start $VM