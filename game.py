import pygame

pygame.init()

screen = pygame.display.set_mode((640, 640))

delta_time = 0.1
clock = pygame.time.Clock()

img = pygame.image.load("img.png").convert()
img = pygame.transform.scale(img,
                             (img.get_width() * 2,
                              img.get_height() * 2))

imgs = pygame.Surface((64, 64), pygame.SRCALPHA)
imgs.blit(img, (0, 0))
imgs.blit(img, (20, 0))
imgs.blit(img, (10, 10))

font = pygame.font.Font(None, size=30)

x = 0

running = True
while running:
    screen.fill((255, 255, 255))

    img.set_alpha(max(0, 255 - x))
    screen.blit(imgs, (x, 30))

    x += 50 * delta_time

    text = font.render("Hello World!", True, (255, 0, 0))
    screen.blit(text, (300, 100))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

    delta_time = clock.tick(60) / 1000
    delta_time = max(0.001, min(0.1, delta_time))

pygame.quit()