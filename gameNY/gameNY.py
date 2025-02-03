import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

# Настройка размеров окна
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Заголовок окна
pygame.display.set_caption("Новогодний сбор подарков")

# Класс персонажа
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('santa.png').convert_alpha()
        self.rect = self.image.get_rect(center=(screen_width // 2, screen_height - 50))
        self.speed = 20
    
    def update(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if key[pygame.K_RIGHT]:
            self.rect.x += self.speed
        
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > screen_width:
            self.rect.right = screen_width

# Класс подарка
class Gift(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('gift.png').convert_alpha()
        self.rect = self.image.get_rect(
            center=(random.randint(100, screen_width - 100), random.randint(100, screen_height - 200)))
        self.collected = False
    
    def update(self):
        if self.collected:
            self.rect.center = (random.randint(100, screen_width - 100), random.randint(100, screen_height - 200))
            self.collected = False
        else:
            self.rect.y += 5
            if self.rect.bottom >= screen_height:
                self.rect.center = (random.randint(100, screen_width - 100), random.randint(100, screen_height - 200))
                self.collected = True

# Класс 
class Snowflake(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('snowflake.png').convert_alpha()
        self.rect = self.image.get_rect(
            center=(random.randint(0, screen_width), 0))
        self.speed = random.randint(1, 5)
    
    def update(self):
        self.rect.y += self.speed
        if self.rect.top > screen_height:
            self.kill()

def main():
    clock = pygame.time.Clock()
    FPS = 60
    
    player = Player()
    gifts = pygame.sprite.Group()
    snowflakes = pygame.sprite.Group()
    
    score = 0
    lives = 3
    game_over = False
    start_time = pygame.time.get_ticks()
    total_time = 60 * 1000  # 30 секунд
    
    # Изначально добавляем 5 подарков
    for _ in range(1):
        gift = Gift()
        gifts.add(gift)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        current_time = pygame.time.get_ticks() - start_time
        remaining_time = max(total_time - current_time, 0)
        
        player.update()
        gifts.update()
        snowflakes.update()
        
        collected_gifts = pygame.sprite.spritecollide(player, gifts, False)
        for gift in collected_gifts:
            gift.collected = True
            score += 1
        
        hit_snowflakes = pygame.sprite.spritecollide(player, snowflakes, True)
        if hit_snowflakes:
            lives -= len(hit_snowflakes)
        
        if random.random() < 0.01:
            snowflake = Snowflake()
            snowflakes.add(snowflake)
        
        # Проверяем, были ли собраны все подарки
        all_collected = all(gift.collected for gift in gifts.sprites())
        if all_collected:
            # Удваиваем количество подарков
            for _ in range(len(gifts)):
                gift = Gift()
                gifts.add(gift)
        
        screen.fill((0, 0, 0))  # Черный фон
        screen.blit(pygame.image.load('newhouse.png'), (0, 0))
        gifts.draw(screen)
        snowflakes.draw(screen)
        screen.blit(player.image, player.rect)
        
        font = pygame.font.Font(None, 36)
        time_text = font.render(f"Тime: {remaining_time//1000}", True, (255, 255, 255))
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        lives_text = font.render(f"Lives: {lives}", True, (255, 255, 255))
        screen.blit(time_text, (20, 20))
        screen.blit(score_text, (screen_width - 120, 20))
        screen.blit(lives_text, (screen_width // 2 - 40, 20))
        
        if remaining_time <= 0 or lives <= 0:
            game_over = True
        
        if game_over:
            break
        
        pygame.display.flip()
        clock.tick(FPS)
    
    end_screen(screen, score)

def end_screen(screen, final_score):
    font = pygame.font.Font(None, 48)
    text = font.render(f"Game Over! Your Score: {final_score}", True, (255, 255, 255))
    rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(text, rect)
    pygame.display.flip()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

if __name__ == "__main__":
    main()