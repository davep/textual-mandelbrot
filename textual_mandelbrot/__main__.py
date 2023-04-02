"""Mandelbrot plotting application for the terminal."""

##############################################################################
# Python imports.
from __future__ import annotations

##############################################################################
# Textual imports.
from textual.app     import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Header, Footer

##############################################################################
# Local imports.
from .           import __version__
from .mandelbrot import Mandelbrot
from .colouring  import default_map, blue_brown_map, shades_of_green

##############################################################################
class MandelbrotApp( App[ None ] ):
    """A Textual-based Mandelbrot set plotting application for the terminal."""

    TITLE = "Mandelbrot"
    """The title for the application."""

    SUB_TITLE = f"v{__version__}"
    """The sub-title for the application."""

    CSS = """
    Screen {
        align: center middle;
    }

    Mandelbrot {
        border: round grey;
    }
    """

    BINDINGS = [
        Binding( "1", "colour( 0 )", "Colours 1", show=False ),
        Binding( "2", "colour( 1 )", "Colours 2", show=False ),
        Binding( "3", "colour( 2 )", "Colours 2", show=False )
    ]
    """Keyboard bindings for the application."""

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
        plot                 = self.query_one( Mandelbrot )
        plot.border_title    = f"{event.from_x:.10f}, {event.from_y:.10f} -> {event.to_x:.10f}, {event.to_y:.10f}"
        plot.border_subtitle = f"{event.multibrot:0.2f} multibrot | {event.max_iteration:0.2f} iterations"

    def action_colour( self, colour: int ) -> None:
        """Set a colour scheme for the plot.

        Args:
            colour: The number of the colour scheme to use.
        """
        self.query_one( Mandelbrot ).set_colour_source( [
            default_map, blue_brown_map, shades_of_green
        ][ colour] )

##############################################################################
def main() -> None:
    """Main entry point for the console script version."""
    MandelbrotApp().run()

##############################################################################
# Run the main application if we're being called on as main.
if __name__ == "__main__":
    main()

### __main__.py ends here
