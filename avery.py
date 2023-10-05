import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Avery's B-Day Game!")

# Set up the colors
WHITE = (255, 255, 255)

# Set up the player image
player_image = pygame.image.load("avery.jpg")
desired_player_width = 100
desired_player_height = 100
player_image = pygame.transform.rotate(player_image, 270)  # Adjust rotation angle
player_image = pygame.transform.scale(player_image, (desired_player_width, desired_player_height))
player_width, player_height = player_image.get_size()
player_x = (screen_width - player_width) // 2
player_y = screen_height - player_height

# Set up falling objects
falling_objects = [
    {
        "image": pygame.image.load("jersey_mikes.png"),
        "score": 1,
        "frequency": 50
    },
    {
        "image": pygame.image.load("moosetracks.png"),
        "score": 5,
        "frequency": 100
    },
    {
        "image": pygame.image.load("orange.png"),
        "score": -5,
        "frequency": 400
    },
    {
        "image": pygame.image.load("seafood.png"),
        "score": -9999,  # Negative score to trigger game over
        "frequency": 1000
    }
]

# Set up falling object variables
falling_objects_width = 50
falling_objects_height = 50
falling_objects_speed = 2
falling_objects_list = []


# Function to create a falling object
def create_falling_object():
    falling_object = random.choice(falling_objects)
    falling_image = falling_object["image"]
    falling_image = pygame.transform.scale(falling_image, (falling_objects_width, falling_objects_height))
    falling_x = random.randint(0, screen_width - falling_objects_width)
    falling_y = -falling_objects_height
    return {
        "image": falling_image,
        "score": falling_object["score"],
        "x": falling_x,
        "y": falling_y
    }


# More set-up variables
score = 10  # initialized at 10
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()
game_over = False


# Function to handle collisions between falling objects and player
def handle_collision(falling_object):
    global score, game_over

    if falling_object["score"] == -9999:
        game_over = True
    else:
        score += falling_object["score"]

# Game loop
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    # Move the player left or right
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= 5
    if keys[pygame.K_RIGHT] and player_x < screen_width - player_width:
        player_x += 5

    # Update the falling objects' positions
    for falling_object in falling_objects_list:
        falling_object["y"] += falling_objects_speed
        if player_x < falling_object["x"] + falling_objects_width and player_x + player_width > falling_object["x"] and \
                player_y < falling_object["y"] + falling_objects_height and player_y + player_height > falling_object["y"]:
            handle_collision(falling_object)
            falling_objects_list.remove(falling_object)

    # Check if any falling objects reached the bottom
    for falling_object in falling_objects_list:
        if falling_object["y"] > screen_height:
            falling_objects_list.remove(falling_object)

    # Create new falling objects based on their frequencies
    for falling_object in falling_objects:
        if random.randint(1, falling_object["frequency"]) == 1:
            falling_objects_list.append(create_falling_object())

    # Display everything on the screen
    screen.fill(WHITE)
    screen.blit(player_image, (player_x, player_y))
    for falling_object in falling_objects_list:
        screen.blit(falling_object["image"], (falling_object["x"], falling_object["y"]))

    # Display the score
    score_text = font.render("Score: " + str(score), True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

    # Check for game over
    if score <= 0:
        game_over = True


# Game over message
game_over_text = font.render("Game Over", True, (255, 0, 0))
game_over_text_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 2))
screen.blit(game_over_text, game_over_text_rect)
pygame.display.flip()

