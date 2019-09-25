Carving for ext3/ext4 directories
=================================



## Motivation

The on Linux most common file system ext3/ext4 is very consequent in deleting files and directories.

In forensics it could be useful to carve for directories to learn about deleted file- and directory names.



## Magic Bytes

Based on the data structure of a directory we could conclude on the quoted sequence of bytes.

<pre>
????\x0c\x00\x01\x02.\x00\x00\x00????\x0c\x00\x02\x02..\x00\x00
</pre>


It is common that the block size is 8 sectors resulting in 4096 bytes. This leads to the
quoted configuration line, successfully tested with Foremost and Scalpel. Please review
the block size with a tool like fsstat and in case adapt the configuration.

<pre>
       raw      y      4096     ????\x0c\x00\x01\x02.\x00\x00\x00????\x0c\x00\x02\x02..\x00\x00
</pre>



## Details

How did I come to this sequence? The ext data structures are very well described in this exceillent book [1].
The 1st entry of a directory is named '.' and the 2nd entry is named '..'. All numbers are represented in
little endian.

<pre>
4 Bytes: The inode of this file unknown:    ????
2 Bytes: The beginning of the 2nd entry:    x0c x00      --> 12
1 Byte:  The size of the file name:         x01
1 Byte:  The type of the file:              x02          --> This is a driectory
1 Byte:  The file name (Size defined):      .
3 Bytes: Padding to a 4 byte boundary:      x00 x00 x00

4 Bytes: The inode of this file unknown:    ????
2 Bytes: The beginning of the 3rd entry:    x0c x00      --> 12, We ignore empty directories
1 Byte:  The size of the entry name:        x02
1 Byte:  The type of the entry:             x02          --> This is a driectory
2 Byte:  The file name (Size defined):      ..
2 Bytes: Padding to a 4 byte boundary:      x00 x00
</pre>



## References:

[1] File System Forensic Analysis; Brian Carrier; Addison Wesley; 2005; ISBN-13: 978-0321268174;



