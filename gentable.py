#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: R.F. Smith <rsmith@xs4all.nl>
# $Date$
#
# To the extent possible under law, Roland Smith has waived all copyright and
# related or neighboring rights to gentable.py. This work is published from
# the Netherlands. See http://creativecommons.org/publicdomain/zero/1.0/

'''Generates a Python table to convert wavelenths in nm to (R,G,B) tuples.'''

import base64
import zlib

def _adjust(color, factor):
    if color < 0.01:
        return 0
    max_intensity = 255
    gamma = 0.80
    rv = int(round(max_intensity*(color*factor)**gamma))
    if rv < 0:
        return 0
    if rv > max_intensity:
        return max_intensity
    return rv

def wavelen2rgb(nm):
    """Converts a wavelength between 380 and 780 nm to an RGB color tuple."""
    if nm < 380 or nm > 780:
        raise ValueError('wavelength out of range')
    red = 0.0
    green = 0.0
    blue = 0.0
    # Calculate intensities in the different wavelength bands.
    if nm < 440:
        red = -(nm - 440.0) / (440.0 - 380.0)
        blue = 1.0
    elif nm < 490:
        green = (nm - 440.0) / (490.0 - 440.0)
        blue = 1.0
    elif nm < 510:
        green = 1.0
        blue = -(nm - 510.0) / (510.0 - 490.0)
    elif nm < 580:
        red = (nm - 510.0) / (580.0 - 510.0)
        green = 1.0   
    elif nm < 645:
        red = 1.0
        green = -(nm - 645.0) / (645.0 - 580.0)
    else:
        red = 1.0
    # Let the intensity fall off near the vision limits.
    if nm < 420:
        factor = 0.3 + 0.7*(nm - 380.0) / (420.0 - 380.0)
    elif nm < 701:
        factor = 1.0
    else:
        factor = 0.3 + 0.7*(780.0 - nm) / (780.0 - 700.0)
    # Return the calculated values in an (R,G,B) tuple.
    return (_adjust(red, factor), _adjust(green, factor), 
            _adjust(blue, factor))


def txttable():
    limit = 78
    print '# Table to convert wavelengths to (R,G,B) values.'
    print '# The start of the table is at 380 nm.'
    outs = 'rgbtable = ('
    for wl in xrange(380, 780):
        clr = wavelen2rgb(wl)
        add = '{}, '.format(clr)
        if len(outs)+len(add) > limit:
            print outs
            outs = '  '+add
        else:
            outs += add
    clr = wavelen2rgb(780)
    add = '{})'.format(clr)
    if len(outs)+len(add) > limit:
        print outs
        print '  '+add
    else:
        print outs+add


def binstr():
    clrs = []
    for wl in xrange(380, 781):
        r, g, b = wavelen2rgb(wl)
        clrs.append(chr(r) + chr(g) + chr(b))
    raw = ''.join(clrs)
    return base64.b64encode(zlib.compress(raw, 9))

def split_len(seq, length):
    return [seq[i:i+length] for i in range(0, len(seq), length)]


def bintable():
    pieces = split_len(binstr(), 60)
    start = pieces.pop(0)
    start = '_ctbl = "{}"'.format(start)
    pieces = ['"{}"'.format(p) for p in pieces]
    pieces.insert(0, start)
    print 'import base64'
    print 'import zlib\n'
    print ' \\\n'.join(pieces)
    print '_ctbl = zlib.decompress(base64.b64decode(_ctbl))'
    print r"""
def rgb(nm):
    if nm < 380 or nm > 780:
        raise ValueError('wavelength out of range')
    nm = (nm - 380)*3
    r = ord(_ctbl[nm])
    g = ord(_ctbl[nm+1])
    b = ord(_ctbl[nm+2])
    return r, g, b
"""

if __name__ == '__main__':
    bintable()
