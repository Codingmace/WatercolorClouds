import math


def polygon(sides, radius=1, rotation=0, translation=None):
    one_segment = math.pi * 2 / sides

    points = [
        (math.sin(one_segment * i + rotation) * radius,
         math.cos(one_segment * i + rotation) * radius)
        for i in range(sides)]

    if translation:
        points = [[sum(pair) for pair in zip(point, translation)]
                  for point in points]

    return points

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

points1 = polygon(8, radius=10)
points2 = octagon(-7, 10,10)

"""
(0.0, 10.0)
(7.071067, 7.071067)
(10.0, 0)
(7.071067, -7.071067)
(0, -10.0)
(-7.071067, -7.071067)
(-10.0, 0)
(-7.071067, 7.071067)
"""
"""
(10, 0)
(17.071067, 7.071067)
(17.071067, 17.071067)
(10.0, 24.14213562373095)
(0.0, 24.14213562373095)
(-7.071067, 17.071067)
(-7.071067, 7.071067)
"""
for i in range(0, len(points1)):
#    print(points1[i])
    print(points2[i])
