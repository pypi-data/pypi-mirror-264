from math import *
from mpmath import *


def square(sidelength):
    float(sidelength)
    return sidelength ** 2


def rectangle(length, width):
    float(length)
    float(width)
    return length * width


def circle(radius):
    float(radius)
    return pi * (radius ** 2)


def isosceles_triangle(base, height):
    float(base)
    float(height)
    return (base * height) / 2


def equilateral_triangle(sidelength):
    float(sidelength)
    return (sqrt(3) / 4) * (sidelength ** 2)


def scalene_triangle(a, b, c):
    float(a)
    float(b)
    float(c)
    s = (a + b + c) / 2
    return sqrt(s * (s - a) * (s - b) * (s - c))


def pentagon(sidelength):
    float(sidelength)
    return (1 / 4) * (sqrt(5 * (5 + 2 * sqrt(5)))) * (sidelength ** 2)


def hexagon(sidelength):
    float(sidelength)
    return ((3 * sqrt(3)) / 2) * (sidelength ** 2)


def heptagon(sidelength):
    float(sidelength)
    return (7 / 4) * (sidelength ** 2) * cot(pi / 7)


def octagon(sidelength):
    float(sidelength)
    return 2 * (1 + sqrt(2)) * (sidelength ** 2)


def nonagon(sidelength):
    float(sidelength)
    return (9 / 4) * (sidelength ** 2) * cot(pi / 9)


def decagon(sidelength):
    float(sidelength)
    return (5 / 2) * (sidelength ** 2) * sqrt(5 + 2 * sqrt(5))


def undecagon(apothem, sidelength):
    float(sidelength)
    float(apothem)
    return (11 / 4) * apothem * sidelength


def dodecagon(sidelength):
    float(sidelength)
    return 3 * (2 + sqrt(3)) * (sidelength ** 2)


def tridecagon(apothem, sidelength):
    float(sidelength)
    float(apothem)
    return (13 / 4) * apothem * sidelength


def tetradecagon(sidelength):
    float(sidelength)
    return (14 / 4) * (sidelength ** 2) * cot(pi / 14)


def pentadecagon(sidelength):
    float(sidelength)
    return (15 / 4) * (sidelength ** 2) * cot(pi / 15)


def trapezoid(b_1, b_2, height):
    float(b_1)
    float(b_2)
    float(height)
    return (1 / 2) * (b_1 + b_2) * height


def ellipse(minr, majr):
    float(minr)
    float(majr)
    return pi * majr * minr


def polyominoes(amountofsquares, squaresl):
    float(amountofsquares)
    float(squaresl)
    return amountofsquares * (squaresl ** 2)


def star(sidelength, numpoints):
    float(sidelength)
    float(numpoints)
    return ((sidelength ** 2) * numpoints) / (2 * tan(pi / numpoints))


def hemicircle(radius):
    float(radius)
    return (pi * (radius ** 2)) / 2


def squircle(a_1l, a_1w, a_2l, a_2w, a_3l, a_3w, radius):
    float(radius)
    float(a_1l)
    float(a_2l)
    float(a_3l)
    float(a_1w)
    float(a_2w)
    float(a_3w)
    return (a_1l * a_1w) + (a_2l * a_2w) + (a_3l + a_3w) + (pi * (radius ** 2))


def parallelogram(b_1, b_2, height):
    float(b_1)
    float(b_2)
    float(height)
    return (1 / 2) * (b_1 + b_2) * height


def square_with_equilateral_triangle_top(length, trianglesl):
    float(length)
    float(trianglesl)
    return (length ** 2) + ((sqrt(3) / 4) * ((sqrt(3) * (trianglesl ** 2)) / 4))


def kite(diagonal_1, diagonal_2):
    float(diagonal_1)
    float(diagonal_2)
    return (1 / 2) * (diagonal_1 * diagonal_2)


def rhombus(diagonal):
    float(diagonal)
    return (1 / 2) * (diagonal ** 2)


