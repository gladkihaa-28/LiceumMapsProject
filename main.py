import sys
import pygame
import pygame.font
import aiohttp
import asyncio
from pygame.locals import *
from pygame import *
from win32api import GetSystemMetrics

back_color = "#003153"
screen_width = GetSystemMetrics(0)
screen_height = GetSystemMetrics(1)

async def get_map_async(cord_x=37, cord_y=55, spn_x=0.5, spn_y=0.5, type_map="map"):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://static-maps.yandex.ru/1.x/?ll={cord_x},{cord_y}&spn={spn_x},{spn_y}&l={type_map}') as response:
            data = await response.read()
            with open('map_image.png', 'wb') as f:
                f.write(data)

def get_resolution():
    info = pygame.display.Info()
    screen_width = info.current_w
    screen_height = info.current_h
    return screen_width, screen_height

def draw_text(screen, text, color, x, y):
    font = pygame.font.SysFont('Calibri', 36)
    label = font.render(text, True, color)
    screen.blit(label, (x, y))

async def main_menu_async():
    global wins
    global dies
    pygame.init()
    screen = pygame.display.set_mode(get_resolution())
    pygame.display.set_caption("Alpha_0.1")
    screen.fill(Color(back_color))

    while True:
        screen.fill((30, 30, 30))
        but_width = screen_width / 2 - 50
        but_h = screen_height / 2 - 50
        draw_text(screen, "Maps", (255, 255, 255), screen_width / 2 - 90, screen_height / 2 - 250)
        draw_text(screen, "Start", (255, 255, 255), but_width, screen_height / 2 - 200)
        draw_text(screen, "Exit", (255, 255, 255), but_width, screen_height / 2 - 150)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if but_width <= x <= but_width + 200 and screen_height / 2 - 200 <= y <= screen_height / 2 - 160:
                    await main_async()
                elif but_width <= x <= but_width + 200 and screen_height / 2 - 150 <= y <= screen_height / 2 - 110:
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()

async def main_async():
    cord_x = 37
    cord_y = 56
    spn_x = 0.5
    spn_y = 0.5

    pygame.init()
    screen = pygame.display.set_mode(get_resolution())
    pygame.display.set_caption("Alpha_0.1")
    screen.fill(Color(back_color))

    running = True
    while running:
        for e in pygame.event.get():
            if e.type == QUIT:
                running = False
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                running = False
                await main_menu_async()
            if e.type == KEYDOWN and e.key == K_w:
                cord_y += 0.5
            if e.type == KEYDOWN and e.key == K_s:
                cord_y -= 0.5
            if e.type == KEYDOWN and e.key == K_d:
                cord_x += 0.5
            if e.type == KEYDOWN and e.key == K_a:
                cord_x -= 0.5
            if e.type == KEYDOWN and e.key == K_UP:
                spn_y += 0.1
                spn_x += 0.1
            if e.type == KEYDOWN and e.key == K_DOWN:
                spn_y -= 0.1
                spn_x -= 0.1

        await get_map_async(cord_x, cord_y, spn_x, spn_y, "map")
        background_image = pygame.transform.scale(pygame.image.load('map_image.png'), (900, 700))
        bg = pygame.Surface((get_resolution()))
        bg.blit(background_image, (0, 0))

        pygame.display.update()
        pygame.time.Clock().tick(120)
        screen.blit(bg, (1, 1))

if __name__ == "__main__":
    pygame.init()
    asyncio.run(main_menu_async())
