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
sound = pygame.mixer.Sound("sound.mp3")

x = 0

running = True
moving = False

while running:
    screen.fill((255, 255, 255))

    screen.blit(imgs, (x, 30))

    hitbox = pygame.Rect(x, 30, img.get_width(), img.get_height())

    m_pos = pygame.mouse.get_pos()

    target = pygame.Rect(300, 0, 160, 280)
    collision = hitbox.colliderect(target)
    m_collision = target.collidepoint(m_pos)
    pygame.draw.rect(screen, (255 * collision, 255 * m_collision, 0), target)

    if moving:
        x += 50 * delta_time

    text = font.render("Hello World!", True, (255, 0, 0))
    screen.blit(text, (300, 100))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                moving = True
            if event.key == pygame.K_f:
                sound.play()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                moving = False


    pygame.display.flip()

    delta_time = clock.tick(60) / 1000
    delta_time = max(0.001, min(0.1, delta_time))

pygame.quit()