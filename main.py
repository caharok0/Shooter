from pygame import*
from random import randint

init()

W, H = 500, 700
FPS = 60

mixer.init()
mixer.music.load("sounds/space.ogg")
mixer.music.set_volume(0.9)
mixer.music.play()

fire_snd = mixer.Sound("sounds/fire.ogg")

font.init()
font1 = font.SysFont("fonts/Bebas_Neue_Cyrillic.ttf", 35, bold=True)
font2 = font.SysFont("fonts/Bebas_Neue_Cyrillic.ttf", 100, bold=True)


window = display.set_mode((W,H))
display.set_caption("Shooter")

bg = transform.scale(image.load("images/1669981801_1-kartinkin-net-p-fon-dlya-prezentatsii-goluboe-nebo-vkontak-1.jpg"), (W, H))

clock = time.Clock()

class GameSprite(sprite.Sprite):
    def __init__(self, x, y, widht, height, speed, ing):
        super().__init__()
        self.widht = widht
        self.height = height
        self.speed = speed
        self.image = transform.scale(image.load(ing), (widht, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def move(self):
        global killed
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < W - self.widht:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(self.rect.centerx, self.rect.top, 15, 20, 20, "images/bullet.png")
        bullets.add(bullet)

    #max_FPS = 100  
    #def on_enemy_killed():
        #global FPS
        #if FPS < max_FPS:
            #FPS*= 1.5
            #print(f"новий FPS: {FPS}")
        #else:
            #print("FPS досяг максимального значення")


class Enemy(GameSprite):
    def update(self):
        global skipped
        self.rect.y += self.speed
        if self.rect.y > H - self.height:
            self.rect.x = randint(0, W - self.widht)
            self.rect.y = 0
            skipped += 1

class Asteroid(GameSprite):
    def __init__(self, x, y, widht, height, speed, ing):
        super().__init__(x, y, widht, height, speed, ing)
        self.angle = 0
        self.original_image = self.image


    def update(self):
        self.rect.y += self.speed
        self.angle = (self.angle + 2.5) % 360
        self.image = transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        if self.rect.y > H - self.height:
            self.rect.x = randint(0, W - self.widht)
            self.rect.y = 0

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

class Buff(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > H - self.height:
            self.rect.x = randint(0, W - self.widht)
            self.rect.y = -100

player = Player(W / 2, H - 100, 50, 100, 5, "images/roket-removebg-preview.png")
life_boost = Buff(randint(0, W - 50), -100, 50, 50, randint(2, 5), "images/life.png")
bullets_boost = Buff(randint(0, W - 50), -100, 50, 50, randint(2, 5), "images/ammo.png")
enemies = sprite.Group()
for i in range(5):
    enemy = Enemy(randint(0, W - 70), randint(-35, 10), 70, 35, randint(1, 3), "images/pranuk.png")
    enemies.add(enemy)

asteroids = sprite.Group()
for i in range(3):
    asteroid = Asteroid(randint(0, W - 70), randint(-35, 10), 70, 35, randint(1, 3), "images/pelmen.png")
    asteroids.add(asteroid)

bullets = sprite.Group()

life = 3
killed = 0
skipped = 0
shoot_count = 30
game = True
finish = False
while game:
    for e in event.get():
        if e.type ==QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if shoot_count > 0:
                    fire_snd.play()
                    player.fire()
                    shoot_count -= 1
                
            if e.key == K_ESCAPE:
                finish = False
    if not finish:
        window.blit(bg, (0,0))
        player.draw()
        player.move()

        enemies.draw(window)
        enemies.update()

        asteroids.draw(window)
        asteroids.update()

        bullets.draw(window)
        bullets.update()

        life_boost.draw()
        life_boost.update()

        bullets_boost.draw()
        bullets_boost.update()
        #зіткнення куль з ворогами
        if sprite.groupcollide(bullets, enemies, True, True):
            killed += 1
            enemy = Enemy(randint(0, W - 70), randint(-35, 10), 70, 35, randint(1, 3), "images/pranuk.png")
            enemies.add(enemy)
        #зіткнення куль з ботами
        if sprite.groupcollide(bullets, asteroids, True, False):
            pass
        #зіткнення гравця з астеройдами
        if sprite.spritecollide(player, asteroids, True):
            life -= 1
            asteroid = Asteroid(randint(0, W - 70), randint(-35, 10), 70, 35, randint(1, 3), "images/pelmen.png")
            asteroids.add(asteroid)
        #зіткнення гравця з ворогами
        if sprite.spritecollide(player, enemies, True):
            life -= 1
            enemy = Enemy(randint(0, W - 70), randint(-35, 10), 70, 35, randint(1, 3), "images/pelmen.png")
            enemies.add(enemy)

        if life == 0:
            finish = True
            mixer.music.stop()

        skipped_txt = font1.render(f"пропущєно: {skipped}", True, (255, 255, 255,))
        window.blit(skipped_txt, (10, 10))

        killed_txt = font1.render(f"вбито: {killed}", True, (255, 255, 255,))
        window.blit(killed_txt, (10, 75))

        life_txt = font2.render(str(life), True, (0, 255, 0,))
        window.blit(life_txt, (W-50, 10))

        bullets_txt = font1.render(f"кількість куль: {shoot_count}", True, (0, 0, 0,))
        window.blit(bullets_txt, (10, 95))
    else:
        life = 3
        skipped = 0
        killed = 0
        shoot_count = 30
        for enemy in enemies:
            enemy.kill()
        for asteroid in asteroids:
            asteroid.kill()
        for bulet in bullets:
            bullets.kill()
        for i in range(5):
            enemy = Enemy(randint(0, W - 70), randint(-35, 10), 70, 35, randint(1, 3), "images/pranuk.png")
            enemies.add(enemy)

        for i in range(3):
            asteroid = Asteroid(randint(0, W - 70), randint(-35, 10), 70, 35, randint(1, 3), "images/pelmen.png")
            asteroids.add(asteroid)


    display.update()
    clock.tick(FPS)

