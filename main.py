from PIL import Image, ImageColor
import math

resolution = 1920
quality = 50

# generic class for Complex numbers, made on the fly
class Complex:
    def __init__(self, real, imaginary):
        self.real = real
        self.imaginary = imaginary
    
    def __add__(self, other):
        return Complex(self.real + other.real, self.imaginary + other.imaginary)
    
    def __mul__(self, other):
        return Complex(self.real * other.real - self.imaginary * other.imaginary, self.real * other.imaginary + self.imaginary * other.real)
    
    def __abs__(self):
        return math.sqrt(self.real**2 + self.imaginary**2)

# I heard somewhere the mandelbrot set is within the radius of two (on the complex plane)
radius = 2
# step to advance complex number to draw on the image by pixel
step = radius / float(resolution)
# iteration to check if complex position > 2
iteration = quality

# set up variables
coord = Complex(-radius, -radius)
im = Image.new('RGB', (resolution, resolution))

# until top right corner, repeat:
while coord.real <= 2:
    # for each column from left, repeat from bottom to top
    while coord.imaginary <= 2:
        # copy complex into new var
        value = Complex(coord.real, coord.imaginary)
        iterated = 0
        # start iterating until max iteration reached or |value| > 2 (which apparently means is not in the mandelbrot set)
        # i really should research how the set is made before even doing this smh
        for i in range(iteration):
            value = value*value + coord
            iterated += 1
            if abs(value) > 2:
                break
        
        # put the pixel on the image. Recall that the coordinates are [-2, 2] but the image is [0, resolution] so add the radius then multiply by resolution/4
        # color the pixel according to the number of iterations it took. closer to black = less iteration = reached abs > 2 faster = not bounded at all
        if iterated < iteration - 1:
            im.putpixel((int((coord.real + radius) * resolution/4), int((coord.imaginary + radius) * resolution/4)), (0, 0, 0))
        else:
            color_measure = (256**3)/(math.sqrt(8)) * abs(value)
            r = int(math.floor(color_measure / (256*2)))
            g = int(math.floor((color_measure - r*256*2) / 256))
            b = int(color_measure - r*256*2 - g*256)

            im.putpixel((int((coord.real + radius) * resolution/4), int((coord.imaginary + radius) * resolution/4)), (r,g,b))
        coord = Complex(coord.real, coord.imaginary + step)
    coord = Complex(coord.real + step, -radius)

im.show()