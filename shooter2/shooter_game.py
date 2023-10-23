#Создай собственный Шутер!
from random import randint
from pygame import *


# создай окно игры
window = display.set_mode((700, 500))
display.set_caption("Шутер")
background = transform.scale(image.load("galaxy.jpg"), (700, 500))


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, widht, height, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (widht, height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < 595:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 30, 30, -15 )
        bullets.add(bullet)


class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()



lost = 0 

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y >= 600:
            self.rect.y = 0 
            self.rect.x = randint(10, 700)
            lost = lost + 1

bullets = sprite.Group()


clock = time.Clock()
FPS = 60
run = True
finish = False

points = 0


mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

fire_sound = mixer.Sound('fire.ogg')



font.init()
font = font.Font(None, 30)




player_image = "rocket.png"
enemy_image = "ufo.png"

hero = Player(player_image, 100, 420, 70, 70, 5)


win = font.render(
    'YOU WIN', True, (255, 255, 255)
)

lose = font.render(
    'YOU LOSE, иди тренируйся', True, (255, 255, 255)
)



enemys = sprite.Group()
for i in range(1, 6):
    enemy = Enemy(enemy_image,randint(10, 400), -40, 50, 50, randint(1, 5))
    enemys.add(enemy)


while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                hero.fire()
                fire_sound.play()



    if finish != True:  
        window.blit(background,(0, 0))
        hero.reset()  
        hero.update()
        enemys.update() 

        enemys.draw(window)

        bullets.update()
        bullets.draw(window)

        text_lose = font.render("Пропущено:" + str(lost), 1, (225, 225, 225))
        text_points = font.render("Счет" + str(points), 1, (225, 225, 225))
        window.blit(text_lose, (10, 50))
        window.blit(text_points, (10, 20))

        sprite_list = sprite.groupcollide(
            bullets, enemys, True, True
        )

        for i in sprite_list:
            points += 1
            enemy = Enemy(enemy_image,randint(10, 400), -40, 50, 50, randint(1, 5))
            enemys.add(enemy)

        if lost >= 3 or sprite.spritecollide(hero, enemys, False):
            finish = True
            window.blit(lose, (200, 200))

        if points >= 10:
            finish = True
            window.blit(win, (300, 200))

        

        
         
        
    




    display.update()
    clock.tick(FPS)