#!/usr/bin/env python

__version__    = "0.0.1"
__date__       = "05.05.2012"
__author__     = "Joseph Zeranski"
__maintainer__ = "Joseph Zeranski"
__email__      = "madsc13ntist@gmail.com"
__copyright__  = "Copyright 2012, " + __author__
__license__    = "MIT"
__status__     = "Prototype"
__credits__    = [""]
__description__= "Perform a conditional XOR on a file."

####################### MIT License ####################### 
# Copyright (c) 2012 Joseph Zeranski
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
###########################################################

### Import Modules
import optparse

###  Functions
def toint(data, convert_ascii=True):
    '''
    Convert str, hex, bin or int and return its numerical value.
    '''
    t = type(data)
    #print("%s %s" % (t, data))
    if t == int:
        return data
    if t == str and data.startswith('0x'):
        return int(data, 16)
    if t == str and data.startswith('0b'):
        return int(data, 2)
    try:
        return int(ord(data))
    except ValueError:
        return ord(data)
    return data

def smart_xor(filename, patched_filename, xor_key=0x0, ignore=[], offsets=[]):
    '''
    Perform an XOR on each byte whose value is not present in the 'ignore' list.
    '''
    with open(patched_filename, 'wb') as p:
        with open(filename, 'rb') as fp:
            byte = fp.read(1)
            while byte != "":
                i = toint(byte)
                o = toint(fp.tell())
                if i not in ignore:
                    if options.only_offset:
                        if o in offsets:
                            p.write(chr(i ^ xor_key))
                    elif o not in offsets:
                        p.write(chr(i ^ xor_key))
                else:
                    p.write(byte)

                if options.verbose:
                    if i not in ignore:
                        if options.only_offset:
                            if o in offsets:
                                print("XORing offset:    %s" % hex(o))
                byte = fp.read(1)


### If the script is being executed (not imported).
if __name__ == "__main__":
    opt_parser = optparse.OptionParser()
    opt_parser.usage  = "%prog [options] args\n"

    #''' Additional formatting for Meta-data ''''''''''''''''''
    if __description__ not in ["", [""], None, False]:
        opt_parser.usage += __description__ + "\n"
    opt_parser.usage += "Copyright (c) 2012 " + __author__ + " <" + __email__ + ">"
    if __credits__ not in ["", [""], None, False]:
        opt_parser.usage += "\nThanks go out to "
        if type(__credits__) == str:
            opt_parser.usage += __credits__ + "."
        elif type(__credits__) == list:
            if len(__credits__) == 1:
                opt_parser.usage += __credits__[0] + "."
            else:
                opt_parser.usage += ', '.join(__credits__[:-1]) + " and " + __credits__[-1] + "."
    #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    opt_parser.add_option("-v",
                          dest="verbose",
                          action  = "store_true",
                          default = False,
                          help    = "More verbose output regarding XORing.")
    opt_parser.add_option("-f",
                          dest="outfile",
                          action  = "store",
                          default = False,
                          help    = "the filename to save the patched file to.")
    opt_parser.add_option("-k",
                          dest="key",
                          action  = "store",
                          default = False,
                          help    = "the XOR key to use.  example: 149, 0x95")
    opt_parser.add_option("-o",
                          dest="offset",
                          action  = "store",
                          default = False,
                          help    = "offsets to skip regardless of byte value.\t\t\t\tSupports: comma seperated (no spaces). int, hex (ranges)\t\t\t\texample : 42,0x95,25-50,0x14-0x1A,250-0xFF")
    opt_parser.add_option("-s",
                          dest="only_offset",
                          action  = "store_true",
                          default = False,
                          help    = "ONLY XOR offsets unless value is to be ignored. (used with '-o')")
    opt_parser.add_option("-i",
                          dest="ignore",
                          action  = "store",
                          default = False,
                          help    = "byte values to ignore.\t\t\t\t\tSupports: comma seperated (no spaces). int, hex (ranges)\t\t\t\texample : 42,0x95,25-50,0x14-0x1A,250-0xFF")
    (options, args) = opt_parser.parse_args()

    if not args or not options.key:
        opt_parser.print_help()
        exit(1)

    ### Parse XOR key
    if options.key:
        options.key = toint(options.key)
        if type(options.key) != int:
            print("key value invalid: %s" % options.key)
            exit(1)

    ### Parse byte values to ignore
    if options.ignore:
        ignore = []
        for x in options.ignore.split(','):
            if '-' in x:
                y = x.split('-')
                for n in range(toint(y[0]), toint(y[-1])):
                    ignore.append(n)
                continue
            if toint(x) is not None:
                ignore.append(toint(x))
            else:
                print("ignore parameter invalid: %s" % x)
                exit(1)
        options.ignore = sorted(ignore)

    ### Parse offsets to skip
    if options.offset:
        offset = []
        for x in options.offset.split(','):
            if '-' in x:
                y = x.split('-')
                for n in range(toint(y[0]), toint(y[-1])):
                    offset.append(n)
                continue
            if toint(x) is not None:
                offset.append(toint(x))
            else:
                print("offset parameter invalid: %s" % x)
                exit(1)
        options.offset = sorted(offset)

    # Do things with your options and args.
    for arg in args:
        print("Using XOR key:    %s" % hex(options.key))
        if options.ignore:
            print("Ignoring values:  %s" % ", ".join([ hex(toint(x)) for x in options.ignore ]))
        else:
            options.ignore = []
        if options.offset:
            if not options.only_offset:
                print("Ignoring offsets: %s" % ", ".join([ hex(toint(x)) for x in options.offset ]))
            else:
                print("Only XOR offsets: %s" % ", ".join([ hex(toint(x)) for x in options.offset ]))
        else:
            options.offset = []
        if options.verbose:
            print('-' * 30)
        if options.outfile:
            smart_xor(arg, options.outfile, options.key, options.ignore, options.offset)
        else:
            smart_xor(arg, arg + '.patched', options.key, options.ignore, options.offset)
