import pyglet
from pyglet.gl import *
from random import randint

# Next line avoids a particular bug crashing on my laptop
# pyglet.options['graphics_vbo'] = False 

# Enable alpha blending
glEnable(GL_BLEND)              
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

# Load Score font
pyglet.font.add_file('data/showg.ttf')
bladerunner = pyglet.font.load('Showcard Gothic')

# Create game window and GUI
window = pyglet.window.Window()
scorelabel = pyglet.text.Label('Fruit Pick',
                          font_name='Showcard Gothic',
                          font_size=12,
                          x=window.width - 10, y=window.height - 10,
                          anchor_x='right', anchor_y='top')

# Initialise global objects like sprites of PC and NPC
player = pyglet.sprite.Sprite(pyglet.image.load("data/catcher.png"))
fruits_seq = pyglet.image.ImageGrid(pyglet.image.load("data/fruits.png"), 1, 6)
fps_display = pyglet.clock.ClockDisplay()
falling = [[0, 50, 400], ]
plunk = pyglet.media.load('data/receive.wav', streaming=False)

@window.event
def on_mouse_motion(x, y, dx, dy):
    player.x, player.y = x, 100

@window.event
def on_draw():
    window.clear()
    scorelabel.draw()
    for f in falling:
        fruits_seq[f[0]].blit(f[1], f[2])
    player.draw()
    fps_display.draw()

ticks = 0
score = 0
def update(dt):
    global ticks, falling, score, scorelabel, plunk
    ticks += 1
    if not falling:
        return
    for f in falling:
        # Check for a catch. Player must be close to the fruit 
        if 100 <= f[2] <= 120 and player.x - 30 <= f[1] <= player.x + 30: 
            if f[0] == 1:
                print "You caught a tomato. It is not a fruit!"
                pyglet.app.exit()
            f[2] = 0
            score += 10
            plunk.play()
            scorelabel.text = "Fruit Value Rs. %04d.00" % score
        f[2] -= 4
    # Purge caught fruits and fruits outside the screen
    falling_new = [f for f in falling if f[2] > 0]
    # Add new fruits if less fruits on screen
    if len(falling_new) <= 10 and ticks % 10 == 0:
        falling_new.append([randint(0,5), randint(20,800), 400])
    falling = falling_new

pyglet.clock.schedule_interval(update, 1/60.0) # update at 60Hz
pyglet.app.run()
print "Your Score is", score
