smart_xor
=========

Perform conditional bitwise XOR operations on files.

~~~~
Usage: smart_xor.py [options] args
Perform a conditional XOR on a file.
Copyright (c) 2012 Joseph Zeranski <madsc13ntist gmail.com>

Options:
  -h, --help  show this help message and exit
  -v          More verbose output regarding XORing.
  -f OUTFILE  the filename to save the patched file to.
  -k KEY      the XOR key to use.  example: 149, 0x95
  -o OFFSET   offsets to skip regardless of byte value.
              Supports: comma seperated (no spaces). int, hex (ranges)
              example : 42,0x95,25-50,0x14-0x1A,250-0xFF
  -s          ONLY XOR offsets unless value is to be ignored. (used with '-o')
  -i IGNORE   byte values to ignore.
              Supports: comma seperated (no spaces). int, hex (ranges)
              example : 42,0x95,25-50,0x14-0x1A,250-0xFF
~~~~


Example Usage
=====

extracting a malicious executable from an xored cab file hiding in a gif.

~~~~
$ cabextract 4378156187_5.showlist.gif
4378156187_5.showlist.gif: no valid cabinets found
~~~~

the gif doesn't appear to contain a valid cabinet stream but we know (from the malware driving this infection) that the cab contains an executable called "javae.exe". We know from the stage-1 malware that it is going to xor by 0x78 and ignore null bytes (0x0) and the key (0x78) and extract a stage-2 executable from the cab. (but you could also find some of that with a quick xorsearch for the cabinet header...)

~~~~
$ xorsearch 4378156187_5.showlist.gif MSCF
Found XOR 78 position 2800: MSCFxxxx.Q.xxxxx,xxxxxxx...x.xxxxxxxFxxx.x.xx..xxx
~~~~

So we xor the gif by 0x78 (ignoring the key and null bytes).

~~~~
$ ./smart_xor.py -k 0x78 -i 0x0,0x78 4378156187_5.showlist.gif 
Using XOR key:    0x78
Ignoring values:  0x0, 0x78
~~~~

Now we have the patched (xored) gif.  We can now extract the executable from the cabinet.
~~~~
$ cabextract 4378156187_5.showlist.gif.patched 
Extracting cabinet: 4378156187_5.showlist.gif.patched
  extracting javae.exe

All done, no errors.
~~~~

Success! :)

~~~~
$ file -i javae.exe 
javae.exe: application/x-dosexec; charset=binary
~~~~
