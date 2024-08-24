import pygame
import math
import requests
import sys


REDDISH = (216, 112, 147)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FPS = 60
RADIUS = 25
SPACE = 20


class HangmanGame:
    def __init__(self):
        # Define constants
        self.REDDISH = (216, 112, 147)
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.WIDTH, self.HEIGHT = 900, 720
        self.FPS = 60
        self.radius = 25
        self.space = 20
        self.incorrect = 0
        self.win_count = 0
        self.loss_count = 0
        self.button_width = 200
        self.button_height = 50

        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Hangman")
        self.clock = pygame.time.Clock()
        self.x_start = round((self.WIDTH - (self.radius * 2 + self.space) * 13) / 2)
        self.y_start = 540

        self.reset_game()

        # Fonts
        self.font = pygame.font.SysFont("Chalkduster.ttf", 45)
        self.WORD = pygame.font.SysFont("Chalkduster.ttf", 40)
        self.TITLE = pygame.font.SysFont("Chalkduster.ttf", 70)

    def resize_screen(self, new_width, new_height):
        self.WIDTH, self.HEIGHT = new_width, new_height
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.RESIZABLE)
        
        # Recalculate positions and spacing
        self.x_start = (self.WIDTH - (self.radius * 2 + self.space) * 13) // 2
        self.y_start = self.HEIGHT - (self.radius * 2 + self.space) * 2 - 100
        
        for i in range(26):
            x = self.x_start + self.space * 2 + ((self.radius * 2 + self.space) * (i % 13))
            y = self.y_start + ((i // 13) * (self.space + self.radius * 2))
            self.letters[i][0] = x
            self.letters[i][1] = y
        
        self.continue_button_rect = pygame.Rect(
            self.WIDTH // 2 - self.button_width // 2,
            self.HEIGHT - self.button_height - 30,
            self.button_width,
            self.button_height
        )

    # Fetch word
    def get_word(self):
        try:
            response = requests.get("https://random-word-api.herokuapp.com/word")
            if response.status_code == 200:
                words = response.json()
                if words:
                    return words[0].upper()
        except Exception as e:
            print("Error fetching word:", e)
        return "HANGMAN"

    def reset_game(self):
        self.word = self.get_word()
        self.guessed = []
        self.incorrect = 0
        self.letters = []
        A = 65
        
        # Recalculate positions of letter buttons
        self.x_start = round((self.WIDTH - (self.radius * 2 + self.space) * 13) / 2)
        self.y_start = self.HEIGHT - (self.radius * 2 + self.space) * 2 - 100  # Adjust vertical position if needed
        
        for i in range(26):
            x = self.x_start + self.space * 2 + ((self.radius * 2 + self.space) * (i % 13))
            y = self.y_start + ((i // 13) * (self.space + self.radius * 2))
            self.letters.append([x, y, chr(A + i), True])

        self.game_over = False
        self.game_result = ""

        # Recalculate button positions
        self.continue_button_rect = pygame.Rect(
            self.WIDTH / 2 - self.button_width / 2,
            self.HEIGHT - self.button_height - 30,  # Adjust vertical position if needed
            self.button_width,
            self.button_height
        )

    # Draw Hangman function
    def draw_hangman(self, count):
        # Drawing hangman based on the count of incorrect guesses
        if count > 0:
            pygame.draw.circle(self.screen, self.REDDISH, (150, 180), 50, 10)
        if count > 1 and count <= 7:
            pygame.draw.circle(self.screen, self.REDDISH, (130, 165), 10)
            pygame.draw.circle(self.screen, self.REDDISH, (170, 165), 10)
        if count > 2:
            if self.incorrect == 3:
                pygame.draw.arc(self.screen, self.REDDISH, (120, 170, 60, 40), math.pi, 2 * math.pi, 4)
            if self.incorrect == 4:
                pygame.draw.arc(self.screen, self.REDDISH, (120, 180, 60, 20), math.pi, 2 * math.pi, 4)
            if self.incorrect >= 5 and count <= 7:
                pygame.draw.arc(self.screen, self.REDDISH, (120, 180, 60, 20), 2 *math.pi,  math.pi, 4)

        if count > 3:
            pygame.draw.line(self.screen, self.REDDISH, (150, 230), (150, 380), 10)
        if count > 4:
            pygame.draw.line(self.screen, self.REDDISH, (150, 270), (230, 230), 10)
        if count > 5:
            pygame.draw.line(self.screen, self.REDDISH, (150, 270), (70, 230), 10)
        if count > 6:
            pygame.draw.line(self.screen, self.REDDISH, (150, 380), (190, 450), 10)
        if count > 7:
            pygame.draw.line(self.screen, self.REDDISH, (150, 380), (110, 450), 10)
        if count >= 8:
            pygame.draw.line(self.screen, self.REDDISH, (120, 160), (140, 180), 4)
            pygame.draw.line(self.screen, self.REDDISH, (120, 180), (140, 160), 4)
            pygame.draw.line(self.screen, self.REDDISH, (160, 160), (180, 180), 4)
            pygame.draw.line(self.screen, self.REDDISH, (160, 180), (180, 160), 4)
            pygame.draw.line(self.screen, self.REDDISH, (130, 200), (170, 200), 4)
            pygame.draw.arc(self.screen, self.REDDISH, (128, 230, 40, 10), 0, 2 * math.pi, 10)

    #draw gallows
    def draw_gallows(self):
        pygame.draw.line(self.screen, REDDISH, (50, 500), (50, 120), 10)
        pygame.draw.line(self.screen, REDDISH, (50, 120), (160, 100), 10)
        pygame.draw.line(self.screen, REDDISH, (155, 100), (155, 140), 10)

    # Improved continue Button Design and Hover Effects
    def draw_buttons(self):
        # Draw the continue button with a gradient or rounded effect
        button_color = (0, 255, 0) if not self.continue_button_rect.collidepoint(pygame.mouse.get_pos()) else (0, 200, 0)
        pygame.draw.rect(self.screen, button_color, self.continue_button_rect, border_radius=25)
        
        # Add button text with shadow
        continue_txt = self.WORD.render("Continue", True, self.BLACK)
        shadow_txt = self.WORD.render("Continue", True, (100, 100, 100))  # Shadow color
        self.screen.blit(shadow_txt, (self.continue_button_rect.centerx - continue_txt.get_width() / 2 + 2, 
                                    self.continue_button_rect.centery - continue_txt.get_height() / 2 + 2))
        self.screen.blit(continue_txt, (self.continue_button_rect.centerx - continue_txt.get_width() / 2, 
                                        self.continue_button_rect.centery - continue_txt.get_height() / 2))


    #adding gradient background blue to black
    def draw_gradient_background(self):
        start_color = (230, 230, 250)
        end_color = (204, 153, 255)
        gradient_surface = pygame.Surface((self.WIDTH, self.HEIGHT))
        for i in range(self.HEIGHT):
            r = int(start_color[0] * (1 - i / self.HEIGHT) + end_color[0] * (i / self.HEIGHT))
            g = int(start_color[1] * (1 - i / self.HEIGHT) + end_color[1] * (i / self.HEIGHT))
            b = int(start_color[2] * (1 - i / self.HEIGHT) + end_color[2] * (i / self.HEIGHT))
            color = (r, g, b)
            pygame.draw.line(gradient_surface, color, (0, i), (self.WIDTH, i))
        self.screen.blit(gradient_surface, (0, 0))


    def draw(self):
        self.draw_gradient_background()
        self.screen.fill((204, 153, 255))
        
        # Draw title
        title = self.TITLE.render("Hangman", True, self.BLACK)
        title_rect = title.get_rect(center=(self.WIDTH // 2, 10 + title.get_height() // 2))
        self.screen.blit(title, title_rect)

        # Draw guessed word
        disp_word = " ".join(ltr if ltr in self.guessed else "_" for ltr in self.word)
        text = self.WORD.render(disp_word, True, self.BLACK)
        text_rect = text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2 - 50))
        self.screen.blit(text, text_rect)

        # Draw letter buttons
        for x, y, ltr, visible in self.letters:
            if visible:
                pygame.draw.circle(self.screen, self.BLACK, (x, y), self.radius, 4)
                txt = self.font.render(ltr, True, self.BLACK)
                txt_rect = txt.get_rect(center=(x, y))
                self.screen.blit(txt, txt_rect)

        self.draw_gallows()
        self.draw_hangman(self.incorrect)

        # Draw stats
        stats_text = self.WORD.render(f"Wins: {self.win_count}   Losses: {self.loss_count}", True, self.BLACK)
        stats_rect = stats_text.get_rect(topleft=(10, 10))
        self.screen.blit(stats_text, stats_rect)

        if self.game_over:
            self.draw_buttons()
            
            # Calculate the position for result text
            result_text = self.WORD.render(self.game_result, True, self.BLACK)
            result_rect = result_text.get_rect(center=(self.WIDTH // 2, self.continue_button_rect.top - 20))

            # Draw the result text above the continue button with a margin
            self.screen.blit(result_text, result_rect)

        pygame.display.update()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.VIDEORESIZE:
                    self.resize_screen(event.w, event.h)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_click(event)
                elif event.type == pygame.KEYDOWN:
                    self.handle_key_press(event)

            self.update()
            self.draw()
            self.clock.tick(self.FPS)

    def update(self):
        won = all(letter in self.guessed for letter in self.word)
        if won and not self.game_over:
            self.game_result = "YOU WON"
            self.win_count += 1
            self.game_over = True

        if self.incorrect >= 8 and not self.game_over:
            self.game_result = f"YOU LOST, The answer was {self.word}"
            self.loss_count += 1
            self.game_over = True

    def handle_mouse_click(self, event):
        x_mouse, y_mouse = pygame.mouse.get_pos()
        
        if self.game_over:
            # Check if the continue button is clicked
            if self.continue_button_rect.collidepoint(x_mouse, y_mouse):
                self.reset_game()
                return

        # Check if a letter button is clicked
        for letter in self.letters:
            x, y, ltr, visible = letter
            if visible:
                dist = math.sqrt((x - x_mouse) ** 2 + (y - y_mouse) ** 2)
                if dist <= self.radius:
                    letter[3] = False
                    self.guessed.append(ltr)
                    if ltr not in self.word:
                        self.incorrect += 1
                    return

    #Handle keyboard click
    def handle_key_press(self, event):
        if event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
        
        if pygame.K_a <= event.key <= pygame.K_z:
            letter = chr(event.key).upper()
            
            # Check if the letter is in the available letters and hasn't been guessed yet
            if letter in [ltr for _, _, ltr, visible in self.letters if visible] and letter not in self.guessed:
                self.guessed.append(letter)
                
                # Update letter visibility based on the guess
                for letter_data in self.letters:
                    x, y, ltr, visible = letter_data
                    if ltr == letter:
                        letter_data[3] = False  # Mark the letter as guessed
                
                # Update incorrect count if necessary
                if letter not in self.word:
                    self.incorrect += 1

if __name__ == "__main__":
    game = HangmanGame()
    game.run()
