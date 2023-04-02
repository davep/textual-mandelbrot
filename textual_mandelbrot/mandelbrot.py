"""Provides a Textual widget for plotting a Mandelbrot set."""

##############################################################################
# Python imports.
from __future__        import annotations
from decimal           import Decimal
from operator          import mul, truediv
from functools         import lru_cache
from typing            import Iterator
from typing_extensions import Final

##############################################################################
# Textual imports.
from textual.binding  import Binding
from textual.color    import Color
from textual.message  import Message

##############################################################################
# Textual-canvas imports.
from textual_canvas import Canvas

##############################################################################
@lru_cache()
def colour_map( value: int, max_iteration: int ) -> Color:
    """Calculate a colour for an escape value.

    Args:
        value: An escape value from a Mandelbrot set.

    Returns:
        The colour to plot the point with.
    """
    return Color.from_hsl( value / max_iteration, 1, 0.5 if value else 0 )

##############################################################################
@lru_cache()
def _mandelbrot( x: Decimal, y: Decimal, multibrot: float, max_iteration: int ) -> int:
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
    for n in range( max_iteration ):
        if abs( c2 ) > 2:
            return n
        c2 = c1 + ( c2 ** multibrot )
    return 0

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
        Binding(
            "up, w, k", "move( 0, -1 )", "Up", show=False
        ),
        Binding(
            "shift+up, W, W", "move( 0, -1, 50 )", "Up", show=False
        ),
        Binding(
            "down, s, j", "move( 0, 1 )", "Down", show=False
        ),
        Binding(
            "shift+down, S, J", "move( 0, 1, 50 )", "Down", show=False
        ),
        Binding(
            "left, a, h", "move( -1, 0 )", "Left", show=False
        ),
        Binding(
            "shift+left, A, H", "move( -1, 0, 50 )", "Left", show=False
        ),
        Binding(
            "right, d, l", "move( 1, 0 )", "Right", show=False
        ),
        Binding(
            "shift+right, D, L", "move( 1, 0, 50 )", "Right", show=False
        ),
        Binding(
            "pageup, right_square_bracket",
            "zoom( -1.2 )", "In", key_display="PgUp"
        ),
        Binding(
            "pagedown, left_square_bracket",
            "zoom( 1.2 )", "Out", key_display="PgDn"
        ),
        Binding(
            "ctrl+pageup, right_curly_bracket",
            "zoom( -2.0 )", "In+", key_display="Ctrl+PgUp"
        ),
        Binding(
            "ctrl+pagedown, left_curly_bracket",
            "zoom( 2.0 )", "Out+", key_display="Ctrl+PgDn"
        ),
        Binding(
            "shift+pageup", "multibrot( 1 )", "Mul+", key_display="Sh+PgUp"
        ),
        Binding(
            "shift+pagedown", "multibrot( -1 )", "Mul-", key_display="Sh+PgDn"
        ),
        Binding(
            "comma", "max_iter( -10 )","Res-"
        ),
        Binding(
            "less_than_sign", "max_iter( -100 )", "Res--"
        ),
        Binding(
            "full_stop", "max_iter( 10 )", "Res+"
        ),
        Binding(
            "greater_than_sign", "max_iter( 100 )", "Res++"
        ),
        Binding(
            "ctrl+r", "reset", "Reset"
        ),
        Binding(
            "escape", "app.quit", "Exit"
        )
    ]
    """Keyboard bindings for the widget."""

    class Changed( Message ):
        """Message sent when the range of the display changes.

        This will be sent if the user (un)zooms or moves the display.
        """

        def __init__( self, mandelbrot: Mandelbrot ) -> None:
            """Initialise the message.

            Args:
                mandelbrot: The Mandelbrot causing the message.
            """
            super().__init__()
            self.mandelbrot: Mandelbrot = mandelbrot
            """The Mandelbrot widget that caused the event."""
            self.multibrot: Decimal = mandelbrot._multibrot
            """The 'multibrot' value."""
            self.from_x: Decimal = mandelbrot._from_x
            """Start X position for the plot."""
            self.to_x: Decimal = mandelbrot._to_x
            """End X position for the plot."""
            self.from_y: Decimal = mandelbrot._from_y
            """Start Y position for the plot."""
            self.to_y: Decimal = mandelbrot._to_y
            """End Y position for the plot."""
            self.max_iteration = mandelbrot._max_iteration
            "Maximum number of iterations to perform."

    def __init__(
        self,
        width: int,
        height: int,
        name: str | None    = None,
        id: str | None      = None, # pylint:disable=redefined-builtin
        classes: str | None = None,
        disabled: bool      = False
    ):
        """Initialise the canvas.

        Args:
            width: The width of the Mandelbrot set canvas.
            height: The height of the Mandelbrot set canvas.
            name: The name of the Mandelbrot widget.
            id: The ID of the Mandelbrot widget in the DOM.
            classes: The CSS classes of the Mandelbrot widget.
            disabled: Whether the Mandelbrot widget is disabled or not.
        """
        super().__init__( width, height, name=name, id=id, classes=classes, disabled=disabled )
        self._max_iteration: int = 80
        "Maximum number of iterations to perform."
        self._multibrot: Decimal = Decimal( 2.0 )
        """The 'multibrot' value."""
        self._from_x: Decimal = Decimal( -2.5 )
        """Start X position for the plot."""
        self._to_x: Decimal = Decimal( 1.5 )
        """End X position for the plot."""
        self._from_y: Decimal = Decimal( -1.5 )
        """Start Y position for the plot."""
        self._to_y: Decimal = Decimal( 1.5 )
        """End Y position for the plot."""

    def reset( self ) -> None:
        """Reset the plot."""
        self._max_iteration = 80
        self._multibrot     = Decimal( 2 )
        self._from_x        = Decimal( -2.5 )
        self._to_x          = Decimal( 1.5 )
        self._from_y        = Decimal( -1.5 )
        self._to_y          = Decimal( 1.5 )

    def _frange( self, r_from: Decimal, r_to: Decimal, size: int ) -> Iterator[ Decimal ]:
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

    def _plot( self ) -> None:
        """Plot the Mandelbrot set using the current conditions."""
        with self.app.batch_update():
            for x_pixel, x_point in enumerate( self._frange( self._from_x, self._to_x, self.width ) ):
                for y_pixel, y_point in enumerate( self._frange( self._from_y, self._to_y, self.height ) ):
                    self.set_pixel(
                        x_pixel, y_pixel,
                        colour_map(
                            _mandelbrot( x_point, y_point, float( self._multibrot ), self._max_iteration ),
                            self._max_iteration
                        )
                    )
        self.post_message( self.Changed( self ) )

    def on_mount( self ) -> None:
        """Get the plotter going once the DOM is ready."""
        self._plot()

    def action_move( self, x: int, y: int, steps: int=5 ) -> None:
        """Move the Mandelbrot Set within the view.

        Args:
            x: The amount and direction to move in X.
            y: The amount and direction to move in Y.
        """

        x_step = Decimal( x * ( ( self._to_x - self._from_x ) / steps ) )
        y_step = Decimal( y * ( ( self._to_y - self._from_y ) / steps ) )

        self._from_x += x_step
        self._to_x   += x_step
        self._from_y += y_step
        self._to_y   += y_step

        self._plot()

    @staticmethod
    def _scale( from_pos: Decimal, to_pos: Decimal, zoom: Decimal ) -> tuple[ Decimal, Decimal ]:
        """Scale a dimension.

        Args:
            from_pos: The start position of the dimension.
            to_pos: The end position of the dimension.

        Returns:
            The new start and end positions.
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
            zoom: The amount to zoom by.
        """
        self._from_x, self._to_x = self._scale( self._from_x, self._to_x, zoom )
        self._from_y, self._to_y = self._scale( self._from_y, self._to_y, zoom )
        self._plot()

    def action_max_iter( self, change: int ) -> None:
        """Change the maximum number of iterations for a calculation.

        Args:
            change: The amount to change by.
        """
        # Keep a lower bound for the max iteration.
        if ( self._max_iteration + change ) >= 10:
            self._max_iteration += change
            self._plot()
        else:
            self.app.bell()

    def action_multibrot( self, change: Decimal ) -> None:
        """Change the 'multibrot' modifier.

        Args:
            change: The amount to change by.
        """
        if ( self._multibrot + change ) >= 2:
            self._multibrot += change
            self._plot()
        else:
            self.app.bell()

    def action_reset( self ) -> None:
        """Reset the display of the Mandelbrot set back to initial conditions."""
        self.reset()
        self._plot()

### mandelbrot.py ends here
