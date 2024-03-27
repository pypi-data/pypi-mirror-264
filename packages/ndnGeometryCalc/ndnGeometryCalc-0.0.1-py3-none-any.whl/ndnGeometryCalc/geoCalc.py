import math

def sphere(radius):
    volume = 4 * math.pi * (radius**3) / 3
    surfaceArea = 4 * math.pi * (radius**2)
    return volume, surfaceArea

def cylinder(radius, height):
    volume = math.pi * (radius**2) * height
    surfaceArea = (2 * math.pi * radius) * (height + radius)
    return volume, surfaceArea

def rectangularPrism(length, width, height):
    volume = length * width * height
    surfaceArea = 2 * ((length*width) + (length*height) + (width*height))
    return volume, surfaceArea

def cone(radius, height):
    volume = math.pi * (radius**2) * height / 3
    surfaceArea = math.pi * radius * (radius + math.sqrt((height**2)+(radius**2)))
    return volume, surfaceArea

