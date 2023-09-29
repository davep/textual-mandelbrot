"""Command palette commands for the Mandelbrot application."""

##############################################################################
# Python imports.
from functools import partial

##############################################################################
# Textual imports.
from textual.command import Hit, Hits, Provider

##############################################################################
# Local imports.
from .colouring import default_map, blue_brown_map, shades_of_green
from .mandelbrot import Mandelbrot


##############################################################################
class MandelbrotCommands(Provider):
    """A source of command palette commands for the Mandelbrot widget."""

    async def search(self, query: str) -> Hits:
        """Handle a request to search for system commands that match the query.

        Args:
            user_input: The user input to be matched.

        Yields:
            Command hits for use in the command palette.
        """

        # Nothing in here makes sense if the user isn't current on a
        # Mandelbrot set.
        if not isinstance(self.focused, Mandelbrot):
            return

        # Get a fuzzy matcher for looking for hits.
        matcher = self.matcher(query)

        # Spin out some commands for setting the colours.
        for colour, source in (
            ("default", default_map),
            ("blue/brown", blue_brown_map),
            ("green", shades_of_green),
        ):
            colour = f"Mandelbrot: Set the colour map to {colour} "
            match = matcher.match(colour)
            if match:
                yield Hit(
                    match,
                    matcher.highlight(colour),
                    partial(self.focused.set_colour_source, source),
                    help=f"Set the Mandelbrot colour palette to {colour}",
                )

        # Spin out some commands based around available actions.
        for command, action, help in (
            ("Go home", "zero", "Go to 0, 0 in the Mandelbrot set"),
            ("Reset", "reset", "Reset the Mandelbrot set"),
        ):
            command = f"Mandelbrot: {command}"
            match = matcher.match(command)
            if match:
                yield Hit(
                    match,
                    matcher.highlight(command),
                    partial(self.focused.run_action, action),
                    help=help,
                )


### commands.py ends here
