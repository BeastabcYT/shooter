from pygame import*
from random import randint 
from time import time as timer

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale( image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        case = key.get_pressed()
        if case[K_LEFT] and self.rect.x > 5 :
            self.rect.x -= self.speed
        if case[K_RIGHT] and self.rect.x < 620:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet("bullet.png",self.rect.centerx,self.rect.top,5,20,25)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(5,620)
            global lost
            lost = lost + 1 
class Bullet(GameSprite):
    def update(self):
        self.rect.y = self.rect.y - self.speed
        if self.rect.y < 0 :
            self.kill()
bullets = sprite.Group()




enemys = sprite.Group()
for i in range(5):
    enemy = Enemy("ufo.png",randint(5,620),-40,80,50,randint(1,5))
    enemys.add(enemy)



rocket = Player("rocket.png",150,400,80,100,10)


window = display.set_mode((700,500))
bg = transform.scale(image.load("bg.jpg"),(700,500))
clock = time.Clock()
finish = False

font.init()
myfont = font.Font(None,35)
lost = 0


mixer.init()
mixer.music.load("bgmu.mp3")
mixer.music.play()
fire = mixer.Sound("musho.mp3")
score = 0

myfont2 = font.Font(None,80)
win = myfont2.render("You Win",True,(0,250,0))
lose = myfont2.render("You lose",True,(250,0,0))
life = 3

numberfire  = 0
reload = False



game = True
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if numberfire < 5 and reload == False:
                    numberfire += 1
                    rocket.fire()
                    fire.play()
                if numberfire >= 5 and reload == False:
                    reload = True
                    startreloadtime = timer()

    if not finish:
        window.blit(bg,(0,0))
        enemys.update()
        enemys.draw(window)
        rocket.draw()
        rocket.update()
        bullets.draw(window)
        bullets.update()
        if reload == True:
            now_time = timer()
            if now_time - startreloadtime < 3:
                reloadtext = myfont2.render("reload...",True,(155,0,0))
                window.blit(reloadtext,(260,460))
            else:
                reload = False
                numberfire = 0
       
        if sprite.spritecollide(rocket,enemys,True):
            life = life - 1
        if lost >= 5 or life == 0 :
            finish = True
            window.blit(lose,(240,200))
        kille_enemys = sprite.groupcollide(bullets,enemys,True,True)
        for a in kille_enemys:
            score = score + 1
            enemy = Enemy("ufo.png",randint(0,620),-40,80,50,randint(1,5))
            enemys.add(enemy)
        if score >= 10:
            finish = True
            window.blit(win,(240,200))
        textlife = myfont.render("Хп:"+ str(life),True,(255,255,255)) 
        text_lost = myfont.render("пропущено:"+ str(lost),True,(255,255,255))
        text_score = myfont.render("рахунок:"+ str(score),True,(255,255,255)) 
        window.blit(text_score,(10,50))
        window.blit(text_lost,(10,20)) 
        window.blit(textlife,(620,15))
        display.update()
    else:
        finish =  False
        lost = 0
        score = 0
        life = 3
        for b in bullets:
            b.kill()
        for d in enemys:
            d.kill()
        time.delay(3000)
        for i in range(5):
            enemy = Enemy("ufo.png",randint(5,620),-40,80,50,randint(1,5))
            enemys.add(enemy)
        numberfire = 0
    clock.tick(50)