import pygame
from bird import Bird
import sys
import os
import random
from pipe import Pipe
import neat
import math


pygame.init()
pygame.font.init()


#GLOBAL 
HEIGHT, WIDTH = 800, 1500
WHITE = (255, 255, 255)
BLUE = (100, 150, 255)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
myfont = pygame.font.SysFont('Comic Sans MS', 30)
gen = 0
max_score = 0

IMAGE_BACKGROUND = pygame.image.load("Assets/background.jpg")
IMAGE_PIPE = pygame.image.load("Assets/tuyau.png")

RESIZE_MULTIPLIER = 1.5
IMAGE_BIRD = pygame.image.load("Assets/birdLowPoly_2.png")
IMAGE_BIRD = pygame.transform.scale(IMAGE_BIRD, (int(34*RESIZE_MULTIPLIER), int(24*RESIZE_MULTIPLIER)))


 #x//3 index neat pipe


def main(genomes, config):
    global birds, ge, nets, pipes, gen, max_score

    clock = pygame.time.Clock()

    gen += 1

    birds = []
    ge = []
    nets = []
    pipes = [Pipe(1000, IMAGE_PIPE), Pipe(1500, IMAGE_PIPE), Pipe(2000, IMAGE_PIPE)]

    for genome_id, genome in genomes:
        birds.append(Bird(IMAGE_BIRD, 200))
        ge.append(genome)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        genome.fitness = 0

    pipe_index = 0

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        screen.blit(IMAGE_BACKGROUND, (0, 0))
      
        for i, bird in enumerate(birds):
            bird.update()
            len_birds = len(birds)
            screen.blit(bird.img, bird.rect)
            ge[i].fitness += 0.05
            score = bird.score
        
        if score > max_score:
            max_score = score

        if len(birds) == 0:
            break

        if score <= 40:
            level_speed = 5 + score//5

        for pipe in pipes:
            pipe.update(level_speed)
            screen.blit(pipe.img, pipe.rect)
            screen.blit(pipe.img, pipe.rect_2)
            for i, bird in enumerate(birds):
                if bird.rect.colliderect(pipe.rect) or bird.rect.colliderect(pipe.rect_2) or bird.rect.y >= 800 or bird.rect.y <= 0:
                    ge[i].fitness -= 1
                    remove(i)

            if not pipe.scored and pipe.rect.x <= 100:
                for i, bird in enumerate(birds):
                    bird.score += 1
                    ge[i].fitness += 5
                pipe.scored = True
                pipe_index += 1


        for i, bird in enumerate(birds):
            output = nets[i].activate((bird.rect.y,

             bird.rect.y - pipes[pipe_index%3].rect.y,
              bird.rect.y - pipes[pipe_index%3].rect_2.y + 800,

            bird.rect.y - pipes[(pipe_index+1)%3].rect.y,
              bird.rect.y - pipes[(pipe_index+1)%3].rect_2.y + 800,

              pipe.rect.x,
              level_speed))
              
            if output[0] > 0.5:
                bird.jump = True


        ScoreText = myfont.render("Score : " + str(score), False, (0, 0, 0))
        MaxScoreText = myfont.render("Max Score : " + str(max_score), False, (0, 0, 0))
        GenText = myfont.render("Gen : " + str(gen), False, (0, 0, 0))
        LenText = myfont.render("Individuals left : " + str(len_birds), False, (0, 0, 0))
        screen.blit(ScoreText, (1330, 20))
        screen.blit(MaxScoreText, (1263, 60))
        screen.blit(GenText, (20, 20))
        screen.blit(LenText, (20, 60))

        clock.tick(60)
        pygame.display.update()

def distance(bird, rect):
    return abs(bird.rect.y - rect.y)

def remove(index):
    birds.pop(index)
    ge.pop(index)
    nets.pop(index)


# Setup the NEAT Neural Network
def run(config_path):

    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )

    pop = neat.Population(config)
    pop.run(main, 50)


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    run(config_path)