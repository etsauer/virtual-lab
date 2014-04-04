#Setup Instructions#

Things to note:
- uses simple NAT networking for compatibility with wifi interfaces
- recommend using qcow2 images for quick creation and cloning


##Install KVM##
```bash
$ yum install @virtualization python-lxml
```

##Create Base Image##
Use the virt-manager to create a base install from an ISO, using all default options except:
- 8 gb disk, use virtio type
- Hypervisor/Virt Type: kvm
- check box to customize before launch
- NIC -> Device Model: virtio

Once installed and booted, log in as root and do the following:
- Register with subscription-manager. (Verify with a 'yum repolist')
- Create generic user with sudo access, i.e.:

```bash
$ useradd -d /home/vm-user vm-user
$ sed '/^root.*/a some-user ALL=(ALL)       NOPASSWD: ALL' /etc/sudoers
```
Push Public Key to that User

##Run Script##
```bash
### DO Not Run As root ###
$ git clone git@github.com:etsauer/virtual-lab.git
$ 
```