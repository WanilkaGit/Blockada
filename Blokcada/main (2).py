"""Імпорта"""
import time

from pygame import*# імпорт пайгейма

init()# ініціалізуєм пайгейм
"""ОСЬ ТУТ ПРОМАЛЬОВУЄТЬСЯ РІВЕНЬ"""
level1 = [
    "r                                                                    .",# так виглядає
    "r                                                                    .",# рівень кожен 
    "r                                                                    .",# символ 
    "r                                                                    .",# відповідає за
    "rr  e °  °  k   l                             re   °  °  °     l     .",# свій обєкт
    "r  ------------                                ---------------       .",
    "rr / l                                       r / l         r / l     .",
    "rr   l                                       r   l         r   l     .",
    "rr     °m l                       r ec  °  °     l   r         l     .",
    "r  ------                           ------------       -------       .",
    "r     r / l                                          r / l           .",
    "r     r   l                                          r   l           .",
    "r     r    °  °  ° m l                       r e °  °    l           .",
    "r       ------------                           ---------             .",
    "r                r / l                       r / l                   .",
    "r             g   r   l         d             r   l                   .",
    "r                                                                    .",
    "----------------------------------------------------------------------"]# 
"""Картинки щоб швидше вставляти бо по іншому довго"""
hero_r = "images/hero_r.png"
hero_l = "images/hero_l.png"

enemy_l = "images/enemy_l.png"
enemy_r = "images/enemy_r.png"

coin_img = "images/coin.png"
door_img = "images/door.png"
key_img = "images/key.png"
chest_open = "images/cst_open.png"
chest_close = "images/cst_close.png"
stairs = "images/stair.png"
portal_img = "images/portal.png"
platform = "images/platform.png"
power = "images/mana.png"
nothing = "images/nothing.png"
boss = "images/nothing.png"

h_m_c = 0
font1 = font.SysFont("Arial", 35)
font2 = font.SysFont(('font/ariblk.ttf'), 60)
e_tap = font2.render('press (e)', True, (255, 0, 255))
k_need = font2.render('You need a key to open!', True, (255, 0, 255))
space = font2.render('press (space) to kill the enemy', True, (255, 0, 255))


# це те скільки вийде блоків на екрані 40 кількість пікселів на оин силвол
level1_width = len(level1[0]) * 40
level1_height = len(level1) * 40

#розміри екрану
W = 1280
H = 720

# створюєм вікно
window = display.set_mode((W, H))

# Все для вікна
back = transform.scale(image.load("images/bgr.png"), (W, H))# фон
display.set_caption("Лошок")# назва
display.set_icon(image.load("images/key.png"))# картинка біля назви

"""Класи"""
class Settings(sprite.Sprite):# основний клас тут основні параметри
    def __init__(self, x, y, width, height, speed, img):
        super().__init__()
        self.width = width
        self.height = height
        self.speed = speed
        self.image = transform.scale(image.load(img), (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):# тут прописана функція ресет
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(Settings):# клас гравця з супер класом сетінгс
    def r_l(self):# тут буде переміщення в право ліво
        global mana
        key_pressed = key.get_pressed()# задаєм в зміну значення
        if key_pressed[K_a]:# перевіряєм чи нажата кнопка це а
            self.rect.x -= self.speed# якщо так той демо в ліво
            self.image = transform.scale(image.load(hero_l), (self.width, self.height))# підсьтавляєм фотку
            mana.side = "left"
        if key_pressed[K_d]:#кнопка в низ натиснута
            self.rect.x += self.speed# х додаєм швидкість рухаємось
            self.image = transform.scale(image.load(hero_r), (self.width, self.height))#  підставляєм фотку
            mana.side = "right"



    def u_d(self):# переміщення верх вниз
        key_pressed = key.get_pressed()#  підключаєм список натиснутих клавіш
        if key_pressed[K_s]:# якщо в низ тобто в низ
            self.rect.y += self.speed# ми додає тобто спускаємось
        if key_pressed[K_w]:# якщо в верх то віднімаєм піднімаємось
            self.rect.y -= self.speed# 

class Enemy(Settings):# створюєм клас ворога з спадкуванням у сетінг
    def __init__(self, x, y, width, height, speed, img, side):# створюєм новий ініт 
        Settings.__init__(self, x, y, width, height, speed, img)#все зминулого сетінга переносим
        self.side = side#і ддаєм 

    def update(self):# функція руху
        global side

        if self.side == "left":
            self.rect.x -= self.speed

        if self.side == "right":
            self.rect.x += self.speed
class Mana(Enemy):
    pass

mana = Mana(0, -100, 25, 25, 20, power, "left")
    
class Camera(object):# клас камери коли ми ходимо камера перемііщається з нами
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)
    
    def apply(self, target):
        return target.rect.move(self.state.topleft)
    
    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)
        
