#!/usr/bin/python2
from collections import namedtuple
import sys
import numpy as np
import numpy.linalg as la
from PIL import Image

seeds = [
        (0,0,0),(255,0,0),(0,255,0),(255,255,0),
        (0,0,255),(255,0,255),(0,255,255),(170,170,170),
        (85,85,85),(255,127,127),(127,255,127),(255,255,127),
        (127,127,255),(255,127,255),(127,255,255),(255,255,255)
    ]

REDUCED = 200


class Group:
    def __init__(self, n, rgb, nrgbs):
        self.n = n
        self.rgb = rgb
        self.nrgbs = nrgbs


def getcolors(fName, portrait=True):
    img = Image.open(fName)
    w0, h0 = img.size
    if portrait:
        img = img.resize((REDUCED * w0 / h0, REDUCED), Image.BILINEAR)
    else:
        img = img.resize((REDUCED, REDUCED * h0 / w0), Image.BILINEAR)
    w, h = img.size
    vals = []
    for n, rgb in img.getcolors(w * h):
        vals.append((n, np.array(rgb[0:3])))
    # print vals
    return vals


def kmeans(cvals, top=4, N=50, threshold=90, TOL=1):
    group16 = []
    rgb_old = []
    for i in xrange(len(seeds)):
        group16.append(Group(0, np.array(seeds[i]), []))
        rgb_old.append(np.array(seeds[i]))
    # calulate average while assigning initial classes -- use as BG
    len_g = len(group16)
    sum = np.zeros(3)
    num_rgb = 0
    for col in cvals:
        num = col[0]
        rgb = col[1]
        num_rgb += num
        sum += num * rgb
        min = la.norm(255 * np.ones(3))
        key = 0
        for j in xrange(len(group16)):
            norm = la.norm(group16[j].rgb - rgb)
            if norm < min:
                min = norm
                key = j
        group16[key].nrgbs.append(col)
        group16[key].n += num

    # calculate background and foreground color
    fg = np.around(sum / num_rgb)
    bg_temp = 255 * np.ones(3) - fg

    # if bg & fg are too similar force fg to either black or white
    if la.norm(bg_temp - fg) < threshold:
        if la.norm(bg_temp) < la.norm(fg):
            bg_temp = np.zeros(3)
        else:
            bg_temp = 255 * np.ones(3)

    # rgb_old = []
    for n in xrange(N):
        rgb_new = []
        # calculate new averages
        for i in xrange(len_g):
            if group16[i].n == 0:
                rgb_new.append(group16[i].rgb)
            else:
                new = np.zeros(3)
                for key in group16[i].nrgbs:
                    new += key[0] * key[1]
                new = np.around( new / group16[i].n)
                group16[i].rgb = new
                rgb_new.append(new)
                group16[i].nrgbs = []

        # if no change break
        max_diff = 0
        for i in xrange(len(rgb_new)):
            norm = la.norm(rgb_old[i] - rgb_new[i])
            if norm > max_diff:
                max_diff = norm
        # print "%d: %f" % (n, max_diff)
        if max_diff < TOL:
            break

        for i in xrange(len_g):
            group16[i].n = 0

        # reassign groups using new averages
        for col in cvals:
            min = la.norm(255 * np.ones(3))
            key = 0
            for j in xrange(len_g):
                norm = la.norm(col[1] - group16[j].rgb)
                if norm < min:
                    min = norm
                    key = j
            group16[key].nrgbs.append(col)
            group16[key].n += col[0]

        rgb_old = rgb_new

    # if a group has no points assign color to other nearest group
    # else
    # assign bg color to average of bg_temp & bg_temp's kmean
    bg_min = la.norm(255 * np.ones(3))
    bg_key = 0
    for i in xrange(len_g):
        if group16[i].n == 0:
            min = la.norm(group16[i].rgb - fg)
            color = fg
            for j in xrange(len_g):
                if group16[j].n == 0 or i == j:
                    continue
                norm = la.norm(group16[i].rgb - group16[j].rgb)
                if norm < min:
                    min = norm
                    color = group16[j].rgb
            group16[i].rgb = color
        else:
            norm = la.norm(group16[i].rgb - bg_temp)
            if norm < bg_min:
                bg_min = norm
                bg_key = i
    bg = np.around( 0.618 * bg_temp + 0.382 * group16[bg_key].rgb)

    color_vals = [rgb_to_hex(tuple(bg)), rgb_to_hex(tuple(fg))]
    hex_vals = []
    for i in xrange(len_g):
        color_vals.append(rgb_to_hex(tuple(group16[i].rgb)))
    for t in xrange(top):
        max = 0
        key = 0
        for i in xrange(len(group16)):
            if group16[i].n > max:
                max = group16[i].n
                key = i
        max_rgb = group16.pop(key).rgb
        opp_rgb = 255 * np.ones(3) - max_rgb
        color_vals.append(rgb_to_hex(tuple(max_rgb)))
        color_vals.append(rgb_to_hex(tuple(opp_rgb)))

    return color_vals


def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb


def print_hex(hex_list):
    print "background %s" % (hex_list[0])
    print "foreground %s" % (hex_list[1])
    for i in xrange(2, 18):
        print "color%d %s" % (i - 2, hex_list[i])
    for i in xrange(18, len(hex_list)):
        if i % 2 == 0:
            print "top%d %s" % ((i - 18) / 2, hex_list[i])
        else:
            print "opp%d %s" % ((i - 19) / 2, hex_list[i])


def colorscheme(imgName):
    img_colors = getcolors(imgName)
    hexcolors = kmeans(img_colors)
    print_hex(hexcolors)


if __name__=="__main__":
    colorscheme(sys.argv[1])
