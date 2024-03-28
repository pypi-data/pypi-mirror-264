r"""
This package provides the following functions defined in __all__ for writing
simple procedural style programs with AlgoWorld Robots

This file is part of eduworld package

=== LICENSE INFO ===

Copyright (c) 2024 - Stanislav Grinkov

The eduworld package is free software: you can redistribute it
and/or modify it under the terms of the GNU General Public License
as published by the Free Software Foundation, either version 3
of the License, or (at your option) any later version.

The package is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with the algoworld package.
If not, see `<https://www.gnu.org/licenses/>`_.
"""

import sys
import tkinter as tk

# from random import randint as rnd
from eduworld import Application, PlotterCanvas as Canvas

app: Application = Application()
canvas: Canvas = Canvas(app.root)
initialized: bool = False


def _hide_tk_err(f):
    def w(*args, **kwargs):
        try:
            f(*args, **kwargs)
        except tk.TclError:
            sys.exit(1)

    return w


def _bind_keys():
    app.root.bind("<W>", lambda _: canvas.pen_move_by(0, 1))
    app.root.bind("<w>", lambda _: canvas.pen_move_by(0, 0.5))
    app.root.bind("<S>", lambda _: canvas.pen_move_by(0, -1))
    app.root.bind("<s>", lambda _: canvas.pen_move_by(0, -0.5))
    app.root.bind("<A>", lambda _: canvas.pen_move_by(-1, 0))
    app.root.bind("<a>", lambda _: canvas.pen_move_by(-0.5, 0))
    app.root.bind("<D>", lambda _: canvas.pen_move_by(1, 0))
    app.root.bind("<d>", lambda _: canvas.pen_move_by(0.5, 0))
    app.root.bind("<R>", lambda _: canvas.pen_raise())
    app.root.bind("<r>", lambda _: canvas.pen_raise())
    app.root.bind("<F>", lambda _: canvas.pen_lower())
    app.root.bind("<f>", lambda _: canvas.pen_lower())


#    app.root.bind("<E>", lambda _: r.paint(_colors[rnd(0, _col_max)]))
#    app.root.bind("<e>", lambda _: r.paint(_colors[rnd(0, _col_max)]))


def setup(
    x: float = 0,
    y: float = 0,
    delay: float = 0.7,
    interactive: bool = False,
) -> None:
    """Setup the plotter"""
    global initialized
    if not initialized:
        initialized = True
        app.set_canvas(canvas)
        canvas.set_draw_delay(delay)
        canvas.pen_set_pos(x, y)
        if interactive:
            _bind_keys()
            canvas.set_draw_delay(0)
        app.run()


def shutdown(keep_window: bool = False) -> None:
    """Shut down the app"""
    app.shutdown(keep_window)


@_hide_tk_err
def pen_move_by(dx: float, dy: float) -> None:
    """Move pen by delta"""
    canvas.pen_move_by(dx, dy)


@_hide_tk_err
def pen_set_pos(x: float, y: float) -> None:
    """Move pen to apsolute x and y coordinates"""
    canvas.pen_set_pos(x, y)


def pen_raise() -> None:
    """Raise pen"""
    canvas.pen_raise()


def pen_lower() -> None:
    """Lower pen"""
    canvas.pen_lower()


def pen_color(color: str) -> None:
    """Set pen color"""
    canvas.pen_color(color)


def pen_width(width: int) -> None:
    """Set pen width"""
    canvas.pen_width(width)


__all__ = [
    # setup
    "setup",
    "shutdown",
    "pen_raise",
    "pen_lower",
    "pen_color",
    "pen_width",
    "pen_set_pos",
    "pen_move_by",
]
