import pygame
import math
pygame.font.init()
WIDTH, HEIGHT = 1200,700
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("SOLAR SYSTEM SIM")

#CONSTANTS
FPS = 60

#COLORS
YELLOW = (255,255,0)
BLUE = (100,100,255)
RED = (200,50,50)
DARK_GRAY = (80,70,81)
WHITE = (255,255,255 )
ORANGE = (150,100,64)


#FONT
FONT = pygame.font.SysFont("comicsans",15)


class Planet():

    AU = 149.6e6 * 1000 #this is 146 million and 600 thousand kilometers converted to meters (multiply by 1000)
    G = 6.67428e-11 
    SCALE = 80/AU  #1AU = 100 pixels
    TIMESTEP = 3600 * 24 #1 day 
    def __init__(self,x,y,radius,color,mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.vel_x = 0
        self.vel_y = 0

        self.sun = False #specify that the planet is the sun or not
        self.satern = False
        self.distance_to_sun = 0 #the distance of a planet to the sun
        self.orbit = [] 

    def draw(self,win):

        x = self.x * self.SCALE + WIDTH/2
        y = self.y * self.SCALE + HEIGHT/2

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x,y = point
                x = x * self.SCALE + WIDTH/2
                y = y * self.SCALE + HEIGHT/2
                updated_points.append((x,y))

            pygame.draw.lines(win,self.color,False,updated_points,2)
        
        pygame.draw.circle(win,self.color,(x,y),self.radius)

        if not self.sun:
            distance_text = FONT.render(f'{round(self.distance_to_sun/1000,1)}km',1,WHITE)
            win.blit(distance_text,(x-distance_text.get_width()/2,y-distance_text.get_height()/2))
        
        if self.satern:
            pygame.draw.circle(win,self.color,(x,y),35,2)

        

    def attraction(self,other):
        other_x  = other.x
        other_y = other.y

        distance_x  = other_x - self.x 
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x **2 +distance_y**2)#get the distance between 2 object

        if other.sun:#check if the other planet is the sun
            self.distance_to_sun = distance 
        
        force = self.G * self.mass * other.mass / distance**2 #calculate the force of attraction
        theta = math.atan2(distance_y,distance_x)#calculate angle theta
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force

        return force_x,force_y


    def update_position(self,planets):
        total_fx =total_fy = 0
        for planet in planets:
            if self == planet:
                continue

            fx,fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy
            
        #calculate the speed/velocity
        self.vel_x += total_fx/self.mass * self.TIMESTEP
        self.vel_y += total_fy/self.mass * self.TIMESTEP
        #update x ,y position using the speed and using the accurate amount of time
        self.x += self.vel_x *self.TIMESTEP
        self.y += self.vel_y*self.TIMESTEP

        self.orbit.append((self.x,self.y))



#PLANET OBJECTS
sun = Planet(0,0,20,YELLOW,1.98892 * 10**30)
sun.sun = True

earth = Planet(-1 * Planet.AU, 0,16,BLUE,5.9742 * 10**24)
earth.vel_y = 29.783 * 1000 #kilometers converted to meters

mars = Planet(-1.524 * Planet.AU,0,12,RED,6.39 * 10**23)
mars.vel_y = 24.077 *1000

mercury = Planet(0.387 * Planet.AU,0,8,DARK_GRAY , 3.30 * 10**23)
mercury.vel_y = -47.4 * 1000

venus = Planet(0.723 * Planet.AU,0,14,WHITE,4.8685*10**24)
venus.vel_y = -35.02 * 1000

jupiter = Planet(3.204 * Planet.AU,0,20,DARK_GRAY,1898.13*10**24)
jupiter.vel_y = -13.06 *1000

satern = Planet(6.573* Planet.AU,0,22,ORANGE,568.32*10**24)
satern.satern = True
satern.vel_y = -9.68*1000

planets = [sun,earth,mars,mercury,venus,jupiter,satern]

clock = pygame.time.Clock()
run = True
while run:#game loop
    clock.tick(FPS)
    WIN.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    #draw plantes
    for planet in planets:
        planet.update_position(planets)

        planet.draw(WIN)


    pygame.display.update()

pygame.quit()