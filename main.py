import vlc 
from time import sleep
from rpi_ws281x import PixelStrip, Color
import argparse
import PIL.ImageGrab

# LED configuration.
LED_COUNT = 83        # Number of LED pixels.
LED_PIN = 18          # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 127  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

# Define functions which animate LEDs in various ways.
def colorWipe(strip, color):
    """Wipe color across display a pixel at once."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
    strip.show()

def moving_point(strip, color_old, color_point, pause):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color_point)
        if i > 2:
          strip.setPixelColor(i-3, color_old)
        sleep(pause)
        strip.show()
          
    for i in range(3,0,-1):
      strip.setPixelColor(strip.numPixels()-i, color_old)
      strip.show()


# Vorbereiten des Players
Instance = vlc.Instance()
player = Instance.media_player_new()
Media = Instance.media_new("typo.mp4")
Media.get_mrl()
player.set_media(Media)
player.set_fullscreen(True)
player.play()
sleep(1)
Instance.vlm_set_loop("typo",True)

# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    # Create NeoPixel object with appropriate configuration.
    strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    print('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    try:
        while True:
            r, g, b = PIL.ImageGrab.grab().load()[600,960]
            if (vlc.libvlc_media_player_get_position(player) > 0.93):
              player.set_position(0.0)            # Player reset
            elif ( 0.1 < vlc.libvlc_media_player_get_position(player) < 0.12): moving_point(strip, Color(r,g,b), Color(255, 255, 255), 0.01)
            else:
              colorWipe(strip, Color(r,g,b))  # Pink wipe

    except KeyboardInterrupt:
        if args.clear:
            colorWipe(strip, Color(0, 0, 0))
