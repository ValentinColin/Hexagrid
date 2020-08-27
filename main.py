import pygame
import math

pygame.init()


class Colors:
    """Namespace for colors."""
    white = (255, 255, 255)
    black = (0, 0, 0)
    grey = (127, 127, 127)


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
    def lower_radius(self):
        c = self.center
        return c[0]

    @property
    def upper_radius(self):
        pass

    def __contains__(self, point):
        """Check if a polygon contains a point."""
        x, y = point
        return 


class Simulation:
    """Main class for the simulation."""

    def __init__(self, size=(1000, 800)):
        """Create the window the pygame."""
        self.size = size
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Hexagones")
        pygame.display.flip()
        self.min = 5
        self.max = 9
        self.hexagons = []
        self.loop = True
        self.layers= 5

    @property
    def w(self):
        return self.size[0]
    
    @property
    def h(self):
        return self.size[1]

    def main(self):
        """Start the whole program."""
        while self.loop:
            self.update()
            self.loop_events()
            self.show()


    def loop_events(self):
        """For clicking maybe."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.loop = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.loop = False
                if event.key == pygame.K_UP:
                    self.layers += 1
                if event.key == pygame.K_DOWN:
                    if self.layers > 1:
                        self.layers -= 1
                if event.key == pygame.K_d:
                    print(self.layers)

            elif event.type == pygame.MOUSEMOTION:
                # event.mouse
                # self.check_hover(event.x, event.y)
                pass
    
    def check_hover(self, x, y):
        """Check if a polygon is being hovered."""
        for polygon in self.polygons:
            if (x, y) in polygon:
                polygon.alive = True
            else:
                polygon.alive = False
    

    def generate_by_turning_arround(self):
        """Generate the list of hexagons."""
        l = min(self.w, self.h)
        d = self.layers*2
        s = int(l / d / 2)
        x, y = self.w/2, self.h/2

        hexagons = []

        radius = l/d
        step = radius * math.cos(30*math.pi/180)

        hexagons.append(
            self.make_hexagon(x,y,radius/2)
        )

        for nb_turns in range(1, self.layers):

            x += step

            for ai in range(6):
                a = 120 + ai*60

                for n in range(nb_turns):
                    x += step*math.cos(a*math.pi/180)
                    y += step*math.sin(a*math.pi/180)

                    if ai != 6:
                        hexagons.append(
                            self.make_hexagon(x,y,s)
                        )
                
        return hexagons
    
    def draw_one(self, xr, yr):
        """Relative positions."""
        l = min(self.w, self.h)
        d = self.max - self.min
        s = int(l / d / 2)
        x = int(xr*l/d+self.w/2)
        y = int(yr*l/d+self.h/2)
        return self.make_hexagon(x, y, s)


    def update(self):
        """Update the simulation one step up."""
        self.hexagons = self.generate_by_turning_arround()

    def show(self):
        """Show the simulation at a given step."""
        self.screen.fill(Colors.black)
        for hexagon in self.hexagons:
            hexagon.show(self.screen)
        pygame.display.flip()

    def make_hexagon(self, x, y, radius):
        """Create an hexagon given its position in pixels and its radius."""
        phase = math.pi/2
        points = []
        for a in range(6):
            points.append((
                int(x + radius * math.cos(a*60*math.pi/180+phase)),
                int(y + radius * math.sin(a*60*math.pi/180+phase))
                ))
        return Hexagon(points)


if __name__ == "__main__":
    simulation = Simulation()
    simulation.main()