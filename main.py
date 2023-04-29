"""Імпорта"""
from pygame import*# імпорт пайгейма

init()# ініціалізуєм пайгейм

level1 = [
    "r                                                                    .",# так виглядає
    "r                                                                    .",# рівень кожен 
    "r                                                                    .",# символ 
    "r                                                                    .",# відповідає за
    "rr    °  °      l                             r    °  °  °     l     .",# свій обєкт
    "r  ------------                                ---------------       .",
    "rr / l                                       r / l         r / l     .",
    "rr   l                                       r   l         r   l     .",
    "rr     °  l                       r     °  °     l   r         l     .",
    "r  ------                           ------------       -------       .",
    "r     r / l                                          r / l           .",
    "r     r   l                                          r   l           .",
    "r     r       °  °   l                       r   °  °    l           .",
    "r       ------------                           ---------             .",
    "r                r / l                       r / l                   .",
    "r                r   l                       r   l                   .",
    "r                                                                    .",
    "----------------------------------------------------------------------"]# 
"""Картинки щоб швидше вставляти бо по іншому довго"""
hero_l = "images/sprite1.png"
hero_r = "images/sprite1_r.png"

enemy_l = "images/cyborg.png"
enemy_r = "images/cyborg_r.png"

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
        pass


    def u_d(self):# переміщення верх вниз
        pass

class Enemy(Settings):# створюєм клас ворога з спадкуванням у сетінг
    def __init__(self, x, y, width, height, speed, img, side):# створюєм новий ініт 
        Settings.__init__(self, x, y, width, height, speed, img)#все зминулого сетінга переносим
        self.side = side#і ддаєм 

    def update():# функція руху
        pass
    
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
    pass


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
    global items, camera# робимо глобальними змінни
    camera = Camera(camera_config, level1_width, level1_height)# створюєма наблюдателя
    items = sprite.Group()#  створюємо тусу
    block_r = []# список 1:
    block_l = []# список 2:
    plat = []# список 3:
    coins = []# список 4:
    stairs_lst = []# список 6:
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
            x += 40#  ікси плюс 40
        y += 40#  перміщаємось в низ
        x = 0#  ікси 0


def lvl_1():# 1 рівень початок
    game = True# зміна для початку / кінця гри
    while game:#  вайл живиться зміной гейм поки вона тру
        for e in event.get():#  перевіряєм події
            if e.type == QUIT:#  якщо це подія червоний хрестик нажатий
                game = False# то все живитись циклу нічим гейм стає фалсе

        for i in items:#  ходим по групі
            window.blit(i.image, camera.apply(i))#  показуєм обєкти які в полі зору











        display.update()#  оновлюємо вікно



def lvl1_end():# кінець
    pass

start_pos()#  запускаєм дві функції
lvl_1()