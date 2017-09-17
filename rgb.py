# This code has been automatically generated by the gentable.py script.
# You can find this script at https://github.com/rsmith-nl/wavelength_to_rgb
# The algorithm is based on Dan Bruton's work in
# http://www.physics.sfasu.edu/astro/color/spectra.html

import base64
import zlib

_ctbl = b'eNrV0ltr0AUAxuHn1rqoiAqSiA6EEJ3ogBUJeeFFRUdJOjOyWau1bLZpGztnM1oyy' \
        b'2yYmcmMETPNlixNVpmssobKMJuYDVnNGksz0zTe5C9BXyF4v8Dz4y1RMlPpLGVlKs' \
        b'pVVqh+Vu0cDVVa5mqdp61Ge63FdTrqLWuwolFno64m3U3WNutp1ttsY7O+Jpub9Df' \
        b'a2migwY56O+sM1dpTY3iekblGq4zNcWC2QxWOlDtWJqVSIg/JfTJd7pRbZZpMlZtk' \
        b'slwtl8skuUjOk3PkDDlFnNipcWZMjAtjUlwR18aNcXNMi9virpgRD0ZJlMZTMTuqo' \
        b'ibqoyUWxCuxKJbEm/F2dEZXrI4PYn1siL7YHP3xTWyLwfg+9sRwjMT+GI/f4884Fj' \
        b'mxP2S/7JVB+Vr6pEe65C1ZJC9KjTxduKcX1smF74TMhDgtzopz4/y4uGBdFlfFdXF' \
        b'DTImpBe6WuD3ujnvj/ni4ID4WTxTKZ6IyqgtoXTTGC9EaL8fCgvt6dPwrXhmrCnR3' \
        b'rIl18VH0xicF/fPYEl/G1hiI7UWA72KoaPBj7Iufigxj8VtR4nAcjeMnYxyXo3JYD' \
        b'sq4/CqjMiLD8oPsll1Fp+0yUNTqly/kU9kkG2S9fChrpLtIuErekeWyVN6Q16Rd2m' \
        b'SBzJcmqSvqVkulVMiTMkselUfkAZkh98gd/znZFLlerpEr5VK5RC6QiXK2nC4TTv7' \
        b'sf7C/OcZfHOEwhzjIAcYZ4xdG+ZkR9jHMXvawmyF2sZNBdrCNAb5lK1/RzxY28xl9' \
        b'bGIjH9PLenpYx1rep5v36OJdOlnJCpazjKV0sITFvEo7C2njJVqZTwtNNFBHLc9Tz' \
        b'XNUMpsKyinjcUqZSQn/AJ7p9HY='
_ctbl = zlib.decompress(base64.b64decode(_ctbl))


def rgb(nm):
    """
    Converts a wavelength between 380 and 780 nm to an RGB color tuple.

    Argument:
        nm: Wavelength in nanometers.

    Returns:
        a 3-tuple (red, green, blue) of integers in the range 0-255.
    """
    nm = int(round(nm))
    if nm < 380 or nm > 780:
        raise ValueError('wavelength out of range')
    nm = (nm - 380)*3
    r = _ctbl[nm]
    g = _ctbl[nm+1]
    b = _ctbl[nm+2]
    return r, g, b
