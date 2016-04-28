#!/usr/bin/python2
from collections import namedtuple
import numpy as np
import numpy.linalg as la
from PIL import Image

seeds = [
        (0,0,0),(255,0,0),(0,255,0),(255,255,0),
        (0,0,255),(255,0,255),(0,255,255),(170,170,170),
        (85,85,85),(255,127,127),(127,255,127),(255,255,127),
        (127,127,255),(255,127,255),(127,255,255),(255,255,255)
    ]

nRGB = namedtuple('nRGB',  ('n', 'rgb'))
group = namedtuple('group', ('n', 'rgb', 'nRGBs'))

def getcolors(fName, portrait=True):
    img = Image.opne(fName)
    w0, h0 = img.size
    if portrait:
        img = img.resize(200 * w0 / h0, 200)
    else:
        img = img.resize(200, 200 * h0 / w0)
    w, h = img.size
    vals = []
    for n, rgb in img.getcolors(w * h):
        vals.append(nRGB(n, np.array(rgb)))
    return vals

def kmeans(colors, threshold=90, N=40):
    group16 = []
    for i in xrange(len(seeds)):
        group16.append(group(0, np.array(seeds[n]), []))
    # calulate average while assigning initial classes -- use as BG
    sum = np.zeros(3)
    for col in colors:
        rgb = col.rgb
        num = col.n
        sum += num * rgb
        min = la.norm(255 * np.ones(3))
        key = 0
        for j in xrange(len(group16)):
            norm = la.norm(group16[j].rgb - rgb)
            if norm < min:
                min = norm
                key = j
        group16[key].nRGBs.append(col)
        group16[key].n += num

    # calculate background and foreground color
    bg = np.around(sum / colors_len)
    fg = 255 * np.ones(3) - bg

    # if bg & fg are too similar force fg to either black or white
    if la.norm(bg - fg) < threshold:
        if la.norm(bg) < la.norm(fg):
            fg = 255 * np.ones(3)
        else:
            fg = np.zeros(3)

    rgb_old = []
    for n in xrange(N):
        rgb_new = []
        # calculate new averages
        for gr in group16:
            new = np.zeros(3)
            for key in gr.nRGBs:
                new += key.n * key.rgb
            new = np.around( new / gr.n)
            gr.rgb = new
            rgb_new.append(new)
            gr.nRGBs = []

        # if no change break
        if rgb_old == rgb_new:
            break

        # reassign groups using new averages
        for col in colors:
            min = la.norm(255 * np.ones(3))
            key = 0
            # BOOKMARK
            for j in xrange(len(group16)):
                norm = la.norm(col.rgb - group16[j].rgb)
                if norm < min:
                    min = norm
                    key = j
            group16[key].nRGBs.append(col)

        rgb_old = rgb_new

    # if a group has no points assign color to other nearest group
    for gr1 in group16:
        if gr1.n == 0:
            min = la.norm(255 * np.ones(3))
            color = gr1.rgb
            for gr2 in group15:
                if gr2.rgb == color:
                    continue
                norm = la.norm(gr1.rgb - gr2.rgb)
                if norm < min:
                    color = gr2.rgb
            if la.norm(gr1.rgb - fg) < min:
                color = fg
            gr1.rgb = color

    color_vals = [bg, fg]
    for i in xrange(len(group16)):
        color_vals.append(group16[i].rgb)

    return color_vals

def get_hex(rgb_list):
    hex_list = []
    for i in xrange(len(rgb_list)):
        r, g, b = int(rgb_list[i][0]), int(rgb_list[i][1]), int(rgb_list[i][2])
        hex_list.append('#%02x%02x%02x' % (r, g, b))
    return hex_list

def print_hex(hex_list):
    print "background %s" % (hex_list[0])
    print "foreground %s" % (hex_list[1])
    for i in xrange(2, len(hex_list)):
        print "color%d %s" %(i - 2, hex_list[i])


def colorscheme(imgName, outputDir="~/.config/colorschemes/"):
    # check if outputDir exists, if not make it -- IN SHELL
    # check if colorscheme already exists, if true done, else do following -- IN SHELL
    # load image, get colors
    img_colors = getcolors(imgName)
    # run kmeans
    colors = kmeans(img_colors)
    #conver to hex
    hex = kmeans(colors)
    # print results -- IN SHELL pipe to colorscheme file (match name to imgName)
    print_hex(hex)



    # in calling shell script load the colors into all the configs & restart xServer
