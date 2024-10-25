#!/usr/bin/env python
# -*- coding: utf8 -*-

from gimpfu import *
from array import array
from math import *

### Internal functions

def pixel_add_err(px, err, err_weight):
        px[0] = max(min(px[0] + (err[0] / err_weight), 255), 0)
        px[1] = max(min(px[1] + (err[1] / err_weight), 255), 0)
        px[2] = max(min(px[2] + (err[2] / err_weight), 255), 0)
        return px

def pixel_err(old_px, new_px):
        return [ old_px[0] - new_px[0],
                 old_px[1] - new_px[1],
                 old_px[2] - new_px[2] ]

## 2 Gray Levels

def reduce_pixel_2(px):
        return array("B", [ 
                0xFF if px[0] > 127 else 0,
                0xFF if px[1] > 127 else 0,
                0xFF if px[2] > 127 else 0 ])

def reduce_simple_2(buffer, width, height, px_size):
        for y in range(0, height - 1):
                for x in range(0, width - 1):
                        pos = (x + width * y) * px_size
                        buffer[pos : pos + 3] = reduce_pixel_2(buffer[pos : pos + 3])
                gimp.progress_update(1.0 * y / height)


def reduce_sierra_lite_2(buffer, width, height, px_size):
        #      x  1/2
        # 1/4 1/4
        for y in range(0, height - 2):
                # first col
                pos = (y * width) * px_size
                pos_x1 = (1 + y * width) * px_size
                pos_y1 = ((y + 1) * width) * px_size
                old_px = buffer[pos : pos + 3]
                px = reduce_pixel_2(old_px)
                buffer[pos : pos + 3] = px
                err = pixel_err(old_px, px)
                buffer[pos_x1 : pos_x1 + 3] = pixel_add_err(
                        buffer[pos_x1 : pos_x1 + 3], err, 2)
                buffer[pos_y1 : pos_y1 + 3] = pixel_add_err(
                        buffer[pos_y1 : pos_y1 + 3], err, 4)

                # middle rows
                for x in range(1, width - 2):
                        pos = (x + y * width) * px_size
                        pos_x1 = (1 + x + y * width) * px_size
                        pos_y1 = (x + (y + 1) * width) * px_size
                        pos_y1_xm1 = (x - 1 + (y + 1) * width) * px_size
                        old_px = buffer[pos : pos + 3]
                        px = reduce_pixel_2(old_px)
                        buffer[pos : pos + 3] = px
                        err = pixel_err(old_px, px)
                        buffer[pos_x1 : pos_x1 + 3] = pixel_add_err(
                                buffer[pos_x1 : pos_x1 + 3], err, 2)
                        buffer[pos_y1 : pos_y1 + 3] = pixel_add_err(
                                buffer[pos_y1 : pos_y1 + 3], err, 4)
                        buffer[pos_y1_xm1 : pos_y1_xm1 + 3] = pixel_add_err(
                                buffer[pos_y1_xm1 : pos_y1_xm1 + 3], err, 4)
                
                # last col
                pos = ((y + 1) * width - 1) * px_size
                pos_y1 = ((y + 2) * width - 1) * px_size
                pos_y1_xm1 = ((y + 2) * width - 2) * px_size
                old_px = buffer[pos : pos + 3]
                px = reduce_pixel_2(old_px)
                buffer[pos : pos + 3] = px
                err = pixel_err(old_px, px)
                buffer[pos_y1 : pos_y1 + 3] = pixel_add_err(
                        buffer[pos_y1 : pos_y1 + 3], err, 4)
                buffer[pos_y1_xm1 : pos_y1_xm1 + 3] = pixel_add_err(
                        buffer[pos_y1_xm1 : pos_y1_xm1 + 3], err, 4)
                gimp.progress_update(float(y) / float(height))
        ## last row
        # first col
        pos = ((height - 1) * width) * px_size
        pos_x1 = (1 + (height - 1) * width) * px_size
        old_px = buffer[pos : pos + 3]
        px = reduce_pixel_2(old_px)
        buffer[pos : pos + 3] = px
        err = pixel_err(old_px, px)
        buffer[pos_x1 : pos_x1 + 3] = pixel_add_err(
                buffer[pos_x1 : pos_x1 + 3], err, 2)

        # middle cols
        for x in range(1, width - 2):
                pos = (x + y * width) * px_size
                pos_x1 = (1 + x + (height - 1) * width) * px_size
                old_px = buffer[pos : pos + 3]
                px = reduce_pixel_2(old_px)
                buffer[pos : pos + 3] = px
                err = pixel_err(old_px, px)
                buffer[pos_x1 : pos_x1 + 3] = pixel_add_err(
                        buffer[pos_x1 : pos_x1 + 3], err, 2)

        # last col
        pos = ((y + 1) * width - 1) * px_size
        old_px = buffer[pos : pos + 3]
        px = reduce_pixel_2(old_px)
        buffer[pos : pos + 3] = px
        gimp.progress_update(float(y) / float(height))

## 16 Gray Levels

def reduce_pixel_16(px):
        return array("B", [
                (px[0] & 0xF0) | (px[0] >> 4),
                (px[1] & 0xF0) | (px[1] >> 4),
                (px[2] & 0xF0) | (px[2] >> 4) ])

def reduce_simple_16(buffer, width, height, px_size):
        for y in range(0, height - 1):
                for x in range(0, width - 1):
                        pos = (x + width * y) * px_size
                        buffer[pos : pos + 3] = reduce_pixel_16(buffer[pos : pos + 3])
                gimp.progress_update(float(y) / float(height))

