# Ezlab UI

UI to create virtual machines and install HPE Ezmeral products.

## Usage

It supports install operations for Virtual Machines on Proxmox VE and Libvirt/KVM.
VMware used to work but their cloud-init (vm-customisations) is too complex to handle for me, so I left it there.

### Prepare Templates

Download base cloud images for template creation.

Tested images can be found at:
Rocky8:
`https://download.rockylinux.org/pub/rocky/8/images/x86_64/Rocky-8-GenericCloud.latest.x86_64.qcow2`

RHEL8 (login required):
`rhel-8.8-x86_64-kvm.qcow2`

#### Libvirt/KVM

Create a user with libvirt and sudo groups added, use this command to provide rw access for that user to the pool location (below is the default pool location, change accordingly):

```bash
sudo useradd -d /home/ezmeral -G libvirt,sudo -m -s /bin/bash -U ezmeral
sudo setfacl -Rm u:ezmeral:rwX /var/lib/libvirt/images/
echo "ezmeral ALL=(ALL:ALL) NOPASSWD:ALL" | sudo tee /etc/sudoers.d/ezmeral
```

Copy Base image file (RHEL/Rocky8 qcow2) to storage pool (default: /var/lib/libvirt/images).

`ssh-copy-id <username>@<kvm_host>` since you cannot use password auth with libvirt connection.


#### Vmware

THIS IS NOT WORKING YET/AGAIN!!!

Install required package

`virt-customize -a Rocky-8-GenericCloud.latest.x86_64.qcow2 --install open-vm-tools`
Convert qcow2 image

`qemu-img convert -f qcow2 -O vmdk -o subformat=streamOptimized Rocky-8-GenericCloud.latest.x86_64.qcow2 Rocky-8-GenericCloud.latest.x86_64.img`

Enable SSH for the ESX host
vCenter - Host - Configure - Services - SSH -> Start

Copy image to a datastore (change your host name and datastore path)
`scp Rocky-8-GenericCloud.latest.x86_64.img root@<esx.host>:/vmfs/volumes/<datastore>`

Login to the esx host (change your host name)
`ssh root@<esx.host>`

Convert image to disk
`vmkfstools -i Rocky-8-GenericCloud.latest.x86_64.img rocky-template.vmdk -W file -d thin -N`

#### Proxmox VE

Copy qcow2 base image file(s) into /var/lib/vz/template/qemu folder (create the qemu folder first)

Create a template using these commands (or using GUI, example [here](https://ostechnix.com/import-qcow2-into-proxmox/)). Adjust storage (`local-lvm`) to match your environment:

`qm create 200 --name rhel --bios ovmf --efidisk0 local-lvm:0,efitype=4m,pre-enrolled-keys=1,size=4M --cores 1 --sockets 1 --cpu host --memory 512 --scsihw virtio-scsi-single --machine q35 --agent enabled=1,freeze-fs-on-backup=0,fstrim_cloned_disks=1,type=virtio`
<!-- --net0 model=virtio,bridge=vmbr0  -->

Adjust VM ID (`200`), Image file (`rhel-8.8-cloudvm-qemu.qcow2`) and target storage (`fast1`) as needed:
`qm disk import 200 /var/lib/vz/template/qemu/rhel-8.8-cloudvm-qemu.qcow2 fast1 --format qcow2`

Attach the disk to the VM, adjust VM ID (`200`), Storage (`fast1`), Disk name (`vm-200-disk-0`) as needed:

`qm set 200 --scsi0 fast1:vm-200-disk-0,backup=0,discard=on,iothread=1,replicate=0,size=10G`

And enable boot from disk:

`qm set 200 --boot order=scsi0`

Add cloudinit drive:

`qm set 200 --ide0 local-lvm:cloudinit`

<!-- Configure required devices: -->

<!-- `qm set 200 --serial0 socket --vga serial0` -->

Finally, convert to template:

`qm template 200`

### Configure Utility

Use Settings menu to save environment details. Use placeholder text to see correct/expected format.

Leave empty if not used (ie, proxy, local repository...)

### VMs Menu

Login to hypervisor

New VM:

Select correct template, if bridge name doesn't pop up, close the dialog (`ESC`) and re-open.

Select the pre-defined configuration:

    UA Control Plane    | 2 VMs | 4 cores | 32GB Memory
    UA Workers          | 3 VMs | 32 cores | 128GB Memory
    DF Single Node      | 1 VM | 8 cores | 64GB Memory
    DF 5-Node Cluster   | 5 VMs | 8 cores | 32GB Memory
    Generic (Client)    | 1 VM | 1 cores | 2GB Memory

### Ezmeral Menu

Only Data Fabric for now. 

#### Install Ezmeral Data Fabric

Version 7.6.1 with EEP 9.2.1 will be installed on as many hosts provided. Installer will be installed on the first node and system will automatically distribute services across other nodes. Single node installation is also possible. 

Core components (fileserver, DB, Kafka/Streams, s3server, Drill, HBase, Hive) and monitoring tools (Grafana, OpenTSDB...) will be installed. Subject to change to optimize installation time & complexity.

##### Configure Step

Prepare for Data Fabric installation. Set up proxy, ulimit etc for your environment. Run in `dry mode` (in Settings) to get a bash script for preparations.

Add nodes to prepare multiple nodes.

##### Install Step

Create Data Fabric cluster on the provided nodes.

##### Cross-Cluster Step

Will be working soon!

##### Connect Step

Will download secure files from the server and install/configure the client for the cluster.

## NOTES

If API servers (ProxmoxVE and/or vSphere) are using self-signed certificates, insecure connection warnings will mess up your screen. You can avoid this using environment variable (this is not recommended due to security concerns):

`export PYTHONWARNINGS="ignore:Unverified HTTPS request"`

## TODO

[ ] Proper documentation and code clean up

[ ] Test on standalone ESX host

[X] Test airgap

