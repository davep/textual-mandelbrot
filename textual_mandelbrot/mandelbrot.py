"""Provides a Textual widget for plotting a Mandelbrot set."""

##############################################################################
# Python imports.
from __future__        import annotations
from decimal           import Decimal
from operator          import mul, truediv
from typing            import Iterator
from typing_extensions import Final

##############################################################################
# Textual imports.
from textual.binding  import Binding
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

    BINDINGS = [
        Binding( "up",                   "move( 0, -1 )",    "Up",    key_display="↑" ),
        Binding( "down",                 "move( 0, 1 )",     "Down",  key_display="↓" ),
        Binding( "left",                 "move( -1, 0 )",    "Left",  key_display="←" ),
        Binding( "right",                "move( 1, 0 )",     "Right", key_display="→" ),
        Binding( "right_square_bracket", "zoom( -1.2 )",     "In",    key_display="]" ),
        Binding( "left_square_bracket",  "zoom( 1.2 )",      "Out",   key_display="[" ),
        Binding( "right_curly_bracket",  "zoom( -2.0 )",     "In+",   key_display="}" ),
        Binding( "left_curly_bracket",   "zoom( 2.0 )",      "Out+",  key_display="{" ),
        Binding( "comma",                "max_iter( -10 )",  "Res-",  key_display="," ),
        Binding( "less_than_sign",       "max_iter( -100 )", "Res--", key_display="<" ),
        Binding( "full_stop",            "max_iter( 10 )",   "Res+",  key_display="." ),
        Binding( "greater_than_sign",    "max_iter( 100 )",  "Res++", key_display=">" ),
    ]
    """Keyboard bindings for the widget."""

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

    MOVE_STEPS: Final = 5
    "Defines the granularity of movement in the application."

    def action_move( self, x: int, y: int ) -> None:
        """Move the Mandelbrot Set within the view.

        Args:
            x (int): The amount and direction to move in X.
            y (int): The amount and direction to move in Y.
        """

        x_step = Decimal( x * ( ( self.to_x - self.from_x ) / self.MOVE_STEPS ) )
        y_step = Decimal( y * ( ( self.to_y - self.from_y ) / self.MOVE_STEPS ) )

        self.from_x += x_step
        self.to_x   += x_step
        self.from_y += y_step
        self.to_y   += y_step

        self.plot()

    @staticmethod
    def _scale( from_pos: Decimal, to_pos: Decimal, zoom: Decimal ) -> tuple[ Decimal, Decimal ]:
        """Scale a dimension.

        Args:
            from_pos (Decimal): The start position of the dimension.
            to_pos (Decimal): The end position of the dimension.

        Returns:
            tuple[ Decimal, Decimal ]: The new start and end positions.
        """

        # Figure the operator from the sign.
        by = truediv if zoom < 0 else mul

        # We don't need the sign anymore.
        zoom = Decimal( abs( zoom ) )

        # Calculate the old and new dimensions.
        old_dim = to_pos - from_pos
        new_dim = Decimal( by( old_dim, zoom ) )

        # Return the adjusted points.
        return (
            from_pos + Decimal( ( old_dim - new_dim ) / 2 ),
            to_pos - Decimal( ( old_dim - new_dim ) / 2 )
        )

    def action_zoom( self, zoom: Decimal ) -> None:
        """Zoom in our out.

        Args:
            zoom (Decimal): The amount to zoom by.
        """

        # Apply the zoom.
        self.from_x, self.to_x = self._scale( self.from_x, self.to_x, zoom )
        self.from_y, self.to_y = self._scale( self.from_y, self.to_y, zoom )

        # Repaint.
        self.plot()

    def action_max_iter( self, change: int ) -> None:
        """Change the maximum number of iterations for a calculation.

        Args:
            change (int): The amount to change by.
        """
        # Keep a lower bound for the max iteration.
        if ( self.max_iteration + change ) > 10:
            self.max_iteration += change
            self.plot()
        else:
            self.app.bell()

### mandelbrot.py ends here
