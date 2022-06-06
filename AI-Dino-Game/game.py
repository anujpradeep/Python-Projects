import pickle
import pygame
import os
import neat

from level import Level
from obstacle import Obstacle
from player import Player
from common import *

max_score = 0
current_gen = 0
pscore = 0


def game():

    level = Level(screen)

    player = Player(screen)

    obstacles = [Obstacle(screen)]

    clock = pygame.time.Clock()
    while 1:
        clock.tick(240)
        level.frame()
        p_rect: pygame.Rect = player.frame()
        for obstacle in obstacles:
            o_rect = obstacle.frame()
            if obstacle.x - 30 <= player.x and len(obstacles) <= 1:
                obstacles.append(Obstacle(screen))

            if obstacle.x < -(obstacle.rect.bottomright[0] - obstacle.rect.bottomleft[0]):
                obstacles.remove(obstacle)

            if p_rect.colliderect(o_rect):
                return level.score

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.can_jump()
                if event.key == pygame.K_DOWN:
                    player.down = True


def menu():
    prev_score = -1

    global max_score, current_gen

    standing_dino = Player(screen)

    while 1:
        screen.fill('white')
        pygame.draw.line(screen, 'black', (0, 380), (WIDTH, 380), 3)

        render_texts(screen, ['Press SPACE to begin playing', "R-CTRL to train AI"],
                     'centurygothic', 32, (0, 0, 0), (255, 255, 255), "center", 2)
        if prev_score > -1:
            render_texts(screen, ['Previous Score : ' + str(prev_score)],
                         'centurygothic', 32, (0, 0, 0), (255, 255, 255), "top_left", 1)

        screen.blit(
            standing_dino.images[2], (50, standing_dino.y))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    prev_score = game()
                if event.key == pygame.K_RCTRL:
                    run()
                    max_score = 0
                    current_gen = 0


def eval_genomes(genomes : neat.DefaultGenome, config):
    nets: list[neat.nn.FeedForwardNetwork] = []
    dinos: list[Player] = []
    ge: list[neat.DefaultGenome] = []
    global current_gen, max_score, pscore

    current_gen += 1

    for _, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        dinos.append(Player(screen))
        genome.fitness = 0
        ge.append(genome)

    level = Level(screen)
    obstacles = [Obstacle(screen)]

    run = True
    clock = pygame.time.Clock()
    while run and len(dinos) > 0:
        clock.tick(240)
        level.frame()

        render_texts(screen, ['Pervious Gen Score : ' + str(pscore), 'Max score : ' + str(max_score)],
                     'centurygothic', 32, (0, 0, 0), (255, 255, 255), "top_left", 2)

        render_texts(screen, ["ESCAPE to end this gen"],
                     'centurygothic', 32, (255, 0, 0), (255, 255, 255), "bottom_right", 2)

        if len(obstacles) <= 1:
            if obstacles[0].x - 30 < 50:
                obstacles.append(Obstacle(screen))

        for obs in obstacles:
            o_rect = obs.frame()
            if obs.x < -(obs.rect.bottomright[0] - obs.rect.bottomleft[0]):
                obstacles.remove(obs)
            for i, dino in enumerate(dinos):
                p_rect = dino.frame()
                if p_rect.colliderect(o_rect):
                    ge[i].fitness -= 3
                    nets.pop(i)
                    ge.pop(i)
                    dinos.pop(i)

        for i, dino in enumerate(dinos):

            ge[i].fitness += 0.05

            output = nets[dinos.index(dino)].activate(
                (
                    dino.x,
                    dino.y,
                    obstacles[0].x,
                    obstacles[0].y,
                    obstacles[0].index,
                    obstacles[0].speed
                )
            )

            if output[0] > 0.5:
                dino.can_jump()

        if level.score >= 50:
            if len(dinos) > 0:
                pickle.dump(nets[0], open(
                    "best_pickles/best.pickle_" + str(current_gen), "wb"))

        render_texts(screen, ['Generation ' + str(current_gen), 'Alive ' + str(len(dinos))],
                     'centurygothic', 32, (0, 0, 0), (255, 255, 255), "bottom_left", 2)

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    break

    pscore = level.score
    if max_score < level.score:
        max_score = pscore


def run():
    local_dir = os.path.dirname(__file__)
    config_file = os.path.join(local_dir, 'config.txt')

    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation, config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Run for up to 50 generations.
    winner = p.run(eval_genomes, 50)

    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))


def main():
    # Initialise screen
    pygame.init()

    global screen

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Dino Game')
    menu()


if __name__ == '__main__':
    main()
