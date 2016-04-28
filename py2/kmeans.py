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

# nRGB = namedtuple('nRGB',  ('n', 'rgb'))
# group = namedtuple('group', ('n', 'rgb', 'nRGBs'))

'''
class NRGB:
    def __init__(self, n, rgb):
        self.n = n
        self.rgb = rgb
'''

class Group:
    def __init__(self, n, rgb, nrgbs):
        self.n = n
        self.rgb = rgb
        self.nrgbs = nrgbs

def getcolors(fName, portrait=True):
    img = Image.open(fName)
    w0, h0 = img.size
    if portrait:
        img = img.resize((200 * w0 / h0, 200), Image.BILINEAR)
    else:
        img = img.resize((200, 200 * h0 / w0), Image.BILINEAR)
    w, h = img.size
    vals = []
    for n, rgb in img.getcolors(w * h):
        vals.append((n, np.array(rgb)))
    # print vals
    return vals

def kmeans(cvals, threshold=90, N=40, TOL=1e-1):
    print 'running'
    group16 = []
    rgb_old = []
    for i in xrange(len(seeds)):
        group16.append(Group(0, np.array(seeds[i]), []))
        rgb_old.append(np.array(seeds[i]))
    # calulate average while assigning initial classes -- use as BG
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
    bg = np.around(sum / num_rgb)
    fg = 255 * np.ones(3) - bg

    # if bg & fg are too similar force fg to either black or white
    if la.norm(bg - fg) < threshold:
        if la.norm(bg) < la.norm(fg):
            fg = 255 * np.ones(3)
        else:
            fg = np.zeros(3)

    # rgb_old = []
    for n in xrange(N):
        rgb_new = []
        # calculate new averages
        for gr in group16:
            if gr.n == 0:
                rgb_new.append(gr.rgb)
            else:
                new = np.zeros(3)
                for key in gr.nrgbs:
                    new += key[0] * key[1]
                new = np.around( new / gr.n)
                gr.rgb = new
                rgb_new.append(new)
                gr.nrgbs = []
                gr.n = 0

        # if no change break
        max_diff = 0
        for i in xrange(len(rgb_new)):
            norm = la.norm(rgb_old[i] - rgb_new[i])
            if norm > max_diff:
                max_diff = norm
        print "%d: %f" % (n, max_diff)
        if max_diff < TOL:
            break

        # if np.array_equal(np.array(rgb_old), np.array(rgb_new)):
            # print 'break %d' % (n)
            # break

        # reassign groups using new averages
        for col in cvals:
            min = la.norm(255 * np.ones(3))
            key = 0
            for j in xrange(len(group16)):
                norm = la.norm(col[1] - group16[j].rgb)
                if norm < min:
                    min = norm
                    key = j
            group16[key].nrgbs.append(col)
            group16[key].n += col[0]

        rgb_old = rgb_new

    # if a group has no points assign color to other nearest group
    for i in xrange(len(group16)):
        if group16[i].n == 0:
            min = la.norm(group16[i].rgb - fg)
            color = fg
            for j in xrange(len(group16)):
                if i == j:
                    continue
                norm = la.norm(group16[i].rgb - group16[j].rgb)
                if norm < min:
                    min = norm
                    color = group16[j].rgb
            group16[i].rgb = color

    color_vals = [rgb_to_hex(tuple(bg)), rgb_to_hex(tuple(fg))]
    hex_vals = []
    for i in xrange(len(group16)):
        color_vals.append(rgb_to_hex(tuple(group16[i].rgb)))
    # print color_vals
    return color_vals


def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb

# deprecated
def get_hex(rgb_list):
    # print rgb_list
    hex_list = []
    for i in xrange(len(rgb_list)):
        r, g, b = int(rgb_list[i][0]), int(rgb_list[i][1]), int(rgb_list[i][2])
        # print '#%02x%02x%02x' % (r,g,b)
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
    hexcolors = kmeans(img_colors)
    # print results -- IN SHELL pipe to colorscheme file (match name to imgName)
    print_hex(hexcolors)



    # in calling shell script load the colors into all the configs & restart xServer
