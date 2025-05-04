import pygame
import random

# --------------------- Player ---------------------


class Player:


    def __init__(self, settings, world_width, world_height):
        self.settings = settings
        self.width = 50
        self.height = 50
        self.x = world_width // 2
        self.y = world_height // 2
        self.speed = self.settings.player_speed
        self.color = (0, 255, 0)
        self.world_width = world_width
        self.world_height = world_height
        self.health = self.settings.player_health 
        self.weapons = []  
        self.weapon_cooldowns = {}  
        self.attack_visuals = []  
        self.load_weapons()


    def load_weapons(self):
            weapon_list = ["sword", "bow", "magic_wand", "rock_staff"]
            self.weapons = weapon_list[:self.settings.player_weapon + 1]
            for weapon in self.weapons:
                self.weapon_cooldowns[weapon] = 0


    def add_weapon(self, weapon_name):
        if weapon_name not in self.weapons:
            self.weapons.append(weapon_name)
            self.weapon_cooldowns[weapon_name] = 0


    def take_damage(self, amount):
        effective_damage = max(0, amount - self.settings.player_armor)
        self.health -= effective_damage
        if self.health <= 0:
            self.settings.game_state = "menu"


    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
            if self.x < 0:
                self.x = 0
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
            if self.x + self.width > self.world_width:
                self.x = self.world_width - self.width
        if keys[pygame.K_UP]:
            self.y -= self.speed
            if self.y < 0:
                self.y = 0
        if keys[pygame.K_DOWN]:
            self.y += self.speed
            if self.y + self.height > self.world_height:
                self.y = self.world_height - self.height


    def attack(self, enemies, now, souls):
        for weapon in self.weapons:
            if now >= self.weapon_cooldowns[weapon]:
                if weapon == "sword":
                    self.attack_with_sword(enemies, souls)
                    self.weapon_cooldowns[weapon] = now + 400  
                elif weapon == "bow":
                    self.attack_with_bow(enemies, souls)
                    self.weapon_cooldowns[weapon] = now + 700  
                elif weapon == "magic_wand":
                    self.attack_with_magic_wand(enemies, souls)
                    self.weapon_cooldowns[weapon] = now + 600  
                elif weapon == "rock_staff":
                    self.attack_with_rock_staff(enemies, souls)
                    self.weapon_cooldowns[weapon] = now + 750 


    def attack_with_sword(self, enemies, souls):
        sword_range = 120  
        sword_damage = 50


        self.attack_visuals.append((
            "rect",
            (self.x + self.width // 2 - sword_range,
            self.y + self.height // 2 - sword_range,
            sword_range * 2,
            sword_range * 2),
            (255, 0, 0)
        ))


        attack_rect = pygame.Rect(
            self.x + self.width // 2 - sword_range,
            self.y + self.height // 2 - sword_range,
            sword_range * 2,
            sword_range * 2
        )


        for enemy in list(enemies):
            enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)
            if attack_rect.colliderect(enemy_rect):
                if enemy.take_damage(sword_damage):
                    soul = enemy.drop_soul()
                    souls.append(soul)
                    enemies.remove(enemy)


    def attack_with_bow(self, enemies, souls):

        bow_damage = 50
        if enemies:
            nearest_enemy = min(enemies, key=lambda e: (e.x - self.x) ** 2 + (e.y - self.y) ** 2)
            self.attack_visuals.append(("line", (self.x + self.width // 2, self.y + self.height // 2, nearest_enemy.x + nearest_enemy.width // 2, nearest_enemy.y + nearest_enemy.height // 2), (0, 0, 255)))
            if nearest_enemy.take_damage(bow_damage):
                soul = nearest_enemy.drop_soul()
                souls.append(soul)
                enemies.remove(nearest_enemy)


    def attack_with_magic_wand(self, enemies, souls):
        wand_damage = 40
        if enemies:
            nearest_enemy = min(enemies, key=lambda e: (e.x - self.x) ** 2 + (e.y - self.y) ** 2)
            self.attack_visuals.append(("circle", (nearest_enemy.x + nearest_enemy.width // 2, nearest_enemy.y + nearest_enemy.height // 2, 30), (128, 0, 128)))
            if nearest_enemy.take_damage(wand_damage):
                soul = nearest_enemy.drop_soul()
                souls.append(soul)
                enemies.remove(nearest_enemy)
            if enemies:
                second_nearest_enemy = min(enemies, key=lambda e: (e.x - self.x) ** 2 + (e.y - self.y) ** 2)
                self.attack_visuals.append(("circle", (second_nearest_enemy.x + second_nearest_enemy.width // 2, second_nearest_enemy.y + second_nearest_enemy.height // 2, 30), (128, 0, 128)))
                if second_nearest_enemy.take_damage(wand_damage):
                    soul = second_nearest_enemy.drop_soul()
                    souls.append(soul)
                    enemies.remove(second_nearest_enemy)


    def attack_with_rock_staff(self, enemies, souls):
        rock_range = 190
        rock_damage = 100
        self.attack_visuals.append(("circle", (self.x + self.width // 2, self.y + self.height // 2, rock_range), (139, 69, 19)))
        for enemy in list(enemies):
            if abs(enemy.x - self.x) <= rock_range and abs(enemy.y - self.y) <= rock_range:
                if enemy.take_damage(rock_damage):
                    soul = enemy.drop_soul()
                    souls.append(soul)
                    enemies.remove(enemy)


    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(surface, (255, 0, 0), (self.x, self.y - 10, self.width, 5))
        pygame.draw.rect(surface, (0, 255, 0), (self.x, self.y - 10, self.width * (self.health / self.settings.player_health), 5))


        for visual in self.attack_visuals:
            if visual[0] == "rect":
                pygame.draw.rect(surface, visual[2], visual[1], 2)
            elif visual[0] == "line":
                pygame.draw.line(surface, visual[2], visual[1][:2], visual[1][2:], 2)
            elif visual[0] == "circle":
                pygame.draw.circle(surface, visual[2], visual[1][:2], visual[1][2], 2)

        self.attack_visuals.clear()



# --------------------- Enemy ---------------------

class Enemy:


    def __init__(self, x, y, speed, color, health=100, damage=10):
        self.width = 50
        self.height = 50
        self.x = x
        self.y = y
        self.speed = speed
        self.color = color
        self.health = health
        self.damage = damage


    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            return True
        return False 
    

    def drop_soul(self):
        return Soul(self.x + self.width // 2, self.y + self.height // 2)


    def update(self, player, enemies):
        if player.x > self.x:
            self.x += self.speed
        if player.x < self.x:
            self.x -= self.speed
        if player.y > self.y:
            self.y += self.speed
        if player.y < self.y:
            self.y -= self.speed

        for other in enemies:
            if other != self and self.collides_with(other):
                self.resolve_collision(other)


    def collides_with(self, other):
        return (
            self.x < other.x + other.width and
            self.x + self.width > other.x and
            self.y < other.y + other.height and
            self.y + self.height > other.y
        )


    def resolve_collision(self, other):
        if self.x < other.x:
            self.x -= self.speed
        else:
            self.x += self.speed
        if self.y < other.y:
            self.y -= self.speed
        else:
            self.y += self.speed


    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))

        health_bar_width = self.width * (self.health / 100)
        health_bar_x = self.x + (self.width - health_bar_width) // 2 

        pygame.draw.rect(surface, (255, 0, 0), (health_bar_x, self.y - 10, health_bar_width, 5))
        pygame.draw.rect(surface, (0, 255, 0), (health_bar_x, self.y - 10, health_bar_width, 5))
    

# --------------------- Soul ---------------------


class Soul:


    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 10
        self.color = (255, 255, 0) 


    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)


    def collides_with(self, player):
        return (
            abs(self.x - (player.x + player.width // 2)) <= self.radius + player.width // 2 and
            abs(self.y - (player.y + player.height // 2)) <= self.radius + player.height // 2
        )


# --------------------- Factories ---------------------


class EnemyFactory:


    def create_enemy(self, world_width, world_height, player):
        raise NotImplementedError

class ZombieFactory(EnemyFactory):


    def create_enemy(self, world_width, world_height, player):
        return EnemySpawner.spawn_outside_view(1.0, (0, 255, 255), world_width, world_height, player, health=150, damage=5)

class SkeletonFactory(EnemyFactory):


    def create_enemy(self, world_width, world_height, player):
        return EnemySpawner.spawn_outside_view(1.5, (255, 255, 255), world_width, world_height, player, health=100, damage=10)

class OrcFactory(EnemyFactory):


    def create_enemy(self, world_width, world_height, player):
        return EnemySpawner.spawn_outside_view(2.0, (0, 0, 255), world_width, world_height, player, health=200, damage=15)

class VampireFactory(EnemyFactory):


    def create_enemy(self, world_width, world_height, player):
        return EnemySpawner.spawn_outside_view(2.5, (255, 0, 255), world_width, world_height, player, health=120, damage=20)

class RandomFactory(EnemyFactory):


    def create_enemy(self, world_width, world_height, player):
        factory = random.choice([ZombieFactory(), SkeletonFactory(), OrcFactory(), VampireFactory()])
        return factory.create_enemy(world_width, world_height, player)


# --------------------- Spawner ---------------------


class EnemySpawner:


    @staticmethod
    def spawn_outside_view(speed, color, world_width, world_height, player, health=100, damage=10):
        margin = 600
        side = random.choice(['top', 'bottom', 'left', 'right'])

        if side == 'top':
            x = random.randint(0, world_width)
            y = random.randint(0, max(0, int(player.y - margin)))
        elif side == 'bottom':
            x = random.randint(0, world_width)
            y = random.randint(min(world_height, int(player.y + margin)), world_height)
        elif side == 'left':
            x = random.randint(0, max(0, int(player.x - margin)))
            y = random.randint(0, world_height)
        else:
            x = random.randint(min(world_width, int(player.x + margin)), world_width)
            y = random.randint(0, world_height)

        return Enemy(x, y, speed, color, health, damage)


# --------------------- Game ---------------------

class Game:


    def __init__(self, settings, screen):
        self.settings = settings
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.internal_width = 1280
        self.internal_height = 720
        self.screen_width, self.screen_height = self.screen.get_size()
        self.world_width = self.internal_width * 2
        self.world_height = self.internal_height * 2
        self.world_surface = pygame.Surface((self.world_width, self.world_height))
        self.font = pygame.font.SysFont("Arial", 36)
        self.reset()


    def reset(self):
        self.settings.reset()
        self.settings.player = Player(self.settings, self.world_width, self.world_height)
        self.enemies = []  
        self.souls = []  
        self.last_spawn_time = 0
        self.spawn_delay = 2000
        self.elapsed_time = 0


    def run(self):
        if not hasattr(self, 'elapsed_time'):
            self.elapsed_time = 0
        start_ticks = pygame.time.get_ticks()

        damage_timer = 0 
        running = True
        while running:
            now = pygame.time.get_ticks()
            elapsed_ms = now - start_ticks + self.elapsed_time
            elapsed_seconds = elapsed_ms // 1000

            if elapsed_seconds >= 300:
                self.display_end_message("You Win!")
                self.settings.souls += len(self.souls)
                self.settings.save()
                self.settings.game_state = "menu"
                self.elapsed_time = 0 
                break

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.settings.game_state = "quit"
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.elapsed_time = elapsed_ms
                    self.settings.game_state = "menu"
                    running = False

            # Update & spawn
            self.spawn_enemies(elapsed_seconds, now)
            self.settings.player.update()
            self.settings.player.attack(self.enemies, now, self.souls)

            # Update enemies and check for collisions
            for e in list(self.enemies):
                e.update(self.settings.player, self.enemies)
                if e.collides_with(self.settings.player):
                    if now - damage_timer >= 1000:
                        self.settings.player.take_damage(e.damage) 
                        damage_timer = now
                if e.health <= 0:
                    soul = e.drop_soul() 
                    self.souls.append(soul) 
                    self.enemies.remove(e)

            # Update souls and check for collection
            for soul in list(self.souls): 
                if soul.collides_with(self.settings.player):
                    self.settings.souls += 1 
                    self.souls.remove(soul)

            # Check if the player's health is 0
            if self.settings.player.health <= 0:
                self.display_end_message("Game Over!")
                self.settings.souls += len(self.souls)
                self.settings.save()
                self.settings.game_state = "menu" 
                self.elapsed_time = 0
                break

            self.draw(elapsed_seconds)

            pygame.display.flip()
            self.clock.tick(self.fps)


    def display_end_message(self, message):
        end_time = pygame.time.get_ticks() + 5000 
        while pygame.time.get_ticks() < end_time:
            self.screen.fill((0, 0, 0)) 
            text_surface = self.font.render(message, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
            self.screen.blit(text_surface, text_rect)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.settings.game_state = "quit"
                    return


    def spawn_enemies(self, elapsed_seconds, now):

        if elapsed_seconds < 180: 
            self.spawn_delay = max(2000, 4000 - elapsed_seconds * 10) 
        else:
            self.spawn_delay = max(500, 2000 - (elapsed_seconds - 180) * 20)

        if now - self.last_spawn_time >= self.spawn_delay:
            self.last_spawn_time = now

            if elapsed_seconds < 60:
                factory = ZombieFactory()
            elif elapsed_seconds < 120:
                factory = SkeletonFactory()
            elif elapsed_seconds < 180:
                factory = OrcFactory()
            elif elapsed_seconds < 240:
                factory = VampireFactory()
            else:
                factory = RandomFactory()

            # Spawn multiple enemies
            for _ in range(5):  # Spawn fewer enemies per batch
                e = factory.create_enemy(self.world_width, self.world_height, self.settings.player)
                self.enemies.append(e)

    def draw(self, elapsed_seconds):
        # World
        self.world_surface.fill((30, 30, 30))
        for e in self.enemies:
            e.draw(self.world_surface)
        for soul in self.souls:
            soul.draw(self.world_surface)
        self.settings.player.draw(self.world_surface)

        # Draw map borders
        border_color = (255, 255, 255)
        border_thickness = 5
        pygame.draw.rect(
            self.world_surface,
            border_color,
            (0, 0, self.world_width, self.world_height),
            border_thickness
        )

        # Camera
        cam_x = max(0, min(self.settings.player.x - self.screen_width // 2,
                            self.world_width - self.screen_width))
        cam_y = max(0, min(self.settings.player.y - self.screen_height // 2,
                            self.world_height - self.screen_height))
        view = pygame.Rect(cam_x, cam_y, self.screen_width, self.screen_height)
        scaled = pygame.transform.scale(self.world_surface.subsurface(view),
                                        (self.screen_width, self.screen_height))
        self.screen.blit(scaled, (0, 0))

        # Timer and soul count
        minutes = elapsed_seconds // 60
        seconds = elapsed_seconds % 60
        txt = f"{minutes:02}:{seconds:02} | Souls: {self.settings.souls}"
        surf = self.font.render(txt, True, (255, 255, 255))
        rect = surf.get_rect(center=(self.screen_width // 2, 30))
        self.screen.blit(surf, rect)