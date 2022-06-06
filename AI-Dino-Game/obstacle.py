import pygame
import random
from common import *


class Obstacle():

    def __init__(self, screen):
        self.screen: pygame.Surface = screen
        self.index = random.randint(0, 3)

        # 0 - Cactus, 1 - Tall Cactus, 2 - 2 Stacked Cactus, 3 - 3 Stacked Cactus
        self.obstacle_choices = ['1_cactus',
                                 'tall_cactus', '2_cactus', '3_cactus']

        if self.index == 1:
            image = pygame.image.load('data/tall_cactus.png')
            self.image = pygame.transform.scale(
                image, (image.get_width() * 1.2, image.get_height() * 1.1))
        else:
            self.image = pygame.transform.rotozoom(pygame.image.load(
                'data/' + self.obstacle_choices[self.index] + '.png'), 0, 0.8)

        self.rect = self.image.get_rect()

        self.x = random.randint(750, 800)

        if self.index == 1:
            self.y = 280
            self.speed = 2
        else:
            self.y = 307
            self.speed = 2

    def frame(self):
        self.x -= self.speed
        o_rect = self.screen.blit(self.image, (self.x, self.y))
        return o_rect
