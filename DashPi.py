import os
import pygame
import time
import random
import serial

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
scope = pyscope()
# Don't display cursor.
pygame.mouse.set_visible(False)
# Make a font
font = pygame.font.Font('DroidSans.ttf', 30)

# Fill/clear the screen & Update.
scope.screen.fill((0,0,0))
pygame.display.update()

# The test screen to be drawn on cuz i cant figure out how to make a surface this size..
main_rect = pygame.draw.rect(scope.screen, (0,0,0), (0,0,320,240))
main_rect_outline = pygame.draw.rect(scope.screen, (255,255,255), (0,0,320,240),1)
header_rect = pygame.draw.rect(scope.screen, (0,0,0), (0,0,320,20))
header_rect = pygame.draw.rect(scope.screen, (255,255,255), (0,0,320,20),1)

# Top Header thing
# I'm sure ill display some actual information at some point.
scope.write("Welcome Connor",85,1)

# Update the screen before starting the main loop
pygame.display.update()

# Start the serial stuff.
# The arduino doesn't start reporting data untill it gets some data.
# Any ol' data will do.
ser = serial.Serial('/dev/ttyACM0', 115200)
ser.write(str(chr(1))) # Send some data to get some data...

ev = pygame.event.poll()
while ev.type != pygame.QUIT:
	# Do the main stuff.

	# The serial data will be formatted as such:
	# 65.00 1500 50
	# MPH   RPM  GAS%

	# Get the line for serial, split it up and spit it with scope.write.
	line = ser.readline() # This is the actual serial command
	splitLine = line.split()
	# print len(splitLine)

	if len(splitLine) < 4: # Make sure we have the correct data here.
		speed = splitLine[0]
		rpm = splitLine[1]
		gas = splitLine[2]


	#Just for testing. This is to spammy. maybe ill add a verbose mode or debug mode or something.
	#print speed
	#print rpm
	#print gas

	# Of course this will look better but for now it works.
	scope.write('Current Speed: {} MPH'.format(speed), 30, 45)
	scope.write('Current RPMs: {} RPM'.format(rpm), 30, 115)
	scope.write('Current Gas Meter: {}% '.format(gas), 30, 190)
	# Update the display so we can see what's up.
	pygame.display.update()

	main_rect = pygame.draw.rect(scope.screen, (0,0,0), (0,20,320,220))


#exit in 2 seconds
time.sleep(2)

