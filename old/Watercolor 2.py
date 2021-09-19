import cairo, sys, copy, math, random

float_gen = lambda a, b: random.uniform(a, b)

# Background: 5 black, 4 white, 2 Red, 2 Blue, 2 Green, 3 Mix
# Color Scheme:
# https://visme.co/blog/color-combinations/
# https://www.canva.com/learn/100-color-combinations/
# Amount of Blocks: 1, 7, 11, 14, 15
# Number of sides: 

backColors = [[0,0,0],[1,1,1],[1,0,0],[0,1,0],[0,0,1],[.5,.5,.5],[.25,.25,.25],[.75,.75,.75]]
colorWeights = [5, 4, 3, 3, 2, 1, 1, 1]
schemeNames = []
colorScheme = []
schemeWeights = [10,10,10,10,10,10,10,10,10,10,10]
numberBlocks = [1, 7, 11, 14, 15]
blockWeight = [1, 7, 1100, 1414, 1015]

f = open("scheme.txt")
lines= f.readlines()
for line in lines:
    split= line.split(',')
    schemeNames.append(split[0].strip())
    temp = []
    for i in range(1, len(split)):
        curCol = []
        curCol.append(int(split[i][0:2],16)/255)
        curCol.append(int(split[i][2:4],16)/255)
        curCol.append(int(split[i][4:6],16)/255)
        temp.append(curCol)
    colorScheme.append(temp)
#print(colorScheme)
#print(schemeNames)
#print(random.choices(schemeNames, weights=schemeWeights, k=1))

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
            midpoint = ((shape[j - 1][0] + shape[j][0])/2 + float_gen(-variance, variance), (shape[j-1][1] + shape[j][1])/2 + float_gen(-variance, variance))
            shape.insert(j, midpoint)
    return shape


def main():
    width, height = 800, 800
    bgColor = random.choices(backColors, weights=colorWeights, k=1)[0]
    print(bgColor)
    initial = 10
    deviation = 50
    
    palletName = random.choices(schemeNames, weights=schemeWeights)[0]
    palletIndex = schemeNames.index(palletName)
    colors = colorScheme[palletIndex]
    
    basedeforms = 1
    finaldeforms = 3

    minshapes = 15
    maxshapes = 20

    shapealpha = .04

    ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    cr = cairo.Context(ims)

    cr.set_source_rgb(bgColor[0], bgColor[1], bgColor[2]) # Background between 0 and 1
    cr.rectangle(0, 0, width, height)
    cr.fill()

    cr.set_line_width(1)
#    input()
    g = open('cons.txt')
    cur = int(g.readline())
    g.close()
#    cur = 5
#    for p in range(-160, 960, 60):
    for p in range(-int(height * .2), int(height * 1.2), 60):
        curColor = random.choice(colors)
        cr.set_source_rgba(curColor[0], curColor[1], curColor[2], shapealpha)

        shape = octagon(random.randint(-100, width + 100), p, random.randint(100, 250))
        baseshape = deform(shape, basedeforms, initial)

        for j in range(14):
            tempshape = copy.deepcopy(baseshape)
            layer = deform(tempshape, finaldeforms, deviation)

            for i in range(len(layer)):
                cr.line_to(layer[i][0], layer[i][1])
            cr.fill()
    
    ims.write_to_png('Examples/watercolor' + str(int(cur)) + '.png')
    cur += 1
    g = open('cons.txt' , 'w')
    g.write(str(cur))
    g.close()

from PIL import Image, ImageDraw

def imageDraw():
    images = []

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

main()
