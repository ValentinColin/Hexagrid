import pygame
import math

from hexagon import Hexagon
from colors import Colors

class Simulation:
    """Main class for the simulation."""

    def __init__(self, size=(800, 800), layers=5):
        """Create the window the pygame."""
        self.layers = layers
        self.screen = pygame.display.set_mode(size, pygame.RESIZABLE)
        pygame.display.set_caption("Hexagones")
        pygame.display.flip()
        self.hexagons = []
        self.loop = True
        self.on = False
        self.hexagons = self.generate()

    @property
    def size(self):
        return self.screen.get_size()

    @property
    def w(self):
        return self.screen.get_size()[0]

    @property
    def h(self):
        return self.screen.get_size()[1]

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
                    self.layers += 1
                    self.hexagons = self.generate()
                elif event.key == pygame.K_DOWN:
                    if self.layers > 1:
                        self.layers -= 1
                    self.hexagons = self.generate()
                elif event.key == pygame.K_RIGHT:
                    self.update()
                    self.show()
                elif event.key == pygame.K_LEFT:
                    # ...Show the previous state of the grid...
                    self.show()
                elif event.key == pygame.K_p:
                    print(self.layers)
                elif event.key == pygame.K_r:
                    self.reset()

                # debug
                elif event.key == pygame.K_s:
                    for h in self.hexagons:
                        print("id:",h.id," -> state:",h.alive)
                    print("\n\n\n")

                elif event.key == pygame.K_SPACE:
                    self.on = not self.on
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.click(event.pos)
            elif event.type == pygame.VIDEORESIZE:
                self.screen = pygame.display.set_mode(
                    (event.w, event.h),
                    pygame.RESIZABLE
                )

    def click(self, position):
        """Check if a polygon is being hovered."""
        for hexagon in self.hexagons:
            if position in hexagon:
                hexagon.alive = not hexagon.alive

    def generate(self):
        return self.generate_rectangle()
        # return self.generate_by_turning_arround()

    def generate_rectangle(self):
        """Generate a square of hexagons in hexagonal space."""

        # No one will ever understand this code
        l = min(self.w, self.h)




        h = math.sqrt(3)/2

        layers = 2 * self.layers - 1

        w_rec = layers
        h_rec = layers

        l_rec = max(w_rec, h_rec)


        step = int(l / 2 / l_rec)
        radius = step / h

        hexagons = []

        for layer in range(layers):
            y_rec = layer - layers//2
            d1 = max(-layer, -(layers//2))
            d2 = min(layers//2, layers-layer-1)
            for x_rec in range(d1, d2+1):

                #print(x_rec, y_rec)
                x = x_rec / l_rec
                y = y_rec / l_rec

                x, y = self.hexagonal_to_cartesian(x, y)

                u = l/l_rec

                x *= l
                y *= l

                x += self.w/2
                y += self.h/2

                y = self.h - y
                print()

                hexagons.append(self.make_hexagon(x, y, radius))
        return hexagons

    def generate_by_turning_arround(self):
        """Generate the list of hexagons by ordering them in spiral."""
        # length of the biggest square that can fit in the window
        l = min(self.w, self.h)
        radius = int(l / self.layers / 4)

        # compute the steps to take between each hexagon draw
        center_to_edge= radius * math.cos(30*math.pi/180)
        step = 2 *  center_to_edge

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

    def update(self):
        """Update the simulation one step up."""
        list_update = []
        for h1 in self.hexagons:
            #print("----- Je regarde l'hexa d'id:",h1.id,"-----")
            count = 0
            for h2 in self.hexagons:
                if h1 != h2:
                    #print("test voisins entre",h1.id,"et",h2.id,"=",self.are_neighbours(h1, h2))
                    if self.are_neighbours(h1, h2): # ne rentre jamais dans la condition
                        if h2.alive:
                            count += 1
                    #print("count (id?:",h2.id,") :",count)
            if count >= 3:
                list_update.append(h1)
        for h in list_update:
            h.alive = True
        #print("\n\n")

    def are_neighbours(self, h1, h2):
        """Are h1 and h2 neighbours? so is the question."""
        x1, y1 = h1.center
        x2, y2 = h2.center
        # ATTENTION: test d'inégalité sur des flottant !!!!
        # J'ai donc pris le upper_radius pour être tranquille
        return math.sqrt((x1-x2)**2 + (y1-y2)**2) <= (h1.upper_radius + h2.upper_radius)

    def show(self):
        """Show the simulation at a given step."""
        self.screen.fill(Colors.black)
        self.show_hexagons()
        self.show_text_on_or_off()
        pygame.display.flip()

    def reset(self):
        """Reset all the hexagones (all will be dead)"""
        for h in self.hexagons:
            h.alive = False

    def show_text_on_or_off(self): # à finir
        """Show if the simulation is on or off."""
        font = pygame.font.SysFont('freesansbold', 32)
        if self.on:     text = font.render('On' , True, Colors.green)
        else:           text = font.render('Off', True, Colors.red  )
        textRect = text.get_rect()
        textRect.centerx = 10
        textRect.centery = 10

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

    def cartesian_to_hexagonal(self, x, y):
        """https://cdn.discordapp.com/attachments/729992302575091718/750448489304948916/IMG_20200901_221213.jpg
        Deal with it.
        x1, y1 = (math.cos(-math.pi/4), math.sin(-math.pi/4))
        x2, y2 = (0, 1)

        return (
            x1*x + y1*y
            x2*x + y2*y
        )"""
        # return (x*(math.sqrt(3)/2), y - x/2)
        return (x - y/2, y*(math.sqrt(3)/2))

    def hexagonal_to_cartesian(self, x, y):
        """Conversion from hexagonal space to cartesian space."""
        h = math.sqrt(3)/2
        y_ = y * h
        return (x + y/2, y_)

if __name__ == "__main__":
    pygame.init()
    simulation = Simulation()
    simulation.main()
