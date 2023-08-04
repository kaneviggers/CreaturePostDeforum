from image_queue import image_queue
from screeninfo import get_monitors
import threading
import asyncio
import pygame
import queue
import os

global window
# global image_queue
global running

lock = threading.Lock()

def init():
    global window
    # global image_queue

    # image_queue = queue.Queue()

    second_screen_width, second_screen_height = find_second_display_resolution()

    if second_screen_width is None and second_screen_height is None:
        print("Failed to get second display resolution")
    
    os.environ["SDL_VIDEO_WINDOW_POS"] = f"{second_screen_width},0"

    pygame.init()

    window = pygame.display.set_mode((second_screen_width, second_screen_height), pygame.FULLSCREEN)
    pygame.display.set_caption("Image Generator")

    run()

def find_second_display_resolution():
    monitors = get_monitors()
    if len(monitors) >= 2:
        second_monitor = monitors[1]
        second_screen_width = second_monitor.width
        second_screen_height = second_monitor.height
        return second_screen_width, second_screen_height
    else:
        print("Second display not found.")
        return None, None

def display_image(path):
    global window

    image = pygame.image.load(path)

    print(image.get_height())
    print(image.get_width())


    # img_surface = pygame.surfarray.make_surface(image)
    window.blit(image, (0, 0))
    pygame.display.flip()
    # pygame.display.update()

def process_messages():
    global running
    # global image_queue

    while running:
        try:
            image = image_queue.get(timeout=0.1)  # Non-blocking get with timeout
        except queue.Empty:
            continue

        # Process the message (you can define your own message format and actions)
        # if message.get("type") == "image":
        #     image = message.get("data")
        #     display_image(image)

        print(image)

def run():
    global running
    # global image_queue

    running = True

    message_thread = threading.Thread(target=process_messages)
    message_thread.start()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        while not image_queue.empty():
            image = image_queue.get()
            display_image(image)
    
    running = False
    pygame.quit()

    message_thread.join()

def stop():
    global running

    running = False