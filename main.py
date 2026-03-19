import pygame
import pygame.gfxdraw

WIDTH = 1920
HIGHT = 1080
pygame.init()

screen = pygame.display.set_mode((WIDTH, HIGHT))
def main():

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill("black")

        # Render Here
        for i in range(HIGHT //2):
            draw_pixel(i, i, (255, 0, 0))

        # End render
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

def draw_pixel(x, y, color:tuple[int, int, int]):
    ScreenX = int((WIDTH /2) + x)
    ScreenY = int((HIGHT /2) - y)
    r, g, b = clamp(color[0]), clamp(color[1]), clamp(color[2])


    pygame.gfxdraw.pixel(screen, ScreenX, ScreenY, (r, g, b))

def clamp (n):
    if n < 0:
        return 0
    elif n > 255:
        return 255
    else:
        return n
if __name__ == "__main__":
    main()