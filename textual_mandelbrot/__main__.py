"""Mandelbrot plotting application for the terminal."""

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
        width: 130;
        height: 50;
    }
    """

    def compose( self ) -> ComposeResult:
        """Compose the child widgets."""
        yield Header()
        yield Mandelbrot( 128, 96 )
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
            f"{event.from_x:.2f}, "
            f"{event.from_y:.2f} -> "
            f"{event.to_x:.2f}, "
            f"{event.to_y:.2f} -- "
            f"{event.max_iteration} iterations"
        )

##############################################################################
# Run the main application if we're being called on as main.
if __name__ == "__main__":
    MandelbrotApp().run()

### __main__.py ends here
