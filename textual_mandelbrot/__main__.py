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

    TITLE = "Mandelbrot"
    """The title for the application."""

    SUB_TITLE = f"v{__version__}"
    """The sub-title for the application."""

    def compose( self ) -> ComposeResult:
        """Compose the child widgets."""
        yield Header()
        yield Mandelbrot( 128, 96 )
        yield Footer()

##############################################################################
# Run the main application if we're being called on as main.
if __name__ == "__main__":
    MandelbrotApp().run()

### __main__.py ends here
