import pygame

class Bird:

    def __init__(self, img, posX, posY=300):
        self.jump = False
        self.vel_time = 0
        self.jump_time = 0
        self.score = 0
        self.img = img
        self.rect = self.img.get_rect()
        self.rect.topleft = (posX, posY)
        
    def update(self):

        if self.jump and self.jump_time <= 4:
            velocity = -10
            self.jump_time += 1

        elif self.jump:
            self.jump_time = 0
            self.jump = False
            self.vel_time = 0.0

        if not self.jump:

            velocity = (0.75*9.81*self.vel_time)**2
            self.vel_time += 1/60
        
        self.rect.y += velocity
