import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

class Enemy(pygame.sprite.Sprite):
    def __init__(self, level):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-50, -10)
        self.speed = random.randrange(1, 5) + level

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > HEIGHT:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-50, -10)
            self.speed = random.randrange(1, 5)

def show_message(screen, message, font_size=36, y_offset=0):
    font = pygame.font.Font(None, font_size)
    text = font.render(message, True, RED)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2 + y_offset))
    pygame.display.flip()
    pygame.time.wait(2000)

def main():
    global all_sprites, enemies, player
    level = 1
    score = 0
    running = True

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pygame Shooter")
    clock = pygame.time.Clock()

    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    player = Player()
    all_sprites.add(player)

    for _ in range(10 * level):
        enemy = Enemy(level)
        all_sprites.add(enemy)
        enemies.add(enemy)

    def reset_game():
        nonlocal level, score
        level = 1
        score = 0
        all_sprites.empty()
        enemies.empty()
        global player
        player = Player()
        all_sprites.add(player)
        for _ in range(10 * level):
            enemy = Enemy(level)
            all_sprites.add(enemy)
            enemies.add(enemy)
        player.rect.centerx = WIDTH // 2
        player.rect.bottom = HEIGHT - 10

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for enemy in enemies.copy():
            if enemy.rect.colliderect(player.rect):
                show_message(screen, "Game Over - Score: {}".format(score))
                reset_game()
            elif enemy.rect.top >= HEIGHT:
                score += 1
                enemies.remove(enemy)
                all_sprites.remove(enemy)
                new_enemy = Enemy(level)
                all_sprites.add(new_enemy)
                enemies.add(new_enemy)

        screen.fill(WHITE)
        all_sprites.draw(screen)
        all_sprites.update()

        if len(enemies) == 0:
            level += 1
            for _ in range(10 * level):
                enemy = Enemy(level)
                all_sprites.add(enemy)
                enemies.add(enemy)

        font = pygame.font.Font(None, 36)
        score_text = font.render("Score: {}".format(score), True, BLUE)
        level_text = font.render("Level: {}".format(level), True, BLUE)
        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (10, 50))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()