"""A library that provides a widget for plotting a Mandelbrot set."""

######################################################################
# Main app information.
__author__     = "Dave Pearson"
__copyright__  = "Copyright 2023, Dave Pearson"
__credits__    = [ "Dave Pearson" ]
__maintainer__ = "Dave Pearson"
__email__      = "davep@davep.org"
__version__    = "0.2.0"
__licence__    = "MIT"

##############################################################################
# Local imports.
from .mandelbrot import Mandelbrot, default_map, blue_brown_map

##############################################################################
# Export the imports.
__all__ = [ "Mandelbrot", "default_map", "blue_brown_map" ]

### __init__.py ends here
