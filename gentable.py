#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: R.F. Smith <rsmith@xs4all.nl>
# $Date: 2012-05-20 $
#
# To the extent possible under law, Roland Smith has waived all copyright and
# related or neighboring rights to NAME. This work is published from the
# Netherlands. See http://creativecommons.org/publicdomain/zero/1.0/

'''Generates a Python table to convert wavelenths in nm to (R,G,B) tuples.'''

import sys

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

def wavelen2rgb(wl):
    """Converts a wavelength between 380 and 780 nm to an RGB color tuple."""
    if wl < 380 or wl > 780:
        raise ValueError
    red = 0.0
    green = 0.0
    blue = 0.0
    # Calculate intensities in the different wavelength bands.
    if nm < 440:
        red = -(wl - 440.0) / (440.0 - 380.0)
        blue = 1.0;
    elif wl < 490:
        green = (wl - 440.0) / (490.0 - 440.0)
        blue = 1.0
    elif wl < 510:
        green = 1.0;
        blue = -(wl - 510.0) / (510.0 - 490.0)
    elif wl < 580:
        red = (wl - 510.0) / (580.0 - 510.0)
        green = 1.0;   
    elif wl < 645:
        red = 1.0;
        green = -(wl - 645.0) / (645.0 - 580.0)
    else:
        red = 1.0
    # Let the intensity fall off near the vision limits.
    if nm < 420:
        factor = 0.3 + 0.7*(wl - 380.0) / (420.0 - 380.0)
    elif nm < 701:
        factor = 1.0
    else:
        factor = 0.3 + 0.7*(780.0 - nm) / (780.0 - 700.0)
    # Return the calculated values in an (R,G,B) tuple.
    return (_adjust(red, factor), _adjust(green, factor), 
            _adjust(blue, factor))

if __name__ == '__main__':
    limit = 78
    print '# Table to convert wavelengths to (R,G,B) values.'
    print '# The start of the table is at 380 nm.'
    outs = 'rgbtable = ('
    for nm in xrange(380, 780):
        color = wavelen2rgb(nm)
        add = '{}, '.format(color)
        if len(outs)+len(add) > limit:
            print outs
            outs = '  '+add
        else:
            outs += add
    color = wavelen2rgb(780)
    add = '{})'.format(color)
    if len(outs)+len(add) > limit:
        print outs
        print '  '+add
    else:
        print outs+add
