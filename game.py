import pygame
import math
import requests


GREY = (192, 192, 192)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
WIDTH, HEIGHT = 900, 720
FPS = 60
radius = 25
space = 20
incorrect = 0
win_count = 0
loss_count = 0

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman")
clock = pygame.time.Clock()
x_start = round((WIDTH - (radius * 2 + space) * 13) / 2)
y_start = 540

# Fetch word
def get_word():
    try:
        response = requests.get("https://random-word-api.herokuapp.com/word")
        if response.status_code == 200:
            words = response.json()
            if words:
                return words[0].upper()
    except Exception as e:
        print("Error fetching word:", e)
    return "HANGMAN"

def reset_game():
    global word, guessed, incorrect, letters, game_over, game_result
    word = get_word()
    guessed = []
    incorrect = 0
    letters = []
    A = 65
    for i in range(26):
        x = x_start + space * 2 + ((radius * 2 + space) * (i % 13))
        y = y_start + ((i // 13) * (space + radius * 2))
        letters.append([x, y, chr(A + i), True])
    game_over = False
    game_result = ""

reset_game()

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

def draw():
    screen.fill(WHITE)
    title = TITLE.render("Hangman", 1, BLACK)
    screen.blit(title, (WIDTH / 1.9 - title.get_width() / 2, 10))
    
    disp_word = ""
    for ltr in word:
        if ltr in guessed:
            disp_word += ltr + " "
        else:
            disp_word += "_ "
    
    text = WORD.render(disp_word, 1, BLACK)
    screen.blit(text, (500, 250))
    
    for btn_pos in letters:
        x, y, ltr, visible = btn_pos
        if visible:
            pygame.draw.circle(screen, BLACK, (x, y), radius, 4)
            txt = font.render(ltr, 1, BLACK)
            screen.blit(txt, (x - txt.get_width() / 2, y - txt.get_height() / 2))
    
    draw_hangman(incorrect)
    stats_text = WORD.render(f"Wins: {win_count}   Losses: {loss_count}", True, BLACK)
    screen.blit(stats_text, (10, 10))

    if game_over:
        continue_button = pygame.draw.rect(screen, (0,255,0), (WIDTH / 2 - 100, HEIGHT / 2 + 50, 200, 50))
        continue_txt = WORD.render("Continue ?", True, BLACK)
        screen.blit(continue_txt, (WIDTH / 2 - continue_txt.get_width() / 2, HEIGHT / 2 + 50, 200, 10))

        result_text = WORD.render(game_result, True, BLACK)
        screen.blit(result_text, (WIDTH / 2 - result_text.get_width() / 2, HEIGHT / 2 + 120))

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
            if game_over:
                if (WIDTH / 2 - 100 <= x_mouse <= WIDTH / 2 + 100 and HEIGHT / 2 + 50 <= y_mouse <= HEIGHT / 2 + 100):
                    reset_game()
                    continue

            for letter in letters:
                x, y, ltr, visible = letter

                if visible:
                    dist = math.sqrt((x - x_mouse) ** 2 + (y - y_mouse) ** 2)
                    if dist <= radius:
                        letter[3] = False
                        guessed.append(ltr)
                        print(f"Guessed letter: {ltr}, Word: {word}")
                        if ltr not in word:
                            incorrect += 1

    # Check for win or loss
    won = all(letter in guessed for letter in word)
    if won and not game_over:
        game_result = "YOU WON"
        win_count += 1
        game_over = True
        continue

    if incorrect >= 8 and not game_over:
        game_result = f"YOU LOST, The answer was {word}"
        loss_count += 1
        game_over = True
        continue

pygame.quit()