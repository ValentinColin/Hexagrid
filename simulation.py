import pygame
import math

from hexagon import Hexagon
from colors import Colors

class Simulation:
    """Main class for the simulation."""

    def __init__(self, size=(1000, 800), layers=5):
        """Create the window the pygame."""
        self.layers = layers
        self.screen = pygame.display.set_mode(size, pygame.RESIZABLE)
        pygame.display.set_caption("Hexagones")
        pygame.display.flip()
        self.hexagons = []
        self.loop = True
        self.on = False
        self.hexagons = self.generate_by_turning_arround()

    @property
    def size(self):
        return self.screen.get_size()

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
            elif event.type == pygame.VIDEORESIZE:
                self.screen = pygame.display.set_mode(
                    (event.w, event.h),
                    pygame.RESIZABLE
                )
    
    def check_hover(self, position):
        """Check if a polygon is being hovered."""
        for hexagon in self.hexagons:
            if position in hexagon:
                hexagon.alive = not hexagon.alive

    def generate_by_turning_arround(self):
        """Generate the list of hexagons."""
        # length of the biggest square that can fit in the window
        l = min(self.w, self.h) 
        radius = int(l / self.layers / 4)

        # compute the steps to take between each hexagon draw
        step = 2 * radius * math.cos(30*math.pi/180)

        # and start storing hexagons in a list starting from the middle one 
        x, y = self.w/2, self.h/2

        hexagons = [
            self.make_hexagon(x,y,radius)
        ]

        # for each turn in spiral around the middle
        for nb_turns in range(1, self.layers):

            # make one step right
            x += step

            # then turn around the middle by rotating 6 times
            for rotation in range(6):
                angle = 120 + rotation * 60

                # and for each rotation make as many steps as the
                # current number of turn
                for n in range(nb_turns):
                    x += step*math.cos(angle*math.pi/180)
                    y += step*math.sin(angle*math.pi/180)

                    # and of course add the generated hexagon to the list
                    # while making sure there are no duplicates at
                    # the end of the turn
                    if rotation != 6: 
                        hexagons.append(
                            self.make_hexagon(x,y,radius)
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
        # self.show_text_on_or_off()
        pygame.display.flip()

    def show_text_on_or_off(self):
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
    pygame.init()
    simulation = Simulation()
    simulation.main()
