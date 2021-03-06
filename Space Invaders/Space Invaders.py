import sys
import pygame

screen_width = 1200
screen_height = 550
player_spaceship = pygame.image.load("spaceship.png")
game_background = pygame.image.load("space background.png")
laser_png = pygame.image.load("bullet.png")
game_background = pygame.transform.scale(game_background, (1200, 550))
laser_png = pygame.transform.scale(laser_png, (54, 54))
enemy_alien = pygame.image.load("alien_ship.png")
enemy_alien = pygame.transform.scale(enemy_alien, (70, 65))


class space_ship(pygame.sprite.Sprite):  # Jayson/Mahmoud // player model, controls, positions for the laser
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_spaceship
        self.rect = self.image.get_rect()
        self.rect.centerx = screen_width / 2
        self.rect.bottom = screen_height / 1.1
        self.pos = self.rect.centerx, self.rect.bottom
        self.speed_ship = 0
        self.shot = pygame.time.get_ticks()

    def update(self):
        self.speed_ship = 0
        cd = 250  # bullet speed // delay between shots

        key_state = pygame.key.get_pressed()
        if key_state[pygame.K_LEFT]:
            self.speed_ship = -9
        if key_state[pygame.K_RIGHT]:
            self.speed_ship = 9
        self.rect.x += self.speed_ship
        if self.rect.right > screen_width:
            self.rect.right = screen_width
        if self.rect.left < 0:
            self.rect.left = 0

        time_now = pygame.time.get_ticks()

        if key_state[pygame.K_SPACE] and time_now - self.shot > cd:  # bullet keybinding // new sprite group for the laser
            laser = Laser(self.rect.centerx, self.rect.top)
            laser_group.add(laser)
            self.shot = time_now


class Laser(pygame.sprite.Sprite):  # Mahmoud class Laser // Laser init
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = laser_png
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):  # Jayson def update // collision
        self.rect.y -= 5
        if self.rect.bottom < 0:
            self.kill()
        if pygame.sprite.spritecollide(self, alien_group, True):  # Jayson
            self.kill()


laser_group = pygame.sprite.Group()
alien_group = pygame.sprite.Group()


class Aliens(pygame.sprite.Sprite):  # Jayson class Aliens() // enemy aliens, movement
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_alien
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y
        self.move_counter = 0
        self.move_direction = 1

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 500:
            self.move_direction *= -1
            self.move_counter *= self.move_direction


def main():  # Jayson def main // Game main loop
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Space Invaders")
    fps = pygame.time.Clock()

    all_sprites = pygame.sprite.Group()
    spaceship = space_ship()
    all_sprites.add(spaceship)

    for i in range(0, 10):
        alien_group.add(Aliens(i * 70, 50))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        all_sprites.update()
        screen.blit(game_background, (0, 0))
        all_sprites.draw(screen)
        laser_group.update()
        laser_group.draw(screen)
        alien_group.update()
        alien_group.draw(screen)
        pygame.display.flip()
        fps.tick(60)


main()
