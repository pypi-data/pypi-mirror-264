"""Parse the command-line for arguments to `tat`."""

import argparse

from .tat import tat


def tat_cli() -> None:
    """Parse command-line arguments for `tat`."""
    parser = argparse.ArgumentParser(description="Colorize terminal output with regex.")
    parser.add_argument(
        "pattern", metavar="REGEX", help="A regex pattern to be used on output."
    )
    parser.add_argument(
        "colors",
        metavar="COLORS",
        nargs="*",
        help=(
            "List of colors or color-pairs for each group in the regex. "
            "If no colors are given, default colors will be used. "
            "Colors are specified with a hexcode (ex: `ff02a3`) and "
            "color-pairs are specified with two hexcodes separated by a colon "
            "(ex: `123abc:070aca`)."
        ),
    )

    args = parser.parse_args()
    tat(args.pattern, args.colors)
