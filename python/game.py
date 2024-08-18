import pygame
import math
import random
import requests
import json
import os

GREY = (192, 192, 192)
WIDTH, HEIGHT = 900, 720
FPS = 60
radius = 25
space = 20
incorrect = 0

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman")
clock = pygame.time.Clock()

# Fetch word
try:
    words = requests.get("https://random-word-api.herokuapp.com/word").json()
    word = words[0].upper() if words else "PYTHON"
except Exception as e:
    print("Error fetching word:", e)
    word = "PYTHON"

guessed = []
letters = []
x_start = round((WIDTH - (radius * 2 + space) * 13) / 2)
y_start = 540

# Create letter buttons
A = 65
for i in range(26):
    x = x_start + space * 2 + ((radius * 2 + space) * (i % 13))
    y = y_start + ((i // 13) * (space + radius * 2))
    letters.append([x, y, chr(A + i), True])

# Fonts
font = pygame.font.SysFont("8-Bit-Madness", 45)
WORD = pygame.font.SysFont("8-Bit-Madness", 40)
TITLE = pygame.font.SysFont("8-Bit-Madness", 70)

# Draw Hangman function
def draw_hangman(count):
    if count > 0:
        pygame.draw.circle(screen, GREY, (300, 180), 50, 10)
    if count > 1:
        pygame.draw.circle(screen, GREY, (280, 165), 10)
        pygame.draw.circle(screen, GREY, (320, 165), 10)
    if count > 2:
        pygame.draw.arc(screen, GREY, (270, 170, 60, 40), math.pi, 2 * math.pi, 4)
    if count > 3:
        pygame.draw.line(screen, GREY, (300, 230), (300, 380), 10)
    if count > 4:
        pygame.draw.line(screen, GREY, (300, 270), (380, 230), 10)
    if count > 5:
        pygame.draw.line(screen, GREY, (300, 270), (220, 230), 10)
    if count > 6:
        pygame.draw.line(screen, GREY, (300, 380), (340, 450), 10)
    if count > 7:
        pygame.draw.line(screen, GREY, (300, 380), (260, 450), 10)

# Draw function
def draw():
    screen.fill((255, 255, 255))
    title = TITLE.render("Hangman", 1, (0, 0, 0))
    screen.blit(title, (WIDTH / 1.9 - title.get_width() / 2, 10))
    
    disp_word = ""
    for ltr in word:
        if ltr in guessed:
            disp_word += ltr + " "
        else:
            disp_word += "_ "
    
    text = WORD.render(disp_word, 1, (0, 0, 0))
    screen.blit(text, (500, 250))
    
    for btn_pos in letters:
        x, y, ltr, visible = btn_pos
        if visible:
            pygame.draw.circle(screen, (0, 0, 0), (x, y), radius, 4)
            txt = font.render(ltr, 1, (0, 0, 0))
            screen.blit(txt, (x - txt.get_width() / 2, y - txt.get_height() / 2))
    
    draw_hangman(incorrect)
    pygame.display.update()

# Game loop
run = True
while run:
    clock.tick(FPS)
    draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            x_mouse, y_mouse = pygame.mouse.get_pos()
            for letter in letters:
                x, y, ltr, visible = letter
                if visible:
                    dist = math.sqrt((x - x_mouse) ** 2 + (y - y_mouse) ** 2)
                    if dist <= radius:
                        letter[3] = False
                        guessed.append(ltr)
                        print(f"Guessed letter: {ltr}, Word: {word}")  # Debug print
                        if ltr not in word:
                            incorrect += 1

    # Check for win or loss
    won = all(letter in guessed for letter in word)
    if won:
        draw()
        pygame.time.delay(1000)
        screen.fill((0, 0, 0))
        text = WORD.render("YOU WON", 1, (129, 255, 0))
        screen.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
        pygame.display.update()
        pygame.time.delay(4000)
        print("WON")
        break

    if incorrect >= 8:
        draw()
        pygame.time.delay(1000)
        screen.fill((0, 0, 0))
        text = WORD.render("YOU LOST", 1, (255, 0, 0))
        answer = WORD.render("The answer is " + word, 1, (129, 255, 0))
        screen.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
        screen.blit(answer, (WIDTH / 2 - answer.get_width() / 2, HEIGHT / 2 - text.get_height() / 2 + 70))
        pygame.display.update()
        pygame.time.delay(4000)
        print("LOST")
        break

pygame.quit()