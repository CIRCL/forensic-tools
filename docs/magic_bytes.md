Carving for ext3/ext4 directories
=================================



# Motivation

The on Linux most common file system ext3/ext4 is very consequent in deleting files and directories.

In forensics it could be useful to carve for directories to learn about deleted file- and directory names.



# Mounting the partition

<pre>
       raw      y      4096     ????\x0c\x00\x01\x02.\x00\x00\x00??????\x02\x02..\x00\x00
</pre>

The output of the fdisk command show us that the partition start at sector 2048. Each sector contains 1 block of 512 bytes.





