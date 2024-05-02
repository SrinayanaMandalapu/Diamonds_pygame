import pygame
import sys
import os
from strategy import ComputerStrategy
from gameplay import Game

class UI:
    def __init__(self):
        self.screen_width = 1000
        self.screen_height = 700
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.gray = (200, 200, 200)
        self.light_gray = (220, 220, 220)
        self.dark_gray = (100, 100, 100)
        self.blue = (0, 0, 255)
        self.font_size = 36
        self.font = pygame.font.SysFont(None, self.font_size)
        self.card_images = self.load_card_images()
        self.computer_strategy = ComputerStrategy()

    def load_card_images(self):
        images_dir = "images"
        card_images = {}
        for filename in os.listdir(images_dir):
            if filename.endswith(".png"):
                card_images[filename[:-4]] = pygame.image.load(os.path.join(images_dir, filename))
        return card_images

    def display_text(self, text, position, font_size=None, color=None):
        if font_size is None:
            font_size = self.font_size
        if color is None:
            color = self.white
        text_surface = self.font.render(text, True, color)
        self.screen.blit(text_surface, position)

    def draw_button(self, text, rect, action=None, font_size=24):
        mouse_pos = pygame.mouse.get_pos()
        clicked = pygame.mouse.get_pressed()[0]
        if rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, self.light_gray, rect)  
            if clicked and action:
                action()  
        else:
            pygame.draw.rect(self.screen, self.gray, rect)
        self.display_text(text, (rect.x + 10, rect.y + 10), font_size)

    def display_player_cards(self, player_cards):
        x_offset = 50
        for card_name in player_cards:
            self.screen.blit(self.card_images[card_name], (x_offset, 350))
            x_offset += 60

    def draw_top_menu(self):
        pygame.draw.rect(screen, self.dark_gray, pygame.Rect(0, 0, self.screen_width, 50))
        self.draw_button("New Game", pygame.Rect(20, 10, 100, 30), self.main_menu, 20)
        self.draw_button("Quit", pygame.Rect(self.screen_width - 120, 10, 100, 30), self.quit_game, 20)

    def define_game(self):
        self.display_text("Bidding Diamonds Cards Game", (20, 40), font_size=40)
        self.display_text("Rules:", (20, 100), font_size=28)
        # Define game rules display
        #display_text("Bidding Diamonds Cards Game", (20, 40), font_size=40)
        #display_text("Rules:", (20, 100), font_size=28)
        self.display_text("1. Number of Players: 2-3 players compete.", (20, 130), font_size=24)
        self.display_text("2. Card Distribution:", (20, 160), font_size=24)
        self.display_text("- Each player receives a hand of 13 cards.", (40, 190), font_size=20)
        self.display_text("- One suit (clubs, hearts, spades, or diamonds) is assigned to each player.", (40, 210), font_size=20)
        self.display_text("3. Bidding Rounds:", (20, 240), font_size=24)
        self.display_text("- In each round, a diamond card is revealed.", (40, 270), font_size=20)
        self.display_text("- Players take turns bidding with a card from their assigned suit.", (40, 300), font_size=20)
        self.display_text("- The highest bidder wins the round.", (40, 330), font_size=20)
        self.display_text("4. Scoring:", (20, 360), font_size=24)
        self.display_text("- The winner earns points equal to the value of the revealed diamond card.", (40, 390), font_size=20)
        self.display_text("- Points are earned based on the number of diamonds won in each round.", (40, 420), font_size=20)
        self.display_text("5. Tie Cases:", (20, 450), font_size=24)
        self.display_text("- In the event of a tie bid, average points are awarded.", (40, 480), font_size=20)
        self.display_text("6. Game End:", (20, 510), font_size=24)
        self.display_text("- After 13 rounds, the player with the most accumulated diamonds wins the game.", (40, 540), font_size=20)

    def main_menu(self):
        while True:
            self.screen.fill(self.black)
            self.define_game()
            self.draw_button("Play Against Friends", pygame.Rect(100, 600, 180, 40), lambda: self.start_game(False), font_size=20)
            self.draw_button("Play Against Computer", pygame.Rect(400, 600, 180, 40), lambda: self.start_game(True), font_size=20)
            self.draw_button("Quit", pygame.Rect(700, 600, 180, 40), self.quit_game, font_size=20)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                elif event.type == pygame.MOUSEBUTTONDOWN:  
                    if pygame.Rect(350, 550, 300, 50).collidepoint(event.pos):
                        self.start_game()
                    elif pygame.Rect(350, 620, 300, 50).collidepoint(event.pos):
                        self.quit_game()

    def start_game(self, against_computer):
        # Game start logic goes here
        num_players = 2 if against_computer else 3
        self.game = Game(num_players, against_computer)
        
        # Start the game loop
        self.game.start()

    def quit_game(self):
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    ui = UI()
    pygame.init()
    screen = pygame.display.set_mode((ui.screen_width, ui.screen_height))
    pygame.display.set_caption("Bidding Diamonds Cards Game")
    ui.main_menu()
