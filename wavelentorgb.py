#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: R.F. Smith <rsmith@xs4all.nl>
# Last modified: 2015-05-04 00:50:03 +0200
#
# To the extent possible under law, Roland Smith has waived all copyright and
# related or neighboring rights to wavelengthtorgb.py. This work is published
# from the Netherlands. See http://creativecommons.org/publicdomain/zero/1.0/

"""convert wavelengths to RBG."""

from __future__ import print_function, division

gamma = 0.8
maxc = 255


def wavelen2rgb(nm):  # pylint: disable=R0912
    """Convert a wavelength to an RGB tuple

    :nm: wavelength in nanometers
    :returns: an RBG tuple
    """

    def adjust(color, factor):
        if color < 0.01:
            return 0
        rv = int(round(maxc * (color * factor) ** gamma))
        if rv < 0:
            rv = 0
        elif rv > maxc:
            rv = maxc
        return rv

    # Check if a valid wavelength was given.
    if nm < 380 or nm > 780:
        raise ValueError('wavelength outside of visible range')
    # Calculate intensities in the different wavelength bands.
    red, green, blue = 0.0, 0.0, 0.0
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
    # print('DEBUG: r = {}, g = {}, b = {}'.format(red, green, blue))
    if nm < 420:
        factor = 0.3 + 0.7 * (nm - 380.0) / (420.0 - 380.0)
    elif nm < 701:
        factor = 1.0
    else:
        factor = 0.3 + 0.7 * (780.0 - nm) / (780.0 - 700.0)
    # Return the adjusted values
    return (adjust(red, factor), adjust(green, factor), adjust(blue, factor))


def main():
    """Main program.
    """
    cdict = {j: wavelen2rgb(j) for j in range(380, 781)}
    print('ctable = {', end='')
    for j in range(380, 781):
        r, g, b = cdict[j]
        print('{}: ({}, {}, {}), '.format(j, r, g, b), end='')
        k = j - 380
        if k > 0 and k % 3 == 0:
            print()
    print('}')


if __name__ == '__main__':
    main()
