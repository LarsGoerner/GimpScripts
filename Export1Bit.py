#!/usr/bin/env python
# -*- coding: utf8 -*-

from gimpfu import *
import os
from array import array

def export_1bit(image, layer, path, name):
        width = layer.width
        height = layer.height
        px_rgn = layer.get_pixel_rgn(0, 0, width, height)
        buffer = array("B", px_rgn[0:width, 0:height])
        px_size = len(px_rgn[0, 0])
        src_file = open(path + "/" + name + ".c", "w")
        px_gl = 0
        bin_val = 0

        src_file.write("#define " + name.upper() + "_WIDTH\t" + str(width) + "\n")
        src_file.write("#define " + name.upper() + "_HEIGHT\t" + str(height) + "\n")
        src_file.write("uint8_t " + name.upper() + "[" + str(width) + " * " + str(height) + " / 8] = {")

        for y in range(0, height):
                src_file.write("\n\t")
                for x in range(0, width):
                        pos = (x + y * width) * px_size
                        px = buffer[pos : pos + 3]
                        px_gl = sum(px) / 3
                        bin_val |= ( 1 if px_gl > 127 else 0 ) << (x % 8)
                        if x % 8 == 7:
                                src_file.write(str.format("0x{:02X}, ", bin_val))
                                bin_val = 0
        src_file.write("\n};\n")
        src_file.close()

register("python_fu_export_1bit",
        "Export 1-Bit image",
        "Export 1-Bit image as C-struct",
        "Lars Görner",
        "Copyright (c) 2024 Lars Görner",
        "2024",
        "<Image>/File/Export 1Bit Image...",
        "RGB RGB*",
        [
                (PF_DIRNAME, "path", "Output directory", os.getcwd()),
                (PF_STRING, "name", "Output name", "")
        ],
        [],
        export_1bit
)

main()