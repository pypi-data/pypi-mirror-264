"""Colorize terminal output with regex."""

import re
import sys
from math import sin, tau

HEXCODE_PATTERN = r"^([0-9a-f]{6})(:([0-9a-f]{6}))?$"
COLOR = "\x1b[38;2;{0};{1};{2}m"
COLOR_PAIR = "\x1b[38;2;{0};{1};{2};48;2;{3};{4};{5}m"
RESET = "\x1b[0m"


def _to_hex(channel: int) -> str:
    return hex(channel)[2:].zfill(2)


def _rainbow_gradient(n: int) -> list[str]:
    theta = tau / n
    offsets = [0, tau / 3, 2 * tau / 3]

    def color(i):
        return (_to_hex(int(sin(i * theta + offset) * 127 + 128)) for offset in offsets)

    return ["".join(color(i)) for i in range(n)]


def _ansi_from_hexcode(hexcode: str) -> str:
    if (match := re.match(HEXCODE_PATTERN, hexcode)) is None:
        raise ValueError(f"Invalid hexcode: {hexcode}")

    fg_hexcode = match[1]
    fg_digits = fg_hexcode.removeprefix("#")
    fr, fg, fb = int(fg_digits[:2], 16), int(fg_digits[2:4], 16), int(fg_digits[4:], 16)

    if (bg_hexcode := match[3]) is None:
        return COLOR.format(fr, fg, fb)

    bg_digits = bg_hexcode.removeprefix("#")
    br, bg, bb = int(bg_digits[:2], 16), int(bg_digits[2:4], 16), int(bg_digits[4:], 16)
    return COLOR_PAIR.format(fr, fg, fb, br, bg, bb)


def tat(pattern: str, colors: list[str] | None = None) -> None:
    """
    Colorize stdin with a regex pattern.

    Parameters
    ----------
    pattern : str
        Regex pattern used on stdin.
    colors : list[str] | None, default: None
        Color or color-pair for each group in the regex pattern. If none or too few are
        provided, rainbow colors are used.
    """
    regex = re.compile(pattern)

    if colors is None or len(colors) < regex.groups:
        colors = _rainbow_gradient(regex.groups)
    colors = [_ansi_from_hexcode(color) for color in colors]

    piped = sys.stdin.read()
    out = []
    pos = 0
    for match in regex.finditer(piped):
        out.append(piped[pos : match.start()])
        pos = match.start()
        groups: list[tuple[int, str]] = [(match.end(), RESET)]
        for i in range(regex.groups):
            start, end = match.span(i + 1)

            previous_end, color = groups[-1]
            while start >= previous_end:
                groups.pop()
                if previous_end > pos:
                    out.append(color)
                    out.append(piped[pos:previous_end])
                    out.append(RESET)
                    pos = previous_end
                previous_end, color = groups[-1]

            if start > pos:
                out.append(color)
                out.append(piped[pos:start])
                out.append(RESET)
                pos = start

            groups.append((end, colors[i]))

        while groups:
            end, color = groups.pop()
            if end > pos:
                out.append(color)
                out.append(piped[pos:end])
                out.append(RESET)
                pos = end

    out.append(piped[pos:])
    print("".join(out), end="")
