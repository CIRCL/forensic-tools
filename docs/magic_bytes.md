Carving for ext3/ext4 directories
=================================



# Motivation

The on Linux most common file system ext3/ext4 is very consequent in deleting files and directories.

In forensics it could be useful to carve for directories to learn about deleted file- and directory names.



# Magic Bytes

Based on the data structure of a directory we could conclude on the quoted sequence of bytes.

<pre>
????\x0c\x00\x01\x02.\x00\x00\x00??????\x02\x02..\x00\x00
</pre>


It is common that the block size is 8 sectors resulting in 4096 bytes. This leads to the
quoted configuration line, successfully tested with Foremost and Scalpel. 

<pre>
       raw      y      4096     ????\x0c\x00\x01\x02.\x00\x00\x00??????\x02\x02..\x00\x00
</pre>






