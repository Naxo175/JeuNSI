import pygame

# Game variables
GAME_WIDTH = 512
GAME_HEIGHT = 512

PLAYER_X = GAME_WIDTH/2
PLAYER_Y = GAME_HEIGHT/2
PLAYER_WIDTH = 120
PLAYER_HEIGHT = 120
PLAYER_DISTANCE = 5

GRAVITY = 0.5
FRICTION = 0.4
PLAYER_VELOCITY_X = 5
PLAYER_VELOCITY_Y = -10
FLOOR_Y = GAME_HEIGHT * 3/4


# Images
def load_image(relative_path, scale = None):
    image = pygame.image.load("images/" + relative_path)
    if scale != None:
        image = pygame.transform.scale(image, scale)
    return image

background_img = load_image("country-platform/country-platform-preview.png", (384 * 2.3, 224 * 2.3))
player_walk_left_img = load_image("player/player_walk_left.png", (PLAYER_WIDTH, PLAYER_HEIGHT))
player_walk_right_img = load_image("player/player_walk_right.png", (PLAYER_WIDTH, PLAYER_HEIGHT))
player_jump_left_img = load_image("player/player_jump_left.png", (PLAYER_WIDTH, PLAYER_HEIGHT))
player_jump_right_img = load_image("player/player_jump_right.png", (PLAYER_WIDTH, PLAYER_HEIGHT))

pygame.init()
window = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption("Nature Finder")
pygame.display.set_icon(player_walk_right_img)
clock = pygame.time.Clock() # Used for the frame rate


class Player(pygame.Rect):
    def __init__(self):
        pygame.Rect.__init__(self, PLAYER_X, PLAYER_Y, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.image = player_walk_right_img
        self.velocity_x = 0
        self.velocity_y = 0
        self.direction = 1
        self.jumping = False

    def update_image(self):
        if self.jumping:
            if self.direction == "right":
                self.image = player_jump_right_img
            elif self.direction == "left":
                self.image = player_jump_left_img
        else:
            if self.direction == "right":
                self.image = player_walk_right_img
            elif self.direction == "left":
                self.image = player_walk_left_img

player = Player()


def move():
    if player.direction == "left" and player.velocity_x < 0:
        player.velocity_x += FRICTION
    elif player.direction == "right" and player.velocity_x > 0:
        player.velocity_x -= FRICTION
    else:
        player.velocity_x = 0


    player.x += player.velocity_x


    player.velocity_y += GRAVITY
    player.y += player.velocity_y

    if player.y + player.height > FLOOR_Y:
        player.y = FLOOR_Y - player.height
        player.jumping = False

def draw():
    window.fill((84, 222, 158))
    window.blit(background_img, (-200, 0))
    player.update_image()
    window.blit(player.image, player)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and not player.jumping:
        player.velocity_y = PLAYER_VELOCITY_Y
        player.jumping = True
    if keys[pygame.K_DOWN]:
        player.y += PLAYER_DISTANCE
    if keys[pygame.K_LEFT]:
        player.velocity_x = -PLAYER_VELOCITY_X
        player.direction = "left"
    if keys[pygame.K_RIGHT]:
        player.velocity_x = PLAYER_VELOCITY_X
        player.direction = "right"
            
    move()
    draw()
    pygame.display.update()
    clock.tick(60) # 60 fps

pygame.quit()