import os
import pygame
import time
import random
import serial

class dash :
    def __init__ (self)
	ser = serial.Serial('/dev/ttyAMA0', 115200)
	ser.write(' ')

    def get_speed(self):
	# The function to get speed from the stuff. for now it will be spoofed to 65 mph.	
	return 100

    def get_rpm(self):
	# Read the negitive side of the ignition coil to get rpm. 
	# It is just pulses so it should just count them then do some math to get rotations per minute.
	# For now we set it to a fixed number till i create the hardware and maybe get an arduino in the mix.
	return 1500

    def get_gas(self):
	# The gas sender is just a resistor that i should be able to measure the resistance across. I don't know what the data will look like so thie is just a filler.
	return 0

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

# Fill/clear the screen & Update.
scope.screen.fill((0,0,0))
pygame.display.update()


# Images
#speedo_bac = pygame.image.load('test_speedo.png').convert()
#scope.screen.blit(speedo_bac,(0,0))

# The test screen to be drawn on cuz i cant figure out how to make a surface this size..
pygame.draw.rect(scope.screen, (255,255,255), (0,0,320,240) ,1)
pygame.draw.rect(scope.screen, (255,255,255), (0,0,320,20), 1)

# Top Header thing
scope.write("Welcome Connor",85,1)

pygame.display.update()
ev = pygame.event.poll()
ser = serial.Serial('/dev/ttyACM0', 115200)
ser.write(str(chr(1))) # Send some data to get some data...
while ev.type != pygame.QUIT:
	# Do the main stuff.
	print ser.readline()

	speed = dashinfo.get_speed()
	rpm = dashinfo.get_rpm()
	gas = dashinfo.get_gas()
	# Of course this will look better but for now it works.
	# scope.write('Current Speed: {} MPH'.format(speed), 30, 45)
	scope.write('Current RPMs: {} RPM'.format(rpm), 30, 115)
	scope.write('Current Gas Meter: {}% '.format(gas), 30, 190) 

	pygame.display.update()



#exit in 2 seconds
time.sleep(2)