def cube(edgelength):
    float(edgelength)
    return edgelength ** 3


def rectangular_prism(length, width, height):
    float(length)
    float(width)
    float(height)
    return length * width * height


def sphere(radius):
    float(radius)
    return (4 / 3) * pi * (radius ** 3)


def right_cylinder(radius, height):
    float(radius)
    float(height)
    return (radius ** 2) * height


def right_circular_cone(radius, height):
    float(radius)
    float(height)
    return (1 / 3) * pi * (radius ** 2) * height


def dodecahedron(edgelength):
    float(edgelength)
    return (15 + 7 * sqrt(5)) * (edgelength ** 3) / 4 * sqrt(2)


def triangular_prism(ise, s1, s2, s3, ib, ih, esl, height):
    float(s1)
    float(s2)
    float(s3)
    float(ib)
    float(ih)
    float(esl)
    float(height)
    if ise == "i":
        return isosceles_triangle(ib, ih)*height
    elif ise == "s":
        return scalene_triangle(s1, s2, s3)*height
    elif ise == "e":
        return equilateral_triangle(esl)*height


def hemisphere(radius):
    float(radius)
    return (2 / 3) * pi * (radius ** 3)


def torus(majr, minr):
    float(majr)
    float(minr)
    return (pi * minr ** 2) * (2 * pi * majr)


def rhombicosidodecahedron(edgelength):
    float(edgelength)
    return (edgelength ** 3) / 3 * (60 + 29 * sqrt(5))


def pipe(radius, length):
    float(radius)
    float(length)
    return pi * (radius ** 2) * length


def capsule(radius, height):
    float(radius)
    float(height)
    return pi * (radius ** 2) * (4 / 3 * radius + height)


def tetrahedron(edgelength):
    float(edgelength)
    return (edgelength ** 3) / (6 * sqrt(2))


def octahedron(edgelength):
    float(edgelength)
    return ((sqrt(2)) / 3) * (edgelength ** 3)


def icosahedron(edgelength):
    float(edgelength)
    return ((5 * (3 + sqrt(5))) / 12) * (edgelength ** 3)


def triangular_pyramid(iseb, s1, s2, s3, ib, ih, esl, height):
    float(s1)
    float(s2)
    float(s3)
    float(ib)
    float(ih)
    float(esl)
    float(height)
    if iseb == "i":
        ba = isosceles_triangle(ib, ih)
        return (1 / 3) * ba * height
    elif iseb == "s":
        ba = scalene_triangle(s1, s2, s3)
        return (1 / 3) * ba * height
    elif iseb == "e":
        ba = equilateral_triangle(esl)
        return (1 / 3) * ba * height


def square_pyramid(basesl, height):
    float(basesl)
    float(height)
    return (1 / 3) * (square(basesl)) * height


def pentagon_pyramid(basesl, height):
    float(basesl)
    float(height)
    return (1 / 3) * (pentagon(basesl)) * height


def hexagon_pyramid(basesl, height):
    float(basesl)
    float(height)
    return (1 / 3) * (hexagon(basesl)) * height


def heptagon_pyramid(basesl, height):
    float(basesl)
    float(height)
    return (1 / 3) * (heptagon(basesl)) * height


def octagon_pyramid(basesl, height):
    float(basesl)
    float(height)
    return (1 / 3) * (octagon(basesl)) * height


def nonagon_pyramid(basesl, height):
    float(basesl)
    float(height)
    return (1 / 3) * (nonagon(basesl)) * height


def decagon_pyramid(basesl, height):
    float(basesl)
    float(height)
    return (1 / 3) * (decagon(basesl)) * height


def star_prism(basesl, basepoints, height):
    float(basesl)
    float(height)
    float(basepoints)
    return (star(basesl, basepoints)) * height


def steinmetz_solid(cylrad):
    float(cylrad)
    return (16 / 3) * (cylrad ** 2)

