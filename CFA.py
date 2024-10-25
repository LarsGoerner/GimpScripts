#!/usr/bin/env python
# -*- coding: utf8 -*-

from gimpfu import *
from array import array
from math import *

def cfa_conversion(image, drawable, palette):
        gimp.progress_init("Convert...")

        # image data
        width = drawable.width
        height = drawable.height
        px_rgn = drawable.get_pixel_rgn(0, 0, width, height)
        buffer = array("B", px_rgn[0:width, 0:height])
        px_size = len(px_rgn[0, 0])

        # palette data
        pal_clr_num = pdb.gimp_palette_get_info(palette)
        pal_cols = pdb.gimp_palette_get_columns(palette)
        pal_rows = pal_clr_num / pal_cols
        pal_cls = pdb.gimp_palette_get_colors(palette)[1]

        for y in range(0, height - 1):
                for x in range(0, width - 1):
                        pal_id = (x % pal_cols) + (y % pal_rows) * pal_cols
                        pal_clr = pal_cls[pal_id]
                        pos = (x + width * y) * px_size
                        px = buffer[pos : pos + 3]

                        px[0] = int(float(px[0]) * (pal_clr[0] / 255.0))
                        px[1] = int(float(px[1]) * (pal_clr[1] / 255.0))
                        px[2] = int(float(px[2]) * (pal_clr[2] / 255.0))
                        new_px_val = max(px[0], px[1], px[2])
                        px[0] = px[1] = px[2] = new_px_val
                        buffer[pos : pos + 3] = px
                gimp.progress_update(float(y) / float(height))
        px_rgn[0:width, 0:height] = buffer.tostring()
        drawable.update(0, 0, width, height)
        pdb.gimp_progress_end()

register("epi_cfa",
        "Convert image for CFA",         
        "Convert image for CFA displays using a palette",
        "Lars Görner",
        "Copyright (c) 2024 e-Paper Innovation Ltd",
        "2024",
        "<Image>/Filters/e-pi/CFA...",
        "RGB, RGB*",
        [
                (PF_PALETTE, "palette", "CFA Palette", "D107_CFA")
        ],
        [],
        cfa_conversion
)

main()