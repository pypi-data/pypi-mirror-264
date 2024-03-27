# Geometric Calculator

## Description

This package aims to allow its users to seamlessly calculate simple properties of geometric objects such as spheres, rectangular prisms, cylinders, and cones. By using this package, an user can simply enter the basic dimensions of their object and receive the surface area or volume of the object. This package can be used so that coders do not have to clog up their code with mathematical geometry formulas.

## Instructions

### Setting Up
Ensure you already have pipenv on your machine. Type this into a cmd:
pipenv install -i https://test.pypi.org/simple/ ndnGeometryCalc == 0.0.1

### Using the Package
To import our package, simply include the following line in the program:

```
from ndnGeometryCalc import geoCalc
```

Then you can use any of the functions in our package.

```
#Parameters: radius of the sphere
#Returns: Volume and surface area of given sphere
sphere(radius)

#Example
geoCalc.sphere(5)
```

```
#Parameters: radius, height of the cylinder
#Returns: Volume and surface area of given cylinder
cylinder(radius, height)

#Example
geoCalc.cylinder(4,6)
```

```
#Parameters: length, width, height of the rectangular prism
#Returns: Volume and surface area of given rectangular prism
rectangularPrism(length, width, height)

#Example
geoCalc.rectangularPrism(6,5,7)
```

```
#Parameters: radius, height of the cone
#Returns: Volume and surface area of given cone
cone(radius, height):

#Example
geoCalc.cone(4,7)
```

[Example program](./exampleProgram.py)

## Team Members
[Noah Zhou](https://github.com/nz792)

[Daniel Pang](https://github.com/danielpang35github)

[Niket Gautam]()

## Package Page
