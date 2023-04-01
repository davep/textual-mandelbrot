"""Mandelbrot plotting application for the terminal."""

##############################################################################
# Python imports.
from __future__ import annotations

##############################################################################
# Textual imports.
from textual.app     import App, ComposeResult
from textual.widgets import Header, Footer

##############################################################################
# Local imports.
from .           import __version__
from .mandelbrot import Mandelbrot

##############################################################################
class MandelbrotApp( App[ None ] ):
    """A Textual-based Mandelbrot set plotting application for the terminal."""

    TITLE = f"Mandelbrot v{__version__}"
    """The title for the application."""

    CSS = """
    Screen {
        align: center middle;
    }

    Mandelbrot {
        border: heavy grey;
    }
    """

    def _best_size( self ) -> tuple[ tuple[ int, int ], tuple[ int, int ] ]:
        """Figure out the best initial size for the plot and the widget.

        Returns:
            A `tuple` of `tuple`s if two `int`. The first `tuple` is the
            suggested width and height of the canvas itself. The second is
            the suggested width and height for the widget.
        """

        # Get the initial width/height of the display. Note the little bit
        # of "magic number" work here; 2 is allowing for the border of the
        # Canvas widget; 4 is allowing for the border of the Canvas widget
        # and the Header and Footer widgets.
        display_width = self.app.console.width - 2
        display_height = self.app.console.height - 4

        # Go for 4:3 based off the width.
        best_width  = display_width
        best_height = ( ( display_width // 4 ) * 3 ) // 2

        # If that looks like it isn't going to fit nicely...
        if best_height >= display_height:
            # ...let's try and make it fit from the height first.
            best_height = display_height
            best_width  = ( ( best_height // 3 ) * 4 ) * 2

        # Final choice.
        return ( best_width - 2, ( best_height - 2 ) * 2 ), ( best_width, best_height )

    def _mandelbrot( self ) -> Mandelbrot:
        """Create the Mandelbrot plotting widget.

        Returns:
            The widget.
        """
        ( canvas_width, canvas_height ), ( widget_width, widget_height ) = self._best_size()
        plot = Mandelbrot( canvas_width, canvas_height )
        plot.styles.width  = widget_width
        plot.styles.height = widget_height
        return plot

    def compose( self ) -> ComposeResult:
        """Compose the child widgets."""
        yield Header()
        yield self._mandelbrot()
        yield Footer()

    def on_mount( self ) -> None:
        """Set things up once the DOM is available."""
        self.query_one( Mandelbrot ).focus()

    def on_mandelbrot_changed( self, event: Mandelbrot.Changed ) -> None:
        """Handle the parameters of the Mandelbrot being changed.

        Args:
            event: The event with the change details.
        """
        self.sub_title = (
            f"( {event.from_x:.6f}, {event.from_y:.6f} ) -> "
            f"( {event.to_x:.6f}, {event.to_y:.6f} )"
            f" | {event.max_iteration} iterations"
        )

##############################################################################
def main():
    """Main entry point for the console script version."""
    MandelbrotApp().run()

##############################################################################
# Run the main application if we're being called on as main.
if __name__ == "__main__":
    main()

### __main__.py ends here
