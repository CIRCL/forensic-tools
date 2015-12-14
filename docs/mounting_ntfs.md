How to mount a NTFS partition for forensic investigations under Linux.
======================================================================



# Partition table

Read the partition table to identify the offset, where the partition you like to mount starts:

<pre>
$ fdisk -l imagefile.dd

Units = sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes

      Device Boot      Start         End      Blocks   Id  System
imagefile.dd            2048  3907029167  1953513560    7  HPFS/NTFS/exFAT
</pre>

The output of the fdisk command show us that the partition start at sector 2048. Each sector contains 1 block of 512 bytes.



# Mounting the partition

No we know the offset and mount the partition. The syntax is: sudo mount -o options <imagefile> <mountpoint>. You need to have root rights to mount, so you need sudo.

The image should be mounted for forensic investigations. There are some useful options which are explained below. The command to mound should look like:

<pre>
$ sudo mount -o ro,loop,noexec,offset=$((512*2048)),show_sys_files,streams_interface=windows imagefile.dd /mnt/
</pre>



## Explanation of the options

ro
	Open the image in read only mode to prevent modification of the evidence.

loop
	Mount image as loopback device.

noexec
	Prevent execution of binaries from the image to prevent infection of the forensic workstation.

offset
	Offset where the partition starts, in bytes. Easy to calculate for the shell. Just use the fdisk output.

show_sys_files
	Provides access to file system meta data. New files which are not accessible without this options are for example:
<pre>
	- $AttrDef
	- $Boot
	- $BadClus
	- $Extend
	- $LogFile
	- $UpCase
	- $MFTMirr
	- $Secure
	- $Bitmap
	- $Volume
</pre>

streams_interface=windows
	Privides access to NTFS named data streams. Provides information which was not accessible before like:
<pre>
	$ cat /Users/<username>/Downloads/Dropbox.exe:Zone.Identifier
	[ZoneTransfer]
	ZoneId=3
</pre>


