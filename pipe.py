import random

class Pipe:

    def __init__(self, startX, img):

        self.ecart = 180
        self.scored = False

        self.img = img
        self.rect = self.img.get_rect()
        posX = startX
        posY = random.randint(self.ecart + 50, 700)
        self.rect.topleft = (posX, posY)

        self.rect_2 = self.img.get_rect()
        self.rect_2.topleft = (posX, posY - self.ecart - 800)
    
    def update(self, level_speed):

        if self.rect.x <= -100:

            self.rect.y = random.randint(self.ecart + 50, 600)
            self.rect_2.y = self.rect.y - self.ecart - 800

            self.rect.x = 1500
            self.rect_2.x = 1500
            self.scored = False

        else: 
            self.rect.x -= level_speed
            self.rect_2.x -= level_speed
