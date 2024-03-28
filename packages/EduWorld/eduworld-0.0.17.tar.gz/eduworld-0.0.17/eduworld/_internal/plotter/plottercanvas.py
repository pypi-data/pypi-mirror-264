r"""
This file is part of eduworld package.

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

import time

from ..canvas import Canvas


class Pen:
    """Simple data holder for Pen props"""

    def __init__(self):
        self.pos = [0, 0]
        self.color = "black"
        self.width = 5
        self.can_draw = False

    def move_by(self, dx: float, dy: float) -> None:
        """Move pen relatively to its position"""
        self.pos[0] += dx
        self.pos[1] += dy

    def set_pos(self, x: float, y: float) -> None:
        """Set absolute pen position"""
        self.pos[0] = x
        self.pos[1] = y

    def set_width(self, width: int) -> None:
        """Set pen width. Constrained between 1 .. 15"""
        self.width = int(max(1, min(width, 15)))


# pylint: disable=too-many-ancestors, too-many-instance-attributes
class PlotterCanvas(Canvas):
    """Class for drawing lines of many colors aka Plotter"""

    def __init__(self, parent):
        super().__init__(parent)
        self._unit_size = 25
        self._width = 0
        self._height = 0
        self._origin = []
        self._pen = Pen()
        self._lines = []

    def pen_raise(self):
        """Raise the pen. Plotter with pen raised can't draw lines"""
        self._pen.can_draw = False

    def pen_lower(self):
        """Lower the pen. Plotter with pen lowered can draw lines"""
        self._pen.can_draw = True

    def pen_color(self, color: str) -> None:
        """Set the pen color"""
        self._pen.color = color

    def pen_width(self, width: int) -> None:
        """Set the pen width"""
        self._pen.set_width(width)

    def pen_move_by(self, dx: float, dy: float) -> None:
        """Move pen by dx and dy"""
        p = self._pen
        last = p.pos.copy()
        p.move_by(dx, dy)
        if p.can_draw:
            coords = last + p.pos.copy()
            self._lines.append((coords, p.width, p.color))
        self.redraw()

    def pen_set_pos(self, x: float, y: float) -> None:
        """Set absolute pen position"""
        p = self._pen
        last = p.pos.copy()
        p.set_pos(x, y)
        if p.can_draw:
            coords = last + p.pos.copy()
            self._lines.append((coords, p.width, p.color))
        self.redraw()

    def redraw(self, immediate=False) -> None:
        """Redraw everything"""
        if not immediate:
            time.sleep(self._draw_delay)
        self._height = self.winfo_height()
        self._width = self.winfo_width()
        self._origin = [self._unit_size * 2, self._height - self._unit_size * 2]
        self._delete_all()
        self._draw_grid()
        self._draw_lines()
        self._draw_pen()
        self.root.update()

    def _delete_all(self):
        self.delete("grid")
        self.delete("lines")
        self.delete("pen")

    def _draw_pen(self):
        ox = self._origin[0]
        oy = self._origin[1]
        (x, y) = self._pen.pos.copy()
        x = ox + x * self._unit_size
        y = oy - y * self._unit_size
        r = self._unit_size / 2 * 0.2
        c = [x - r, y - r, x + r, y + r]
        tags = ("pen",)
        self.create_oval(c, width=2, outline="black", fill="gray95", tags=tags)

    def _draw_lines(self):
        for line in self._lines:
            self._draw_line(line)

    def _draw_line(self, line):
        ox = self._origin[0]
        oy = self._origin[1]
        coords = line[0].copy()
        width = line[1]
        color = line[2]
        coords[0] = ox + coords[0] * self._unit_size  # xs
        coords[1] = oy - coords[1] * self._unit_size  # ys
        coords[2] = ox + coords[2] * self._unit_size  # xs
        coords[3] = oy - coords[3] * self._unit_size  # ys
        self.create_line(coords, fill=color, width=width, tags=("lines",))

    def _draw_grid(self):
        self._draw_verticals()
        self._draw_horizontals()
        self._draw_x_arrow()
        self._draw_y_arrow()

    def _draw_x_arrow(self):
        half_unit_size = self._unit_size * 0.5
        y = self._height - self._unit_size * 2
        x = self._width - self._unit_size
        arrowhead_x = x - half_unit_size
        arrowhead_top = y - half_unit_size
        arrowhead_bottom = y + half_unit_size
        coords = [
            # shaft
            0,
            y,
            x,
            y,
            # left side
            arrowhead_x,
            arrowhead_top,
            # central
            x,
            y,
            # right side
            arrowhead_x,
            arrowhead_bottom,
        ]
        self.create_line(coords, fill="gray40", width=2, tags=("grid",))

    def _draw_y_arrow(self):
        half_unit_size = self._unit_size * 0.5
        x = self._unit_size * 2
        y = self._unit_size
        arrowhead_y = self._unit_size + half_unit_size
        arrowhead_left = x - half_unit_size
        arrowhead_right = x + half_unit_size
        coords = [
            # shaft
            x,
            self._height,
            x,
            y,
            # left side
            arrowhead_left,
            arrowhead_y,
            # central
            x,
            y,
            # right side
            arrowhead_right,
            arrowhead_y,
        ]
        self.create_line(coords, fill="gray40", width=2, tags=("grid",))

    def _draw_verticals(self):
        line_count = int((self._width / self._unit_size)) + 1
        for i in range(line_count):
            shift = i * self._unit_size
            coords = [shift, 0, shift, self._height]
            self.create_line(coords, fill="gray70", width=1, tags=("grid",))

    def _draw_horizontals(self):
        line_count = int((self._height / self._unit_size)) + 1
        shift = self._height
        for _ in range(line_count):
            shift -= self._unit_size
            coords = [0, shift, self._width, shift]
            self.create_line(coords, fill="gray70", width=1, tags=("grid",))
