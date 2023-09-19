import pygame
import os
import random

# Define some constants for the game
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CARD_SIZE = 100
FPS = 60

# Initialize Pygame
pygame.init()
pygame.display.set_caption("Memory Matching Game")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Load images from the provided directories
image_dir = "C:\\Users\\Tanya Tiwari\\Desktop\\project\\games\\mg2\\images"
image_files = os.listdir(image_dir)
images = []
for file in image_files:
    if file.lower().endswith((".jpg", ".png")):
        image_path = os.path.join(image_dir, file)
        image = pygame.image.load(image_path)
        image = pygame.transform.scale(image, (CARD_SIZE, CARD_SIZE))
        images.append(image)

# Define the levels and their corresponding grid sizes
LEVELS = {
    "easy": (2, 3),
    "medium": (3, 4),
    "hard": (4, 5)
}

# Helper function to randomly select a subset of images for each game
def select_images(num_images):
    if num_images > len(images):
        raise ValueError("Not enough unique images for the requested level.")
    selected_images = random.sample(images, num_images)
    return selected_images

# Helper function to initialize the game with a specific level
def initialize_game(level):
    global cards, flipped, selected, flipped_pos, selected_pos
    rows, cols = LEVELS[level]
    num_images = (rows * cols )// 2  # Calculate the number of pairs needed
    cards = select_images(num_images)
    random.shuffle(cards)
    flipped = [False] * len(cards)
    selected = []
    flipped_pos = (-1, -1)
    selected_pos = []

# Helper function to draw the cards
def draw_cards(cards, flipped,cols):
    for i, card in enumerate(cards):
        row = i // cols
        col = i % cols
        x = col * (CARD_SIZE + 10) + 150
        y = row * (CARD_SIZE + 10) + 100
        if flipped[i]:
            screen.blit(card, (x, y))
        else:
            pygame.draw.rect(screen, (255, 255, 255), (x, y, CARD_SIZE, CARD_SIZE))

# Main level selection loop
def select_level():
    level = None
    font = pygame.font.Font(None, 36)
    buttons = {
        "easy": pygame.Rect(250, 200, 300, 50),
        "medium": pygame.Rect(250, 300, 300, 50),
        "hard": pygame.Rect(250, 400, 300, 50)
    }

    while level is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for btn_name, btn_rect in buttons.items():
                    if btn_rect.collidepoint(mouse_pos):
                        level = btn_name

        screen.fill((0, 0, 0))
        for btn_rect in buttons.values():
            pygame.draw.rect(screen, (255, 255, 255), btn_rect)
        for btn_name, btn_rect in buttons.items():
            text = font.render(btn_name.capitalize(), True, (0, 0, 0))
            text_rect = text.get_rect(center=btn_rect.center)
            screen.blit(text, text_rect)
        pygame.display.flip()

    return level

def game_over_screen():
    font = pygame.font.Font(None, 36)
    back_button = pygame.Rect(650, 50, 100, 40)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if back_button.collidepoint(mouse_pos):
                    return  # Return to the level selection screen
                
        screen.fill((0, 0, 0))
        
back_button = pygame.Rect(650,50,100,40)


# Main game loop
def run_game():
    level = select_level()

    if level is not None:
        initialize_game(level)
        rows, cols = LEVELS[level]
        num_images = rows * cols // 2
        cards = select_images(num_images)
        cards *= 2
        random.shuffle(cards)
        flipped = [False] * len(cards)

        running = True
        selected = []
        selected_pos = []



        # Define the font for the "Back" button
        font = pygame.font.Font(None, 24)  # You can adjust the font size as needed


        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and len(selected) < 2:
                    x, y = event.pos
                    col = (x - 150) // (CARD_SIZE + 10)
                    row = (y - 100) // (CARD_SIZE + 10)
                    index = row * cols + col

                    if not flipped[index]:
                        flipped[index] = True
                        selected.append(cards[index])
                        selected_pos.append((row, col))
                    
                    # Check if the "Back" button was clicked
                    '''if back_button.collidepoint(x, y):
                        level = select_level()  # Return to the level selection screen
                        if level is None:
                            running = False
                            break
                        initialize_game(level)
                        flipped = [False] * len(cards)
                        selected.clear()
                        selected_pos.clear()'''


                    # Check if the "Back" button was clicked
                    if 650 <= x <= 750 and 50 <= y <= 90:
                        run_game()

            if len(selected) == 2:
                if selected[0] == selected[1]:
                    for row, col in selected_pos:
                        flipped[row * cols + col] = True
                else:
                    for row, col in selected_pos:
                        flipped[row * cols + col] = False
                selected.clear()
                selected_pos.clear()

            '''if all(flipped):
                game_over_screen()
                initialize_game(level)'''

            screen.fill((0, 0, 0))
            draw_cards(cards, flipped,cols)

            # Draw the "Back" button
            pygame.draw.rect(screen, (255, 255, 255), back_button)
            back_text = font.render("Back", True, (0, 0, 0))
            back_text_rect = back_text.get_rect(center=back_button.center)
            screen.blit(back_text, back_text_rect)

            pygame.display.flip()
            clock.tick(FPS)

        pygame.quit()

if __name__ == "__main__":
    run_game()
