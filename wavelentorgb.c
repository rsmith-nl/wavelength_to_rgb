/* $Id: program.c,v 1.5 2001/06/21 15:42:45 rsmith Exp rsmith $
 * -*- c -*-
 * This file is part of ...
 * Copyright (C) 2001  R.F. Smith <rsmith@xs4all.nl>
 *
 * This is free software; you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by the
 * Free Software Foundation; either version 2 of the License, or (at your
 * option) any later version.
 *
 * This program is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License along
 * with this program; if not, write to the Free Software Foundation, Inc.,
 * 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
 *
 * $Log: program.c,v $
 *
 */

/** Compile a test program with 
    'gcc -Wall -DTEST -DNDEBUG -lm -o nm2rgb wavelentorgb.c'  **/

#include <math.h>
#include <stdio.h>
#include <stdlib.h>

#define TEST 1

#ifndef NULL
#define NULL (void*)0
#endif

#ifndef NDEBUG
/* __FUNCTION__ is a GCC feature. */
#undef debug
#define debug(TXT) fprintf(stderr,"%s %s(): %s\n",__FILE__,__FUNCTION__,TXT)
#else
#undef debug
#define debug(TXT) (void)0
#endif /* NDEBUG */

static const double _gamma = 0.80;
static const int max_intensity = 255;

/*+ Adjusts the color. Used to drop off the intensity near the vision
  limits.

  const double color The color to change.

  const double factor Used in adjusting the color.

  +*/
static unsigned char _adjust (const double color, const double factor)
{
  int rv;

  /*+ Return 0 for color values near to 0. +*/
  if (color < 0.01) {
    return 0;
  }

  /*+ Calculate the adjusted color value. +*/
  rv = rint(max_intensity*pow(color*factor, _gamma));
  /*+ Then clamp it to the 0 .. 255 range. +*/
  if (rv <0) rv = 0;
  if (rv > max_intensity) rv = max_intensity;

  return (unsigned char) rv;
}

int wavelen2rgb(int nm, unsigned char rgb[3]);

/*+ Converts a wavelength to an RGB color triple. This function returns 0
  on normal completion.

  int nm Wavelength. Should be between 380 and 780 nm.

  unsigned char rgb[3] The calculated color is returned in this array.

+*/
int wavelen2rgb(int nm, unsigned char rgb[3])
{
  double red = 0.0, green = 0.0, blue = 0.0, factor;

  /*+ If nm is not in the range 380 .. 780, fail and return 1. +*/
  if (nm < 380 || nm > 780)
    return 1;
  /*+ Fail with a return value of 2 if rgb is a NULL pointer. +*/
  if (rgb == NULL)
    return 2;

  /*+ Calculate intensities in the different wavelength bands. +*/
  if (nm < 440) {
    red = -(nm - 440.0) / (440.0 - 380.0);
    blue = 1.0;
  } else if (nm < 490) {
    green = (nm - 440.0) / (490.0 - 440.0);
    blue = 1.0;
  } else if (nm < 510) {
    green = 1.0;
    blue = -(nm - 510.0) / (510.0 - 490.0);
  } else if (nm < 580) {
    red = (nm - 510.0) / (580.0 - 510.0);
    green = 1.0;    
  } else if (nm < 645) {
    red = 1.0;
    green = -(nm - 645.0) / (645.0 - 580.0);
  } else {
    red = 1.0;
  } 

  /*+ Let the intensity fall off near the vision limits. +*/
  if (nm < 420) {
    factor = 0.3 + 0.7*(nm - 380.0) / (420.0 - 380.0);
  } else if (nm < 701) {
    factor = 1.0;
  } else {
    factor = 0.3 + 0.7*(780.0 - nm) / (780.0 - 700.0);
  }

  /*+ Return the calculated values in the rgb array. +*/
  rgb[0] = _adjust(red, factor);
  rgb[1] = _adjust(green, factor);
  rgb[2] = _adjust(blue, factor);

  /*+ Return a value of 0 if there were no errors. +*/
  return 0;
}


#ifdef TEST
/*+ Test program for the wavelen2rgb function. +*/
int main(int argc, char *argv[]) 
{
  int n, nm, rv;
  unsigned char rgb[3];

  if (argc < 2)
    return 0;

  for (n=1; n < argc; n++) {
    /*+ For all the command-line arguments, do: +*/
    debug("converting argument to integer");
    nm = (int) strtol(argv[n], NULL, 10);
    debug("Converting nm to rgb");
    rv = wavelen2rgb(nm, rgb); /*+ - convert them to RGB value +*/
    if (rv) {
      printf("%s: wavelenghts should be in range 380 .. 780 nm\n", argv[0]);
    } else {
      /*+ - report the values +*/
      printf("%d nm = %3u, %3u, %3u\n", nm, 
             (unsigned)rgb[0], (unsigned)rgb[1], (unsigned)rgb[2]);
    }
  }
  return 0;
}
#endif /* TEST */


/* EOF $RCSfile: program.c,v $ */
