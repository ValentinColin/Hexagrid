import pygame
import math

pygame.init()


class Colors:
    """Namespace for colors."""
    white = (255, 255, 255)
    black = (0, 0, 0)
    grey  = (127, 127, 127)
    red   = (255,0,0)
    green = (0,255,0)
    blue  = (0,0,255)


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
        xc, yc = self.center
        xp, yp = self.points[0]
        return math.sqrt((xp-xc)**2 + (yp-yc)**2)

    @property
    def lower_radius(self):
        return self.upper_radius * math.cos(math.pi/6) # cos(30 degree)

    def __contains__(self, point):
        """Check if a polygon contains a point."""
        xc, yc = self.center
        xp, yp = point
        return math.sqrt((xc-xp)**2+(yc-yp)**2) <= self.lower_radius


class Simulation:
    """Main class for the simulation."""

    def __init__(self, size=(1000, 800), layers=5):
        """Create the window the pygame."""
        self.size = size
        self.layers = layers
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Hexagones")
        pygame.display.flip()
        self.hexagons = []
        self.loop = True
        self.on = False
        self.hexagons = self.generate_by_turning_arround()

    @property
    def w(self):
        return self.size[0]
    
    @property
    def h(self):
        return self.size[1]

    def main(self):
        """Start the whole program."""
        while self.loop:
            if self.on: self.update()
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
                elif event.key == pygame.K_UP:
                    self.hexagons = self.generate_by_turning_arround()
                    self.layers += 1
                elif event.key == pygame.K_DOWN:
                    self.hexagons = self.generate_by_turning_arround()
                    if self.layers > 1:
                        self.layers -= 1
                elif event.key == pygame.K_RIGHT:
                    self.update()
                    self.show()
                elif event.key == pygame.K_LEFT:
                    self.update()
                    self.show()
                elif event.key == pygame.K_p:
                    print(self.layers)
                elif event.key == pygame.K_SPACE:
                    self.on = not self.on
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.check_hover(event.pos)
    
    def check_hover(self, position):
        """Check if a polygon is being hovered."""
        for hexagon in self.hexagons:
            if position in hexagon:
                hexagon.alive = not hexagon.alive

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
                a = 120 + ai * 60

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
        for h1 in self.hexagons:
            count = 0
            for h2 in self.hexagons:
                if self.is_neighbour(h1, h2):
                    if h2.alive:
                        count += 1
            if count >= 3:
                h1.alive = True

    def is_neighbour(self, h1, h2):
        """Are h1 and h2 neighbours? so is the question."""
        x1, y1 = h1.center
        x2, y2 = h2.center
        return math.sqrt((x1-x2)**2 + (y1-y2)**2) <= h1.lower_radius + h2.lower_radius

    def show(self):
        """Show the simulation at a given step."""
        self.screen.fill(Colors.black)
        self.show_hexagons()
        self.show_update()
        pygame.display.flip()

    def show_update(self):
        """Show if the simulation is on or off."""
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render('GeeksForGeeks', True, Colors.green, Colors.blue)
        textRect = text.get_rect()
        pass

    def show_hexagons(self):
        """Show all hexagons."""
        for hexagon in self.hexagons:
            hexagon.show(self.screen)


    def make_hexagon(self, x, y, radius, phase = math.pi/2):
        """Create an hexagon given its position in pixels and its radius."""
        points = []
        for a in range(6):
            points.append((
                int(x + radius * math.cos(a*60*math.pi/180+phase)) ,
                int(y + radius * math.sin(a*60*math.pi/180+phase))
                ))
        return Hexagon(points)


if __name__ == "__main__":
    simulation = Simulation()
    simulation.main()







