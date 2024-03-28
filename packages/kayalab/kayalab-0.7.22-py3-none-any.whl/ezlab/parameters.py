# App parameters

TASK_FINISHED = "EZTASK_FINISHED"  # used as sentinel for queues

VMWARE = "VMware"
PVE = "Proxmox"
AWS = "AWS"
AZURE = "Azure"
KVM = "KVM"

SUPPORTED_HVES = [
    PVE,
    # VMWARE,
    KVM,
    # AWS
    # AZURE
]

UA = "EZUA"
DF = "EZDF"
DFAAS = "DFaaS"
GENERIC = "Generic"
DFCLIENT = "Client"

MAPR_CORE_VERSION = "7.6.1"
MAPR_MEP_VERSION = "9.2.1"

SSHKEYNAME = "ezlab-key"
SWAP_DISK_SIZE = 16

EZNODES = [
    {
        "name": "ua-control",
        "product": UA,
        "cores": 4,
        "memGB": 8,
        "os_disk_size": 300,
        "data_disk_size": 500,
        "no_of_disks": 1,
        "count": 2,
    },
    {
        "name": "ua-worker",
        "product": UA,
        "cores": 32,
        "memGB": 128,
        "os_disk_size": 300,
        "data_disk_size": 500,
        "no_of_disks": 2,
        "count": 3,
    },
    {
        "name": "df-singlenode",
        "product": DF,
        "cores": 8,
        "memGB": 64,
        "os_disk_size": 240,
        "data_disk_size": 200,
        "no_of_disks": 1,
        "count": 1,
    },
    {
        "name": "df-5nodes",
        "product": DF,
        "cores": 8,
        "memGB": 32,
        "os_disk_size": 240,
        "data_disk_size": 200,
        "no_of_disks": 1,
        "count": 5,
    },
    {
        "name": "dfaas-3nodes",
        "product": DFAAS,
        "cores": 16,
        "memGB": 32,
        "os_disk_size": 240,
        "data_disk_size": 200,
        "no_of_disks": 1,
        "count": 3,
    },
    {
        "name": "generic",
        "product": GENERIC,
        "cores": 1,
        "memGB": 2,
        "os_disk_size": 20,
        "no_of_disks": 0,
        "count": 1,
    },
]

SETUP_COMMANDS = {
    DFAAS: [
        # "sudo useradd -md /home/mapr -u 5000 -U -s /bin/bash mapr",
        # "echo 'mapr ALL=(ALL) NOPASSWD:ALL' | sudo tee /etc/sudoers.d/mapr; sudo chown root:root /etc/sudoers.d/mapr; sudo chmod 440 /etc/sudoers.d/mapr",
        # "echo mapr:mapr | sudo chpasswd",
    ],
    DF: [
        # "sudo chown root:root /etc/sudoers.d/mapr -- 2>/dev/null && sudo chmod 440 /etc/sudoers.d/mapr",
        "sudo sed -i 's/^SELINUX=.*/SELINUX=disabled/' /etc/selinux/config",
        "sudo sysctl vm.swappiness=1 >/dev/null",
        "echo 'vm.swappiness=1' | sudo tee /etc/sysctl.d/mapr.conf >/dev/null",
        "echo 'umask 0022' | sudo tee /etc/profile.d/mapr.sh >/dev/null",
        "echo 'LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/mapr/lib' | sudo tee -a /etc/profile.d/mapr.sh >/dev/null",
        "sudo systemctl disable --now numad",
        "sudo dnf install -y -q wget jq",
    ],
    UA: [
        "sudo dnf -q -y install nfs-utils policycoreutils-python-utils conntrack-tools jq tar >/dev/null",
        "sudo dnf --setopt=tsflags=noscripts install -y -q iscsi-initiator-utils >/dev/null",
        'echo "InitiatorName=$(/sbin/iscsi-iname)" | sudo tee -a /etc/iscsi/initiatorname.iscsi >/dev/null',
        "sudo systemctl enable --now iscsid 2>&1",
        "sudo systemctl disable --now firewalld 2>&1",
        # "sudo sed -i 's/FirewallBackend=.*/FirewallBackend=iptables/' /etc/firewalld/firewalld.conf && sudo systemctl restart firewalld",
        "sudo ethtool -K eth0 tx-checksum-ip-generic off >/dev/null",
    ],
    GENERIC: [
        "sudo dnf remove -y -q cloud-init",
        # disable subscription manager - TODO: needs testing
        "[ -f /etc/yum/pluginconf.d/product-id.conf ] && sudo sed -i 's/^enabled=1/enabled=0/' /etc/yum/pluginconf.d/product-id.conf",
        "[ -f /etc/yum/pluginconf.d/subscription-manager.conf ] && sudo sed -i 's/^enabled=1/enabled=0/' /etc/yum/pluginconf.d/subscription-manager.conf",
        "sudo sed -i 's/^[^#]*PasswordAuthentication[[:space:]]no/PasswordAuthentication yes/' /etc/ssh/sshd_config",
        # enable root login
        # "sudo sed 's/^.*\(ssh-rsa.*\).*$/\1/' /root/.ssh/authorized_keys",
        "sudo systemctl restart sshd",
        # disable ipv6 returns for getent hosts
        "sudo sed -i 's/myhostname//g' /etc/nsswitch.conf",
    ],
}

INSTALL_COMMANDS = {
    DF: [
        """set -euo pipefail
        [ -f /opt/mapr/installer/bin/mapr-installer-cli ] && echo 'Starting installation, this may take ~30 minutes...'
        echo y | sudo /opt/mapr/installer/bin/mapr-installer-cli install -nvp -t /tmp/mapr.stanza -u mapr:mapr@127.0.0.1:9443
        # "sleep 300; sudo /opt/mapr/server/configure.sh -R -keycloak
        """
    ],
    UA: [],
    DFCLIENT: [
        "sudo dnf update -y -q",
        "sudo useradd -md /home/mapr -u 5000 -U -s /bin/bash mapr",
        "echo mapr:mapr | sudo chpasswd",
        "sudo dnf install -y -q mapr-core mapr-client mapr-posix-client-basic java-11-openjdk",
    ],
}

NO_PROXY = "10.96.0.0/12,10.224.0.0/16,10.43.0.0/16,.external.hpe.local,localhost,.cluster.local,.svc,.default.svc,127.0.0.1,169.254.169.254,.{vm_domain},{vm_network},{no_proxy}"

DF_SECURE_FILES = [
    "/opt/mapr/conf/ssl_truststore",
    "/opt/mapr/conf/ssl_truststore.p12",
    "/opt/mapr/conf/ssl_truststore.pem",
    "/opt/mapr/conf/maprtrustcreds.conf",
    "/opt/mapr/conf/maprtrustcreds.jceks",
    "/opt/mapr/conf/ssl_keystore-signed.pem",
]
