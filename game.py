import pygame
import math
import requests


REDDISH = (216, 112, 147)
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
        pygame.draw.circle(screen, REDDISH, (150, 180), 50, 10)
    if count > 1 and count <= 7:
        pygame.draw.circle(screen, REDDISH, (130, 165), 10)
        pygame.draw.circle(screen, REDDISH, (170, 165), 10)
    if count > 2:
        if incorrect == 3:
            pygame.draw.arc(screen, REDDISH, (120, 170, 60, 40), math.pi, 2 * math.pi, 4)
        if incorrect == 4:
            pygame.draw.arc(screen, REDDISH, (120, 180, 60, 20), math.pi, 2 * math.pi, 4)
        if incorrect >= 5 and count <= 7:
            pygame.draw.arc(screen, REDDISH, (120, 180, 60, 20), 2 *math.pi,  math.pi, 4)

    if count > 3:
        pygame.draw.line(screen, REDDISH, (150, 230), (150, 380), 10)
    if count > 4:
        pygame.draw.line(screen, REDDISH, (150, 270), (230, 230), 10)
    if count > 5:
        pygame.draw.line(screen, REDDISH, (150, 270), (70, 230), 10)
    if count > 6:
        pygame.draw.line(screen, REDDISH, (150, 380), (190, 450), 10)
    if count > 7:
        pygame.draw.line(screen, REDDISH, (150, 380), (110, 450), 10)
    if count >= 8:
        #left eye end
        pygame.draw.line(screen, REDDISH, (120, 160), (140, 180), 4)
        pygame.draw.line(screen, REDDISH, (120, 180), (140, 160), 4)
        #right eye end
        pygame.draw.line(screen, REDDISH, (160, 160), (180, 180), 4)
        pygame.draw.line(screen, REDDISH, (160, 180), (180, 160), 4)
        # mouth end
        pygame.draw.line(screen, REDDISH, (130, 200), (170, 200), 4)
        pygame.draw.arc(screen, REDDISH, (128, 230, 40, 10), 0, 2 * math.pi, 10)  # Noose

#draw gallows
def draw_gallows():
    pygame.draw.line(screen, REDDISH, (50, 500), (50, 120), 10)  # Post
    # Horizontal beam
    pygame.draw.line(screen, REDDISH, (50, 120), (160, 100), 10)  # Beam
    pygame.draw.line(screen, REDDISH, (155, 100), (155, 140), 10)  # Noose rope

# Improved Button Design and Hover Effects
def draw_buttons():
    continue_button = pygame.Rect(WIDTH / 2 - 100, HEIGHT / 2 + 50, 200, 50)
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if continue_button.collidepoint(mouse_x, mouse_y):
        pygame.draw.rect(screen, (0, 200, 0), continue_button, border_radius=25)  # Hover color
    else:
        pygame.draw.rect(screen, (0, 255, 0), continue_button, border_radius=25)  # Normal color

    continue_txt = WORD.render("Continue", True, BLACK)
    screen.blit(continue_txt, (WIDTH / 2 - continue_txt.get_width() / 2, HEIGHT / 2 + 60))

#adding gradient background blue to black
def draw_gradient_background():
    start_color = (230, 230, 250)  # Lavender
    end_color = (204, 153, 255)    # Light Purple
    for i in range(HEIGHT):
        r = int(start_color[0] * (1 - i / HEIGHT) + end_color[0] * (i / HEIGHT))
        g = int(start_color[1] * (1 - i / HEIGHT) + end_color[1] * (i / HEIGHT))
        b = int(start_color[2] * (1 - i / HEIGHT) + end_color[2] * (i / HEIGHT))
        color = (r, g, b)
        pygame.draw.line(screen, color, (0, i), (WIDTH, i))

def draw():
    draw_gradient_background()
    screen.fill((204, 153, 255))
    title = TITLE.render("Hangman", True, BLACK)
    screen.blit(title, (WIDTH / 2 - title.get_width() / 2, 10))
    
    disp_word = ""
    for ltr in word:
        if ltr in guessed:
            disp_word += ltr + " "
        else:
            disp_word += "_ "
    
    text = WORD.render(disp_word, True, BLACK)
    screen.blit(text, (500, 250))
    
    for btn_pos in letters:
        x, y, ltr, visible = btn_pos
        if visible:
            pygame.draw.circle(screen, BLACK, (x, y), radius, 4)
            txt = font.render(ltr, True, BLACK)
            screen.blit(txt, (x - txt.get_width() / 2, y - txt.get_height() / 2))
    
    draw_gallows()
    draw_hangman(incorrect)
    stats_text = WORD.render(f"Wins: {win_count}   Losses: {loss_count}", True, BLACK)
    screen.blit(stats_text, (10, 10))

    if game_over:
        draw_buttons()
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