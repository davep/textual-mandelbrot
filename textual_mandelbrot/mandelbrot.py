"""Provides a Textual widget for plotting a Mandelbrot set."""

##############################################################################
# Python imports.
from decimal import Decimal
from typing  import Iterator

##############################################################################
# Textual imports.
from textual.color    import Color
from textual.reactive import var

##############################################################################
# Textual-canvas imports.
from textual_canvas import Canvas

##############################################################################
def colour_map( value: int, max_iteration: int ) -> Color:
    """Calculate a colour for an escape value.

    Args:
        value: An escape value from a Mandelbrot set.

    Returns:
        The colour to plot the point with.
    """
    return Color.from_hsl( value / max_iteration, 1, 0.5 if value else 0 )

##############################################################################
class Mandelbrot( Canvas ):
    """A Mandelbrot-plotting widget."""

    DEFAULT_CSS = """
    Mandelbrot {
        width: 1fr;
        height: 1fr;
    }
    """

    max_iteration: var[ int ] = var( 80 )
    "Maximum number of iteratios to perform."

    from_x: var[ Decimal ] = var( Decimal( -2.5 ) )
    """Start X position for the plot."""

    to_x: var[ Decimal ] = var( Decimal( 1.5 ) )
    """End X position for the plot."""

    from_y: var[ Decimal ] = var( Decimal( -1.5 ) )
    """Start Y position for the plot."""

    to_y: var[ Decimal ] = var( Decimal( 1.5 ) )
    """End Y position for the plot."""

    def frange( self, r_from: Decimal, r_to: Decimal, size: int ) -> Iterator[ Decimal ]:
        """Generate a float range for the plot.

        Args:
            r_from: The value to generate from.
            r_to: The value to generate to.
            size: The size of canvas in the desired direction..

        Yields:
            Decimal: Values between the range to fit the plot.
        """
        steps = 0
        step  = Decimal( r_to - r_from ) / Decimal( size )
        n     = Decimal( r_from )
        while n < r_to and steps < size:
            yield n
            n += Decimal( step )
            steps += 1

    def mandelbrot( self, x: Decimal, y: Decimal ) -> int:
        """Return the Mandelbrot calculation for the point.

        Returns:
            The number of loops to escape, or 0 if it didn't.

        Note:
            The point is considered to be stable, considered to have not
            escaped, if the ``max_iteration`` has been hit without the
            calculation going above 2.0.
        """
        c1 = complex( x, y )
        c2 = 0j
        for n in range( self.max_iteration ):
            if abs( c2 ) > 2:
                return n
            c2 = c1 + ( c2 * c2 )
        return 0

    def plot( self ) -> None:
        """Plot the Mandelbrot set using the current conditions."""
        with self.app.batch_update():
            for x_pixel, x_point in enumerate( self.frange( self.from_x, self.to_x, self.width ) ):
                for y_pixel, y_point in enumerate( self.frange( self.from_y, self.to_y, self.height ) ):
                    self.set_pixel(
                        x_pixel, y_pixel, colour_map( self.mandelbrot( x_point, y_point ), self.max_iteration )
                    )

    def on_mount( self ) -> None:
        """Get the plotter going once the DOM is ready."""
        self.plot()

### mandelbrot.py ends here
