import os
import sys
from random import randint
import pygame

pygame.init()

# Janela
SIZE = WIDTH, HEIGHT = 400, 600
SCREEN = pygame.display.set_mode(SIZE)

# Cores
BLACK = (0, 0, 0)
PINK = (234, 212, 252)
RED = (255, 0, 0)
GRAY = (200, 200, 200)

# Fontes
DIRECTORY = os.getcwd()
FONT = DIRECTORY + "/fonts/unispace_rg.ttf"

pygame.display.set_caption("Shooting Words")

list_words = ["cachorro", "planta", "arvore", "bolo", "maça"]

clock = pygame.time.Clock()

pos_y = 0

FONT = pygame.font.Font(FONT, 24)
VELOCIDA_QUEDA = 1.5

TEXT_DELAY = 2000
TEXT_NEXT_TIME = TEXT_DELAY

palavras = []
pos_xs = []

class Palavra:
    def __init__(self, text: str, pos_x, pos_y=pos_y):
        self.text = text
        self.x = pos_x
        self.y = pos_y
        self.text_render = FONT.render(self.text, True, PINK)

    def draw(self):
        self.y += VELOCIDA_QUEDA
        SCREEN.blit(self.text_render, (self.x, self.y))

    def remove_letra(self, keydown):
        tecla = pygame.key.name(keydown)
        if tecla not in self.text.lower():
            return

        i = self.text.index(tecla)
        _text = list(self.text)
        del _text[i]
        self.text = "".join(_text)
        self.text_render = FONT.render(self.text, True, PINK)

LARGURA_MAX = 150
def nova_posicao_x():
    pos_x = randint(0, LARGURA_MAX)

    while pos_x in pos_xs:
        pos_x = randint(0, LARGURA_MAX)

    pos_xs.append(pos_x)
    return pos_x

ALT_MIN_ENTRE_PALAVRAS = 100
def nova_palavra(ticks):
    global TEXT_NEXT_TIME

    if palavras:
        if (palavras[-1].y >= ALT_MIN_ENTRE_PALAVRAS) and (ticks > TEXT_NEXT_TIME):
            TEXT_NEXT_TIME = ticks + TEXT_DELAY
        else:
            return

    pos_x = nova_posicao_x()
    index = randint(0, len(list_words)-1)
    text = list_words[index]
    palavras.append(Palavra(text, pos_x))

def remove_palavra(index):
    palavras.pop(index)
    pos_xs.pop(index)

ALT_MAX_PARA_REMOVER = HEIGHT - 5
def remove_palavra_fora_da_tela():
    for i, palavra in enumerate(palavras):
        if palavra.y > ALT_MAX_PARA_REMOVER:
            remove_palavra(i)

def remove_letra(event_keydown):
    index = 0 # FIFO
    palavras[index].remove_letra(event_keydown)
    if not palavras[index].text:
        remove_palavra(index)

def escreve_palavras_na_tela():
    remove_palavra_fora_da_tela()
    for p in palavras:
        p.draw()

ticks = pygame.time.get_ticks()
nova_palavra(ticks)

running = True
while running:
    ticks = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            remove_letra(event.key)

    SCREEN.fill(BLACK)

    nova_palavra(ticks)
    escreve_palavras_na_tela()

    pygame.display.flip()
    clock.tick(60)