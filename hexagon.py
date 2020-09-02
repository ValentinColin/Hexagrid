import pygame
import math

from colors import Colors


class Hexagon:
    """An hexagon that can be alive or dead."""
    width = 1

    def __init__(self, points, alive=False):
        """Create a hexagon alive or dead."""
        self.points = points
        self.alive = alive

    @property
    def color(self):
        """Return the color of the polygon."""
        return (Colors.white if self.alive else Colors.black)

    def show(self, screen):
        """Show the hexagon."""
        pygame.draw.polygon(screen, self.color, self.points)
        pygame.draw.polygon(screen, Colors.grey, self.points, Hexagon.width)

    @property
    def center(self):
        """Average of the points of the hexagon.
        Meaning its the center of the hexagon."""
        x_list, y_list = zip(*self.points)
        return (
            sum(x_list)/len(x_list),
            sum(y_list)/len(y_list)
        )

    @property
    def upper_radius(self):
        """Return the radius of the smallest circle that contains the hexagon."""
        xc, yc = self.center
        xp, yp = self.points[0]
        return math.sqrt((xp-xc)**2 + (yp-yc)**2)

    @property
    def lower_radius(self):
        """Return the radius of the bigest circle contained in the hexagone."""
        return self.upper_radius * math.cos(math.pi/6) # cos(30 degree)

    def __contains__(self, point):
        """Check if a polygon contains a point."""
        xc, yc = self.center
        xp, yp = point
        return math.sqrt((xc-xp)**2+(yc-yp)**2) <= self.lower_radius
