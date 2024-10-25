#!/usr/bin/env python
# -*- coding: utf8 -*-

from gimpfu import *
from array import array
from math import *

def graylevel_convert(image, drawable, color_depth):
        width = drawable.width
        height = drawable.height
        px_rgn = drawable.get_pixel_rgn(0, 0, width, height)
        buffer = array("B", px_rgn[0:width, 0:height])
        px_size = len(px_rgn[0, 0])

        gimp.progress_init("Convert...")
        for i in range(0, width * height):
                pos = i * px_size
                px = buffer[pos : pos + 3]
                new_val = max(min(int(0.299 * px[0] + 0.587 * px[1] + 0.114 * px[2]), 255), 0)
                buffer[pos] = new_val
                buffer[pos + 1] = new_val
                buffer[pos + 2] = new_val
                gimp.progress_update(float(i) / float(width * height))
        px_rgn[0:width, 0:height] = buffer.tostring()
        drawable.update(0, 0, width, height)
        pdb.gimp_progress_end()


register("epi_graylevel",
        "Convert to graylevel",         
        "Convert a color image to graylevel image",
        "Lars Görner",
        "Copyright (c) 2024 e-Paper Innovation Ltd",
        "2024",
        "<Image>/Filters/e-pi/Graylevel",
        "RGB, RGB*",
        [
                (PF_OPTION, "color_depth", "Color Depth", 0, ["256"])
        ],
        [],
        graylevel_convert
)

main()