"""A library that provides a widget for plotting a Mandelbrot set."""

######################################################################
# Main app information.
__author__ = "Dave Pearson"
__copyright__ = "Copyright 2023-2025, Dave Pearson"
__credits__ = ["Dave Pearson"]
__maintainer__ = "Dave Pearson"
__email__ = "davep@davep.org"
__version__ = "0.8.1"
__licence__ = "MIT"

##############################################################################
# Local imports.
from .colouring import blue_brown_map, default_map, shades_of_green
from .mandelbrot import Mandelbrot

##############################################################################
# Export the imports.
__all__ = ["Mandelbrot", "default_map", "blue_brown_map", "shades_of_green"]

### __init__.py ends here
