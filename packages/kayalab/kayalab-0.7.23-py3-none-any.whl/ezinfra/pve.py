from ipaddress import ip_address
import logging
from time import sleep
from urllib.parse import quote
from proxmoxer import ProxmoxAPI
from ezinfra.sshkeys import get_ssh_pubkey_from_privatekey, get_privatekey_from_string
from ezinfra.remote import ssh_run_command, wait_for_ssh
from ezlab.parameters import SWAP_DISK_SIZE, TASK_FINISHED
from ezlab.utils import ezapp

logger = logging.getLogger("ezinfra.pve")

def connect(host, username, password):
    result = None
    try:
        result = ProxmoxAPI(
            host,
            user=username,
            password=password,
            verify_ssl=False,
        )
    except Exception as error:
        return error

    return result


def vms(proxmox):
    return proxmox.cluster.resources.get(type="vm")


def storage(proxmox):
    return proxmox.cluster.resources.get(type="storage")


def networks(proxmox):
    return proxmox.cluster.resources.get(type="sdn")


def bridges(proxmox, fromtemplatename):
    if not fromtemplatename or fromtemplatename == "":
        return []

    try:
        template = [
            t for t in vms(proxmox) if t["template"] and t["name"] == fromtemplatename
        ].pop()
    except IndexError:
        return []

    return (
        proxmox.nodes(template["node"]).network.get(type="any_bridge")
        if template
        else []
    )


