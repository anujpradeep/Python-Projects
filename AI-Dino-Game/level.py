import pygame
from common import *


class Level():
    def __init__(self, screen):
        self.screen: pygame.Surface = screen
        self.bgx = 0
        self.score = 0
        self.score_counter = 0

    def rotate(self):
        self.bgx -= 1
        if self.bgx <= -640:
            self.bgx = 0

    def get_score(self):
        if self.score_counter >= MAX_FRAMES:
            self.score += 1
            self.score_counter = 0
        else:
            self.score_counter += 1

    def frame(self):
        self.screen.fill('white')
        pygame.draw.line(self.screen, 'black', (0, 380), (WIDTH, 380), 3)

        self.get_score()

        render_texts(self.screen, ['Score : ' + str(self.score)], 'centurygothic',
                                 32, (0, 0, 0), (255, 255, 255), "top_right", 1)
