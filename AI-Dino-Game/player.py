import pygame
from common import *

class Player():
    def __init__(self, screen):
        self.side = False
        self.down = False
        self.up = True
        self.in_air = False
        self.side_counter = 0
        self.x = 50
        self.gravity = 1
        self.jumpcount = 0
        self.screen: pygame.Surface = screen

        image_left = pygame.image.load('data/dino_left_1.png')
        image_right = pygame.image.load('data/dino_right_2.png')
        image_jump = pygame.image.load('data/dino_jump_1.png')
        image_down_1 = pygame.image.load('data/dino_down_1.png')
        image_down_2 = pygame.image.load('data/dino_down_2.png')

        image_left = pygame.transform.scale(
            image_left, (WIDTH // 10, HEIGHT//5))

        image_right = pygame.transform.scale(
            image_right, (WIDTH // 10, HEIGHT//5))

        image_jump = pygame.transform.scale(
            image_jump, (WIDTH // 10, HEIGHT//5))

        image_down_1 = pygame.transform.scale(
            image_down_1, (WIDTH // 7, HEIGHT//8))

        image_down_2 = pygame.transform.scale(
            image_down_2, (WIDTH // 7, HEIGHT//8))

        rect_left = image_left.get_rect()
        rect_right = image_right.get_rect()
        rect_jump = image_jump.get_rect()
        rect_down_1 = image_down_1.get_rect()
        rect_down_2 = image_down_2.get_rect()

        self.standing_y = 380 - rect_left.height
        self.down_y = 380 - rect_down_1.height

        self.y = self.standing_y

        self.images = [image_left, image_right,
                       image_jump, image_down_1, image_down_2]
        self.rects = [rect_left, rect_right,
                      rect_jump, rect_down_1, rect_down_2]

    def apply_gravity(self):
        if self.y < self.standing_y:
            self.y += self.gravity

    def can_jump(self):
        if not self.in_air:
            self.in_air = True
            self.y = self.standing_y
            self.down = False

    def jumping(self):
        if self.in_air:  # in the air
            if self.up:  # left side of the jump
                self.y -= 4
                self.jumpcount += 1
                if self.jumpcount > 70:
                    self.jumpcount = 0
                    self.up = False
            else:  # right side of the jump
                if self.y == self.standing_y:
                    self.in_air = False
                    self.up = True

    def get_image(self):
        index = 2 # index for jumping sprite 
        if not self.in_air:
            if self.down:
                if self.side:
                    index = 3
                else:
                    index = 4
                self.y = self.down_y
            else:
                if self.side:
                    index = 0
                else:
                    index = 1
                self.y = self.standing_y

        return self.screen.blit(self.images[index], (50, self.y))

    def switch_side(self):
        if self.side_counter >= MAX_FRAMES and not self.in_air:
            self.side_counter = 0
            self.side = not self.side
        else:
            self.side_counter += 1

    def frame(self):
        self.switch_side()

        p_rect = self.get_image()

        self.jumping()

        self.apply_gravity()

        return p_rect
