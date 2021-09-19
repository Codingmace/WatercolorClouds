import cairo, sys, argparse, copy, math, random

float_gen = lambda a, b: random.uniform(a, b)

# Background: 5 black, 4 white, 2 Red, 2 Blue, 2 Green, 3 Mix
# Color Scheme:
# https://visme.co/blog/color-combinations/
# https://www.canva.com/learn/100-color-combinations/
# Amount of Blocks: 
# Shapes

colors = [[0,0,0],[1,1,1],[1,0,0],[0,1,0],[0,0,1],
          [0,0,0],[1,1,1],[1,0,0],[0,1,0],[0,0,1],
          [.5,.5,.5],[.25,.25,.25],[.75,.75,.75],
          [1,1,1],[0,0,0],[1,1,1],[0,0,0],[1,1,1]]
#print(colors)
#colors = [[1, 1, 1], [0, 0, 0], [.5, 0, 0], [1, 0, 1]]
#for i in range(15):
#    colors.append((float_gen(.4, .75), float_gen(.4, .75), float_gen(.4, .75)))
"""
back = open("back.txt", 'r')
lines = back.readlines()
for line in lines:
    temp = line.split(" ")
    t = [float(temp[0]), float(temp[1]), float(temp[2])]
    colors.append(t)
#    colors.append(line.split(" "))
"""

def octagon(x_orig, y_orig, side):
    x = x_orig
    y = y_orig
    d = side / math.sqrt(2)
    oct = []

    oct.append((x, y))

    x += side
    oct.append((x, y))

    x += d
    y += d
    oct.append((x, y))

    y += side
    oct.append((x, y))

    x -= d
    y += d
    oct.append((x, y))

    x -= side
    oct.append((x, y))

    x -= d
    y -= d
    oct.append((x, y))

    y -= side
    oct.append((x, y))

    x += d
    y -= d
    oct.append((x, y))

    return oct

def deform(shape, iterations, variance):
    for i in range(iterations):
        for j in range(len(shape)-1, 0, -1):
            midpoint = ((shape[j-1][0] + shape[j][0])/2 + float_gen(-variance, variance), (shape[j-1][1] + shape[j][1])/2 + float_gen(-variance, variance))
            shape.insert(j, midpoint)
    return shape


def main():
#    parser = argparse.ArgumentParser()
#    parser.add_argument("--width", default=1000, type=int)
#    parser.add_argument("--height", default=1500, type=int)
#    parser.add_argument("-i", "--initial", default=120, type=int)
#    parser.add_argument("-d", "--deviation", default=50, type=int)
#    parser.add_argument("-bd", "--basedeforms", default=1, type=int)
#    parser.add_argument("-fd", "--finaldeforms", default=3, type=int)
#    parser.add_argument("-mins", "--minshapes", default=20, type=int)
#    parser.add_argument("-maxs", "--maxshapes", default=25, type=int)
#    parser.add_argument("-sa", "--shapealpha", default=.02, type=float)
#    args = parser.parse_args()

    width, height = 800, 800
    initial = 120
    deviation = 50
    
    basedeforms = 1
    finaldeforms = 3

    minshapes = 10
    maxshapes = 15

    shapealpha = .04

    ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    cr = cairo.Context(ims)

    cr.set_source_rgb(.01, .01, .01) # Background between 0 and 1
    cr.rectangle(0, 0, width, height)
    cr.fill()

    cr.set_line_width(1)
    cur = 4
    for p in range(-int(height*.2), int(height*1.2), 60):
        cr.set_source_rgba(random.choice(colors)[0], random.choice(colors)[1], random.choice(colors)[2], shapealpha)

        shape = octagon(random.randint(-100, width+100), p, random.randint(100, 300))
        baseshape = deform(shape, basedeforms, initial)

        for j in range(random.randint(minshapes, maxshapes)):
            tempshape = copy.deepcopy(baseshape)
            layer = deform(tempshape, finaldeforms, deviation)

            for i in range(len(layer)):
                cr.line_to(layer[i][0], layer[i][1])
            cr.fill()
    
    ims.write_to_png('Examples/watercolor' + str(int(cur)) + '.png')
    cur += 1

from PIL import Image, ImageDraw

def imageDraw():
    images = []

#    width = 200
    width = 800
    center = width // 2
    color_1 = (0, 0, 0)
#    color_2 = (255, 255, 255)
    color_2 = (20, 255, 20)
    max_radius = 100
#    max_radius = int(center * 1.5)
#    step = 8
    step = 10

    for i in range(0, max_radius, step):
        im = Image.new('RGB', (width, width), color_1)
        draw = ImageDraw.Draw(im)
        draw.ellipse((center - i, center - i, center + i, center + i), fill=color_2)
        images.append(im)

    """
    for i in range(0, max_radius, step):
        im = Image.new('RGB', (width, width), color_2)
        draw = ImageDraw.Draw(im)
        draw.ellipse((center - i, center - i, center + i, center + i), fill=color_1)
        images.append(im)
    """
    images[0].save('image_draw_4.gif',
                   save_all=True, append_images=images[1:], optimize=False, duration=40, loop=1)

#imageDraw()

#main()