def camera_config(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l + W / 2, -t + H / 2
    
    l = min(0, l)  # Не виходимо за ліву межу
    l = max(-(camera.width - W), l)  # Не виходимо за праву межу
    t = max(-(camera.height - H), t)  # Не виходимо за нижню межу
    t = min(0, t)  # Не виходимо за верхню межу
    
    return Rect(l, t, w, h)

"""Функції"""

def collides():# доторкання
    global open_ch, h_m_c
    global open_d
    key_pressed = key.get_pressed()
    for s in stairs_lst:# тут перевіряєм зіткнення гравця з сходами
        if sprite.collide_rect(hero, s):#  якщо зіткнулися то
            hero.u_d()#  ходим в верх в низ
            if hero.rect.y < s.rect.y - 40:#  
                hero.rect.y = s.rect.y - 40
            if hero.rect.y > s.rect.y + 130:
                hero.rect.y = s.rect.y + 130

    for l in block_l:
        if sprite.collide_rect(hero, l):
            hero.rect.x = hero.rect.x - hero.width
        for e in enemy_lst:
            if sprite.collide_rect(e, l):
                e.side = "left"
                e.image = transform.scale(image.load(enemy_l), (e.width, e.height))
        sprite.spritecollide(l, manas, True,)
    for r in block_r:
        if sprite.collide_rect(hero, r):
            hero.rect.x = hero.rect.x + hero.width
        for e in enemy_lst:
            if sprite.collide_rect(e, r):
                e.side = "right"
                e.image = transform.scale(image.load(enemy_r), (e.width, e.height))
        sprite.spritecollide(l, manas, True)

    for e in enemy_lst:
        sprite.spritecollide(e, manas, True)
        items.remove(mana)
        e.rect.y = -100
        items.remove(e)

    if sprite.collide_rect(hero, p6):
        window.blit(e_tap, (450, 50))
        if key_pressed[K_e]:
            items.remove(p6)
            p6.rect.y = -100
            open_ch = True
    
    if sprite.collide_rect(hero, p11):
        window.blit(e_tap, (500, 50))
        if key_pressed[K_e]:
            items.remove(p11)
            p11.rect.y = -100

    if sprite.collide_rect(hero, p7) and open_ch == False:
        window.blit(k_need, (450, 50))

    if sprite.collide_rect(hero, p7) and open_ch == True:
        window.blit(e_tap, (450, 50))
        if key_pressed[K_e]:
            # p7.rect.x = -200
            p7.image = transform.scale(image.load(chest_open), (p7.width, p7.height))
            open_d = True
    
    if sprite.collide_rect(hero, door) and open_d == False:
        hero.rect.x = door.rect.x - hero.width
        window.blit(k_need, (450, 50))

    if sprite.collide_rect(hero, door) and open_d == True:
        hero.rect.x = door.rect.x - hero.width
        window.blit(e_tap, (450, 50))
        if key_pressed[K_e]:
            door.rect.x = -200
            # open_d = True
        
    for coin in coins:
        if sprite.collide_rect(hero, coin):
            h_m_c += 1
            items.remove(coin)
            coin.rect.y = -100

    if key_pressed[K_SPACE]:
        mana.rect.x = hero.rect.centerx
        mana.rect.y = hero.rect.top
        items.add(mana)
        manas.add(mana)

    
            



def menu():# кнопка меню
    pass


def rules():# правила гри
    pass


def pause():# пауза
    pass


def restart():# рестарт
    pass


x = 0
y = 0
def start_pos():# стартова позиція
    global items, camera, hero, block_r, block_l, plat, coins, door, coin
    global stairs_lst, enemy_lst, p6, p11, p7, p8, open_d, open_ch, manas# робимо глобальними змінни
    hero = Player(300, 650, 50, 50 , 15, hero_l)
    camera = Camera(camera_config, level1_width, level1_height)# створюєма наблюдателя
    
    items = sprite.Group()#  створюємо тусу
    manas = sprite.Group()

    open_d = False
    open_ch = False


    block_r = []# список 1:
    block_l = []# список 2:
    plat = []# список 3:
    coins = []# список 4:
    stairs_lst = []# список 6:
    enemy_lst = []# список 10:
    # всі списки дивіться в кінотеатрах(коді)
    x = 0#  координати для обєктів
    y = 0
    for r in level1:# фор як раб почав ходити по списками перевіряєм індекси
        for c in r:#  стучим в двері перевіряєм чи
            if c == "-":# дім полу
                p1 = Settings(x,y, 40, 40, 0, platform)# створюєм раба платформа
                plat.append(p1)# 
                items.add(p1)
            if c == "l":# дім "далі ходу нема"
                p2 = Settings(x,y, 40, 40, 0, nothing)#  повітря
                block_l.append(p2)# вони сидять на двух стулах список
                items.add(p2)# туса/група
            if c == "r":#  дім "далі ходу тож нема"
                p3 = Settings(x,y, 40, 40, 0, nothing)#  повітря
                block_r.append(p3)#в ходять в спи
                items.add(p3)# в туси/групи
            if c == "°":# дім бабла
                p4 = Settings(x,y, 40, 40, 0, coin_img)#  бабла/грошей
                coins.append(p4)#в ходять в спи
                items.add(p4)# в туси/групи
            if c == "/":# дім рабів пояких мона ходить
                p5 = Settings(x, y - 40, 40, 180, 0, stairs)# сходів
                stairs_lst.append(p5)#в ходять в спи
                items.add(p5)# в туси/групи
            if c == "k":
                p6 = Settings(x,y + 20, 40, 20, 0, key_img)#  ключа
                items.add(p6)
            if c == "g":
                p7 = Settings(x,y + 20, 80, 60, 0, chest_close)#  ключа
                items.add(p7)
            if c == "d":
                door = Settings(x,y, 40, 80, 0, door_img)#  ключа
                items.add(door)
            if c  == "e":
                p9 = Enemy(x,y, 40, 40, 20, enemy_r, "right")
                enemy_lst.append(p9)
                items.add(p9)
            if c  == "m":
                p10 = Enemy(x,y, 40, 40, 20, enemy_l, "left")
                enemy_lst.append(p10)
                items.add(p10)
            if c == "c":
                p11 = Settings(x,y + 20, 40, 20, 0, key_img)#  ключа
                items.add(p11)
            x += 40#  ікси плюс 40
        y += 40#  перміщаємось в низ
        x = 0#  ікси 0
    items.add(hero)


def lvl_1():# 1 рівень початок
    global h_m_c, h_m_c_t
    game = True# зміна для початку / кінця гри
    while game:#  вайл живиться зміной гейм поки вона тру
        h_m_c_t = font1.render(str(h_m_c), True, (0, 0, 0))
        time.delay(5)
        window.blit(back,(0, 0))
        for e in event.get():#  перевіряєм події
            if e.type == QUIT:#  якщо це подія червоний хрестик нажатий
                game = False# то все живитись циклу нічим гейм стає фалсе
        hero.r_l()
        mana.update()
        for e in enemy_lst:
            e.update()
        collides()
        camera.update(hero)
        for i in items:#  ходим по групі
            window.blit(i.image, camera.apply(i))#  показуєм обєкти які в полі зору
        window.blit(h_m_c_t, (60, 10))
        window.blit(transform.scale(image.load(coin_img), (40, 40)), (10, 10))
        











        display.update()#  оновлюємо вікно



def lvl1_end():# кінець
    pass

start_pos()#  запускаєм дві функції
lvl_1()