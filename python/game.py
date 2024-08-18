import pygame
import math
import random
import requests
import json

GREY  = (192,192,192)
WIDTH, HEIGHT = 900, 720

pygame.init()

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Hangman")

FPS = 60
clock = pygame.time.Clock() 
run = True
word = requests.get("https://random-word-api.herokuapp.com/word").json()[0]

#Buttons

radius = 25
space = 20
letters = []
x_start = round((WIDTH - (radius * 2 + space) * 13) / 2)
y_start = 540

#Letters
A = 65
for i in range(26): 
    x = x_start + space * 2 + ((radius * 2 + space) * (i % 13)) 
    y = y_start + ((i // 13) * (space + radius * 2)) 
    letters.append([x, y, chr(A + i), True]) 

#Drawing Hangman based on remaining guesses

def draw_hangman(count):
    pi = 3.14
    global state, gameLost, invalidTries
    if count > 0:
        pygame.draw.circle(screen, GREY, (300,180), 50, 10)
    if count > 1:
        pygame.draw.circle(screen, GREY, (280,165), 10, 5)
        pygame.draw.circle(screen, GREY, (320,165), 10, 5)
    #mouth different shapes depending on tries
    if count > 2:
        if len(invalidTries) == 3:
            pygame.draw.arc(screen, GREY, [280,180,40,30], pi, 2*pi, 4)
        elif len(invalidTries) == 4:
            pygame.draw.arc(screen, GREY, [280,184,40,20], pi, 2*pi, 4)
        elif len(invalidTries) == 5:
            pygame.draw.arc(screen, GREY, [280,188,40,10], pi, 2*pi, 4)
        elif len(invalidTries) == 6:
            pygame.draw.arc(screen, GREY, [280,188,40,20], 2*pi, pi, 4)
        elif len(invalidTries) == 7:
            pygame.draw.arc(screen, GREY, [280,188,40,30], 2*pi, pi, 4)
    if count > 3:
        pygame.draw.line(screen, GREY, (300, 230), (300, 380),10)
    if count > 4:
        pygame.draw.line(screen, GREY, (300, 270), (380, 230),10)
    if count > 5:
        pygame.draw.line(screen, GREY, (300, 270), (220, 230),10)
    if count > 6:
        pygame.draw.line(screen, GREY, (300, 380), (340, 450),10)
    if count > 7:
        pygame.draw.line(screen, GREY, (300, 380), (260, 450),10)
        state+=1
        gamesLost+=1

