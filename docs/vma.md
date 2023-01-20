# VMA (proxmox) forensic analysis and extraction

[VMA](https://pve.proxmox.com/wiki/VMA) is the format for images used by proxmox. If you want to extract such file for forensic analysis, you have different options.

## Python script - vma-extractor

[vma-extractor](https://github.com/jancc/vma-extractor) implements an extraction tool for the VMA backup format used by Proxmox. The tool is implemented in Python3. The tool doesn't require any additional dependencies and only extract the [format described by proxmox](https://git.proxmox.com/?p=pve-qemu.git;a=blob_plain;f=vma_spec.txt;hb=refs/heads/master). This is easier the step.

## Dockerfile using the standard vma toolset

https://github.com/AenonDynamics/vma-backup-extractor

## Manually installing vma toolset

- https://github.com/AenonDynamics/vma-backup-extractor/blob/master/Dockerfile

```Bash
sudo apt-get update && apt-get install -y gnupg wget lzop \
    libaio1 librbd1 glusterfs-common libiscsi-bin libcurl4-gnutls-dev \
    libjemalloc2 libglib2.0-0
    
echo deb "http://download.proxmox.com/debian buster pve-no-subscription" >> /etc/apt/sources.list \
    && wget http://download.proxmox.com/debian/proxmox-ve-release-6.x.gpg -O /etc/apt/trusted.gpg.d/proxmox.gpg \
    && apt-get update \
    && apt-get install -y libproxmox-backup-qemu0 \
    && apt-get download pve-qemu-kvm \
    && sudo dpkg -X ./pve-qemu-kvm_* .
    && cp usr/bin/vma .
    
sudo find -type f -name "*libnettle*"
cp /snap/core/14447/usr/lib/x86_64-linux-gnu/libnettle.so.6.2 /usr/lib
sudo ldconfig
```
