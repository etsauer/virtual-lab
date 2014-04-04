#!/bin/bash
# Run in the host, with the cwd being the root of the guest
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

set -x
cp $DIR/network.VM_NAME_GOES_HERE etc/sysconfig/network
cp $DIR/ifcfg-eth0.VM_NAME_GOES_HERE etc/sysconfig/network-scripts/ifcfg-eth0
cp $DIR/hosts.VM_NAME_GOES_HERE etc/hosts
cp $DIR/files.VM_NAME_GOES_HERE/* tmp/