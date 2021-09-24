import cairo, sys, copy, math, random

float_gen = lambda a, b: random.uniform(a, b)

# Background: 5 black, 4 white, 2 Red, 2 Blue, 2 Green, 3 Mix
# Color Scheme:
# https://visme.co/blog/color-combinations/
# https://www.canva.com/learn/100-color-combinations/
# Amount of Blocks: 1, 7, 11, 14, 15
# Number of sides: 8 (RN)

backColors = [[0,0,0],[1,1,1],[1,0,0],[0,1,0],[0,0,1],[.5,.5,.5],[.25,.25,.25],[.75,.75,.75]]
colorWeights = [5, 4, 3, 3, 2, 1, 1, 1]
schemeNames = []
colorScheme = []
schemeWeights = [10,10,10,10,40,15,10,10,10,40,10]
numberBlocks = [1, 7, 11, 14, 15]
blockWeight = [1, 7, 1100, 1414, 1015]

numberSides = [8, 9, 10, 11, 12, 13, 14]
SidesWeight = [1000, 200, 1300, 14, 1000, 900, 1400]


meta = open("metadata.txt", 'a')
f = open("scheme.txt")
lines= f.readlines()
for line in lines:
    split= line.split(',')
    schemeNames.append(split[0].strip())
    temp = []
    for i in range(1, len(split)):
        curCol = []
        split[i] = split[i].strip()
        curCol.append(int(split[i][0:2],16)/255)
        curCol.append(int(split[i][2:4],16)/255)
        curCol.append(int(split[i][4:6],16)/255)
        temp.append(curCol)
    colorScheme.append(temp)
#for i in range(len(colorScheme)):
#    print(schemeNames[i], colorScheme[i])
#print(colorScheme)
#input()
def polygon(sides, radius=1, rotation=0, translation=None, x=0, y=0):
    one_segment = math.pi * 2 / sides

    points = [
        (math.sin(one_segment * i + rotation) * radius,
         math.cos(one_segment * i + rotation) * radius)
        for i in range(sides)]

    if translation:
        points = [[sum(pair) for pair in zip(point, translation)]
                  for point in points]

    octo = []
    for a in points:
        octo.append([x + a[0], y + a[1]])
    return octo
#    return points

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
        for j in range(len(shape) - 1, 0, -1):
            midpoint = ((shape[j - 1][0] + shape[j][0])/2 + float_gen(-variance, variance), (shape[j-1][1] + shape[j][1])/2 + float_gen(-variance, variance))
            shape.insert(j, midpoint)
    return shape


def main():
    width, height = 2400, 2400
    bgColor = random.choices(backColors, weights=colorWeights, k=1)[0]
#    print(bgColor)
    initial = 100
    deviation = 50
    
    palletName = random.choices(schemeNames, weights=schemeWeights)[0]
    palletIndex = schemeNames.index(palletName)
    colors = colorScheme[palletIndex]
    print(palletName)

    bgColor = random.choices(colors)[0]
    bgIndex = colors.index(bgColor)
#    print(colors)
#    print(colors.index(bgColor))

    colors.remove((bgColor))
#    print(colors)
#    input()
    basedeforms = 1
    finaldeforms = 3

    shapeCount = random.choices(numberBlocks, weights=blockWeight)[0]

    shapealpha = .04

    ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    cr = cairo.Context(ims)

    cr.set_source_rgb(bgColor[0], bgColor[1], bgColor[2]) # Background between 0 and 1
    cr.rectangle(0, 0, width, height)
    cr.fill()

    cr.set_line_width(1)
    g = open('cons.txt')
    cur = int(g.readline())
    g.close()
#    for p in range(-160, 960, 60):
    for starty in range(-int(height * .2), int(height * 1.2), 60):
        curColor = random.choice(colors)
#        print(curColor)
#        input()
        cr.set_source_rgba(curColor[0], curColor[1], curColor[2], shapealpha)
        startx = random.randint(-100, width + 100)
        sideLength = random.randint(50, 250)
        shape = polygon(8, sideLength, 45, 0, startx, starty)
#        shape = octagon(startx, starty, sideLength)
        baseshape = deform(shape, basedeforms, initial)

        for j in range(shapeCount):
            tempshape = copy.deepcopy(baseshape)
            layer = deform(tempshape, finaldeforms, deviation)

            for i in range(len(layer)):
                cr.line_to(layer[i][0], layer[i][1])
            cr.fill()
    filename = 'watercolor' + str(int(cur)) + '.png'
    meta.write(str(int(cur)) + "," + palletName + "," + str(bgIndex) + "," + str(shapeCount) + "\n")
    meta.flush()
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

for i in range(5):
    main()

meta.close()
#main()