def reduce_sierra_lite_16(buffer, width, height, px_size):
        #      x  1/2
        # 1/4 1/4
        for y in range(0, height - 2):
                # first col
                pos = (y * width) * px_size
                pos_x1 = (1 + y * width) * px_size
                pos_y1 = ((y + 1) * width) * px_size
                old_px = buffer[pos : pos + 3]
                px = reduce_pixel_16(old_px)
                buffer[pos : pos + 3] = px
                err = pixel_err(old_px, px)
                buffer[pos_x1 : pos_x1 + 3] = pixel_add_err(
                        buffer[pos_x1 : pos_x1 + 3], err, 2)
                buffer[pos_y1 : pos_y1 + 3] = pixel_add_err(
                        buffer[pos_y1 : pos_y1 + 3], err, 4)

                # middle rows
                for x in range(1, width - 2):
                        pos = (x + y * width) * px_size
                        pos_x1 = (1 + x + y * width) * px_size
                        pos_y1 = (x + (y + 1) * width) * px_size
                        pos_y1_xm1 = (x - 1 + (y + 1) * width) * px_size
                        old_px = buffer[pos : pos + 3]
                        px = reduce_pixel_16(old_px)
                        buffer[pos : pos + 3] = px
                        err = pixel_err(old_px, px)
                        buffer[pos_x1 : pos_x1 + 3] = pixel_add_err(
                                buffer[pos_x1 : pos_x1 + 3], err, 2)
                        buffer[pos_y1 : pos_y1 + 3] = pixel_add_err(
                                buffer[pos_y1 : pos_y1 + 3], err, 4)
                        buffer[pos_y1_xm1 : pos_y1_xm1 + 3] = pixel_add_err(
                                buffer[pos_y1_xm1 : pos_y1_xm1 + 3], err, 4)
                
                # last col
                pos = ((y + 1) * width - 1) * px_size
                pos_y1 = ((y + 2) * width - 1) * px_size
                pos_y1_xm1 = ((y + 2) * width - 2) * px_size
                old_px = buffer[pos : pos + 3]
                px = reduce_pixel_16(old_px)
                buffer[pos : pos + 3] = px
                err = pixel_err(old_px, px)
                buffer[pos_y1 : pos_y1 + 3] = pixel_add_err(
                        buffer[pos_y1 : pos_y1 + 3], err, 4)
                buffer[pos_y1_xm1 : pos_y1_xm1 + 3] = pixel_add_err(
                        buffer[pos_y1_xm1 : pos_y1_xm1 + 3], err, 4)
                gimp.progress_update(float(y) / float(height))
        ## last row
        # first col
        pos = ((height - 1) * width) * px_size
        pos_x1 = (1 + (height - 1) * width) * px_size
        old_px = buffer[pos : pos + 3]
        px = reduce_pixel_16(old_px)
        buffer[pos : pos + 3] = px
        err = pixel_err(old_px, px)
        buffer[pos_x1 : pos_x1 + 3] = pixel_add_err(
                buffer[pos_x1 : pos_x1 + 3], err, 2)

        # middle cols
        for x in range(1, width - 2):
                pos = (x + y * width) * px_size
                pos_x1 = (1 + x + (height - 1) * width) * px_size
                old_px = buffer[pos : pos + 3]
                px = reduce_pixel_16(old_px)
                buffer[pos : pos + 3] = px
                err = pixel_err(old_px, px)
                buffer[pos_x1 : pos_x1 + 3] = pixel_add_err(
                        buffer[pos_x1 : pos_x1 + 3], err, 2)

        # last col
        pos = ((y + 1) * width - 1) * px_size
        old_px = buffer[pos : pos + 3]
        px = reduce_pixel_16(old_px)
        buffer[pos : pos + 3] = px
        gimp.progress_update(float(y) / float(height))

def reduce_color(image, drawable, color_depth, reduction_method):
        gimp.progress_init("Reducing...")

        width = drawable.width
        height = drawable.height
        px_rgn = drawable.get_pixel_rgn(0, 0, width, height)
        buffer = array("B", px_rgn[0:width, 0:height])
        px_size = len(px_rgn[0, 0])

        if color_depth == 0: # 16x16x16
                if reduction_method == 0: # simple
                        reduce_simple_16(buffer, width, height, px_size)
                elif reduction_method == 1: # fast dither
                        reduce_sierra_lite_16(buffer, width, height, px_size)
                else:
                        pass
        elif color_depth == 1: # 2x2x2
                if reduction_method == 0: # simple
                        reduce_simple_2(buffer, width, height, px_size)
                elif reduction_method == 1: # fast dither
                        reduce_sierra_lite_2(buffer, width, height, px_size)
                else:
                        pass
        else:
                pass
        px_rgn[0:width, 0:height] = buffer.tostring()
        drawable.update(0, 0, width, height)
        pdb.gimp_progress_end()

register("epi_reduce_color",
        "Reduce color depth",         
        "Reduce color depth",
        "Lars Görner",
        "Copyright (c) 2024 e-Paper Innovation Ltd",
        "2024",
        "<Image>/Filters/e-pi/ColorReduction...",
        "RGB, RGB*",
        [
                (PF_OPTION, "color_depth", "Color Depth", 0, ["16x16x16", "2x2x2"]),
                (PF_OPTION, "reduction_method", "Reduction Method", 0, ["Simple", "Fast Dithering"])
        ],
        [],
        reduce_color
)

main()