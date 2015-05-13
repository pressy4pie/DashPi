import os
import pygame
import time
import random

class dash :
    def __init(self):
	# init dash method.
	self.description = "The class to get info for the dash drawings"
	self.author = "PressY4Pie (Connor Rigby)"
    
    def get_speed(self):
	# The function to get speed from the stuff. for now it will be spoofed to 65 mph.	
	return 65

class pyscope :
    screen = None;
    
    def __init__(self):
        "Ininitializes a new pygame screen using the framebuffer"
        # Based on "Python GUI in Linux frame buffer"
        # http://www.karoltomala.com/blog/?p=679
        disp_no = os.getenv("DISPLAY")
        if disp_no:
            print "I'm running under X display = {0}".format(disp_no)
        
        # Check which frame buffer drivers are available
        # Start with fbcon since directfb hangs with composite output
        drivers = ['fbcon', 'directfb', 'svgalib']
        found = False
        for driver in drivers:
            # Make sure that SDL_VIDEODRIVER is set
            if not os.getenv('SDL_VIDEODRIVER'):
                os.putenv('SDL_VIDEODRIVER', driver)
            try:
                pygame.display.init()
            except pygame.error:
                print 'Driver: {0} failed.'.format(driver)
                continue
            found = True
            break
    
        if not found:
            raise Exception('No suitable video driver found!')
        
        size = (pygame.display.Info().current_w, 
pygame.display.Info().current_h)
        print "Full framebuffer size: %d x %d" % (size[0], size[1])
        self.screen = pygame.display.set_mode((size[0], size[1]),pygame.FULLSCREEN)
        # Clear the screen to start
        self.screen.fill((0, 0, 0))
        # Initialise font support
        pygame.font.init()
        # Render the screen
        pygame.display.update()

    def __del__(self):
        "Destructor to make sure pygame shuts down, etc."
    
    def write(self, input_text, x, y):
	font = pygame.font.Font(None, 30)
        text_surface = font.render(input_text, True, (255, 255, 255))  # White text
        # Blit the text at input x, and y
        self.screen.blit(text_surface, (x, y))

# This is where the main stuff starts...
# Create an instance of the PyScope class
# Initialize dashinfo
scope = pyscope()
dashinfo = dash()
# Don't display cursor.
pygame.mouse.set_visible(False)
# Make a font
font = pygame.font.Font(None, 30)

screen_size = (pygame.display.Info().current_w, pygame.display.Info().current_h)

# Fill/clear the screen & Update.
scope.screen.fill((0,0,0))
pygame.display.update()


# Images
speedo_bac = pygame.image.load('test_speedo.png').convert()

# The test screen to be drawn on cuz i cant figure out how to make a surface this size..
pygame.draw.rect(scope.screen, (255,255,255), (0,0,320,240) ,1)
scope.screen.blit(speedo_bac,(0,0))
pygame.display.update()

pygame.draw.line(scope.screen, (255,255,255), (160,120), (66,193), 1)
pygame.display.update()
ev = pygame.event.poll()
while ev.type != pygame.QUIT:
	# Do the main stuff.
	time.sleep(1)




#exit in 2 seconds
time.sleep(2)

