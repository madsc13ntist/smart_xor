smart_xor
=========

Perform conditional bitwise XOR operations on files.

Example Usage
=====

extracting a malicious executable from an xored cab file hiding in a gif.

~~~~$ cabextract 4378156187_5.showlist.gif
4378156187_5.showlist.gif: no valid cabinets found
~~~~

the gif doesn't appear to contain a valid cabinet stream but we know (from the malware driving this infection) that the cab contains an executable called "javae.exe". We know from the stage-1 malware that it is going to xor by 0x78 and ignore null bytes (0x0) and the key (0x78).

~~~~$ xorsearch 4378156187_5.showlist.gif javae
Found XOR 78 position 283C: javae.e
~~~~

(but you could find some of that with xorsearch.)

So we xor the gif by 0x78, ignoring the key and null bytes.

~~~~$ ./smart_xor.py -k 0x78 -i 0x0,0x78 4378156187_5.showlist.gif 
Using XOR key:    0x78
Ignoring values:  0x0, 0x78
~~~~

so now we have the patched (xored) gif.  so we extract the executable from the cabinet.
~~~~$ cabextract 4378156187_5.showlist.gif.patched 
Extracting cabinet: 4378156187_5.showlist.gif.patched
  extracting javae.exe

All done, no errors.
~~~~

Success. :)

~~~~$ file -i javae.exe 
javae.exe: application/x-dosexec; charset=binary
~~~~
