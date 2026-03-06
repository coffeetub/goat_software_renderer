import ctypes
import time
import random

renderer = ctypes.CDLL("./librenderer.so")

# function signatures
renderer.init_display.argtypes = [ctypes.c_uint32]
renderer.init_display.restype = ctypes.c_void_p

renderer.render_frame.argtypes = [ctypes.c_void_p]

renderer.clear_frame.argtypes = []
renderer.clear_frame.restype = None

renderer.draw_rect.argtypes = [
    ctypes.c_int, ctypes.c_int,
    ctypes.c_int, ctypes.c_int,
    ctypes.c_uint32,
    ctypes.c_void_p
]

renderer.poll_events.argtypes = [ctypes.c_void_p]
renderer.poll_events.restype = ctypes.c_int

renderer.key_pressed.restype = ctypes.c_int

# create window
window = renderer.init_display(0x000000)

WIDTH = 800
HEIGHT = 600

# player
player_x = 350
player_y = 550
player_w = 100
player_h = 20

# falling block
block_x = random.randint(0, WIDTH-40)
block_y = 0
block_w = 40
block_h = 40

running = True

while running:

    running = renderer.poll_events(window)

    # CLEAR FRAMEBUFFER EACH FRAME
    renderer.clear_frame()

    key = renderer.key_pressed()

    # left arrow
    if key == 65361:
        player_x -= 10

    # right arrow
    if key == 65363:
        player_x += 10

    player_x = max(0, min(WIDTH-player_w, player_x))

    # move falling block
    block_y += 5

    # collision detection
    if (block_y + block_h >= player_y and
        block_x < player_x + player_w and
        block_x + block_w > player_x):

        block_y = 0
        block_x = random.randint(0, WIDTH-40)

    # missed block
    if block_y > HEIGHT:
        block_y = 0
        block_x = random.randint(0, WIDTH-40)

    # draw player
    renderer.draw_rect(player_x, player_y,
                       player_w, player_h,
                       0x00ff00, window)

    # draw falling block
    renderer.draw_rect(block_x, block_y,
                       block_w, block_h,
                       0xff0000, window)

    renderer.render_frame(window)

    time.sleep(0.016)