def clone(
    resources: tuple,
    settings: dict,
    vm_number: int,
    dryrun: bool,
):
    template, volume, bridge, eznode, hostname, first_ip = resources

    node = template["node"]
    template_type = template["type"]
    template_id = template["vmid"]

    vm_gateway = settings["gateway"]
    vm_network_bits = settings["cidr"].split("/")[1]
    privatekey: str = settings["privatekey"]

    # cloudinit requires OpenSSH format public key
    pk = get_privatekey_from_string(privatekey)
    publickey = get_ssh_pubkey_from_privatekey(pk)

    multivm = vm_number > 0 
    vm_name = hostname + str(vm_number if multivm else "")

    logger.info("[ %s ] cloning...", vm_name)
    # wait for others to request vmid
    sleep(vm_number * 4)
    nextid = ezapp.connection.cluster.nextid.get()
    logger.info("[ %s ] assigned id %s", vm_name, nextid)

    ipconfig = "ip="
    vm_ip = ""
    if first_ip == "dhcp":
        ipconfig += "dhcp"
    else:
        vm_ip = str(
            ip_address(first_ip) + vm_number - 1 if multivm else ip_address(first_ip)
        )  # adjust for single VM
        ipconfig += f"{vm_ip}/{vm_network_bits}"
        ipconfig += f",gw={vm_gateway}"

    logger.info("[ %s ] (%s) creating", vm_name, nextid)

    if dryrun:
        logger.info("Would clone VM as %s", vm_name)

    else:
        try:
            result = task_waitfor(
                ezapp.connection,
                node,
                ezapp.connection.nodes(node)(template_type)(template_id).clone.post(
                    newid=nextid,
                    name=vm_name,
                    description=eznode["name"],
                ),
            )
            if result == TASK_FINISHED:
                new_vm = ezapp.connection.nodes(node)(template_type)(nextid)
                logger.info("[ %s ] cloned", vm_name)
            else:
                logger.warning("Clone failed for %s: %s", vm_name, result)
                return False

        except Exception as error:
            logger.warning("PVE Exception for %s: %s", vm_name, error)
            return False

    if dryrun:
        logger.info(
            """Would update VM config with:
            cores=%d,
            memory=%d,
            net0=%s,
            ipconfig0=%s,
            tags=%s,
            ciuser=%s,
            cipassword=%s,
            nameserver=%s,
            searchdomain=%s,
            ciupgrade=0,
            sshkeys=%s,
            onboot=1,
            efidisk0=%s:1,efitype=4m,pre-enrolled-keys=1,size=4M",
            """,
            eznode["cores"],
            eznode["memGB"] * 1024,
            f"virtio,bridge={bridge},firewall=0",
            ipconfig,
            eznode["product"],
            settings["username"],
            "*" * 8,
            settings["nameserver"],
            settings["domain"],
            quote(publickey, safe=""),
            volume["storage"],
        )

    else:
        # configure vm
        logger.info("[ %s ] reconfigure", vm_name)
        try:
            new_vm.config.post(
                cores=eznode["cores"],
                memory=eznode["memGB"] * 1024,
                net0=f"virtio,bridge={bridge},firewall=0",
                ipconfig0=ipconfig,
                tags=eznode["product"],
                ciuser=settings["username"],
                cipassword=settings["password"],
                nameserver=settings["nameserver"],
                searchdomain=settings["domain"],
                ciupgrade=0,
                sshkeys=quote(publickey, safe=""),
                onboot=1,
                efidisk0=f"{volume['storage']}:1,efitype=4m,pre-enrolled-keys=1,size=4M",
            )
            logger.info("[ %s ] reconfigured", vm_name)
        except Exception as error:
            logger.warning("PVE Exception for %s: %s", vm_name, error)
            return False

    if dryrun:
        logger.info(
            """Would configure disks:
                OS Disk: %dG
                Swap Disk: %dG
                Data Disks (qty: %d): %s:%d,backup=0,discard=on,cache=unsafe,iothread=1,replicate=0,ssd=1
            """,
            eznode["os_disk_size"],
            SWAP_DISK_SIZE,
            eznode["no_of_disks"],
            volume["storage"],
            eznode["data_disk_size"],
        )

    else:
        logger.info("[ %s ] add disks", vm_name)
        try:
            # configure disks
            new_vm.resize.put(disk="scsi0", size=f"{eznode['os_disk_size']}G")
            # create swap disk (recommended for DF 10% of memGB) with roundup
            # Use fixed size for swap, so installer script can find it
            # swap_size = int(eznode["memGB"] // 10 + 1)
            swap_disk = f"{volume['storage']}:{SWAP_DISK_SIZE},backup=0,discard=on,cache=unsafe,iothread=1,replicate=0,ssd=1"
            new_vm.config.post(scsi1=swap_disk)

            logger.info("[ %s ] %dGB swap disk added", vm_name, SWAP_DISK_SIZE)
            # add data disks /// assume no_of_disks are 0 or 1 or 2
            data_disk = f"{volume['storage']}:{eznode['data_disk_size'] if 'data_disk_size' in eznode else 0},backup=0,discard=on,cache=unsafe,iothread=1,replicate=0,ssd=1"
            if eznode["no_of_disks"] > 0:
                new_vm.config.post(scsi2=data_disk)
            if eznode["no_of_disks"] > 1:
                new_vm.config.post(scsi2=data_disk, scsi3=data_disk)

            logger.info("[ %s ] disks attached", vm_name)
        except Exception as error:
            logger.warning("PVE Exception for %s: %s", vm_name, error)
            return False

        # start vm
        new_vm.status.start.post()

        logger.info("[ %s ] waiting startup...", vm_name)

        # # apply customisations to vm
        if not wait_for_ssh(vm_ip, settings["username"], settings["privatekey"]):
            logger.warning(f"[ %s ] SSH FAILED", vm_ip)
            return False

        # Setup swap space
        for out in ssh_run_command(
            host=vm_ip,
            username=settings["username"],
            keyfile=settings["privatekeyfile"],
            command="sudo mkswap /dev/sdb; sudo swapon /dev/sdb",
        ):
            logger.info("[ %s ] swap on: %s", vm_name, out)
            UUID = out.split(" UUID=")[1]
            print(f"SKERLER {UUID}")
            if UUID:
                for out in ssh_run_command(
                    host=vm_ip,
                    username=settings["username"],
                    keyfile=settings["privatekeyfile"],
                    command=f"echo 'UUID={UUID} none swap sw,nofail 0 0' | sudo tee -a /etc/fstab"
                ):
                    logger.debug("add swap to fstab %s", out)

        # # reboot for changes
        # if task_waitfor(
        #     proxmox=ezapp.connection,
        #     node=node,
        #     task_id=new_vm.status.reboot.post(timeout=60),
        # ) == TASK_FINISHED:
        #     sleep(30) # allow VM to reboot
        #     logger.info("[ %s ] ready for %s", vm_name, eznode["product"])
        #     return True

    # catch all
    logger.info("[ %s ] Finished", vm_name)
    return True


def task_waitfor(proxmox, node, task_id):
    task_submitted = proxmox.nodes(node).tasks(task_id).status.get()
    if task_submitted["status"] == "stopped":
        return task_submitted["exitstatus"]

    try:
        status = proxmox.nodes(node).tasks(task_id).status.get()
        while status["status"] != "stopped":
            logger.debug("PVE task status: %s is %s", status["type"], status["status"])
            sleep(3)
            status = proxmox.nodes(node).tasks(task_id).status.get()
    except Exception as error:
        logger.warning("TASK WAIT FAILED: %s", error)

    return TASK_FINISHED
