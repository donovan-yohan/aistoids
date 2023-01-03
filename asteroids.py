import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Set the window size
WIDTH, HEIGHT = 1280, 960

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Set the icon of the window
pygame.display.set_icon(pygame.image.load("icon.png"))

# Set the title of the window
pygame.display.set_caption("aistoids")

# Load the player image
player_image = pygame.image.load("player.png")

# Load the asteroid image
asteroid_image = pygame.image.load("asteroid.png")

# Load the bullet image
bullet_image = pygame.image.load("bullet.png")

# Set the initial player health
player_health = 10

# Set the initial player position
player_pos = [WIDTH/2, HEIGHT/2]

# Set the initial player velocity
player_vel = [0, 0]

# Set the player acceleration
player_acc = 0.2

# Set the player friction
player_friction = 0.99

# Set the player rotation speed
player_rotation_speed = 3

# Set the player's maximum speed
player_max_speed = 5

# Set the initial player angle (in degrees)
player_angle = 0

# Set the initial player bullet cooldown
player_bullet_cooldown = 0

# Set the player bullet cooldown time
player_bullet_cooldown_time = 30

# Set the player bullet speed
player_bullet_speed = 10

# Set the player bullet lifespan
player_bullet_lifespan = 70

# Set the player bullet damage
player_bullet_damage = 5

# Set the initial player rotation flags
rotate_left = False
rotate_right = False

# Set the initial player acceleration flag
accelerate = False

# Set the initial asteroid spawn rate
asteroid_spawn_rate = 0
asteroid_initial_spawn_rate = 200

# Set the asteroid minimum speed
asteroid_min_speed = 1

# Set the asteroid maximum speed
asteroid_max_speed = 3

# Set the asteroid minimum size
asteroid_min_size = 30

# Set the asteroid maximum size
asteroid_max_size = 175

# Set the asteroid health
asteroid_health = 100

# Set the asteroid damage
asteroid_damage = 10

# Set the asteroid score value
asteroid_score_value = 100

# Set the game font
game_font = pygame.font.Font(None, 36)

# Set the game over font
game_over_font = pygame.font.Font(None, 72)

# Set the game over message
game_over_message = game_over_font.render("Game Over", True, (255, 255, 255))

# Set the game over message rectangle
game_over_rect = game_over_message.get_rect()
game_over_rect.center = (WIDTH/2, HEIGHT/2)

# Create a list to store the player bullets
player_bullets = []

# Create a list to store the asteroids
asteroids = []

# Set the game score
score = 0

# Set the game over flag
game_over = False

# Set the clock
clock = pygame.time.Clock()

# Main game loop
while not game_over:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_over = True
            elif event.key == pygame.K_UP:
                accelerate = True
            elif event.key == pygame.K_LEFT:
                rotate_left = True
            elif event.key == pygame.K_RIGHT:
                rotate_right = True
            elif event.key == pygame.K_SPACE:
                # Fire a bullet if the player's bullet cooldown is 0
                if player_bullet_cooldown == 0:
                    # Calculate the bullet's starting position
                    bullet_x = player_pos[0] + math.cos(math.radians(player_angle))*30
                    bullet_y = player_pos[1] + math.sin(math.radians(player_angle))*30
                    # Create the new bullet
                    new_bullet = [bullet_x, bullet_y, player_angle, player_bullet_lifespan]
                    player_bullets.append(new_bullet)
                    # Reset the player's bullet cooldown
                    player_bullet_cooldown = player_bullet_cooldown_time
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                rotate_left = False
            elif event.key == pygame.K_RIGHT:
                rotate_right = False
            elif event.key == pygame.K_UP:
                accelerate = False

    # Update the player angle
    if rotate_left:
        player_angle += player_rotation_speed
    if rotate_right:
        player_angle -= player_rotation_speed

    # Update the player velocity
    if accelerate:
        # Calculate the acceleration in the x and y directions
        acc_x = math.cos(math.radians(player_angle)) * player_acc
        acc_y = math.sin(math.radians(player_angle)) * player_acc
        # Add the acceleration to the velocity
        player_vel[0] += acc_x
        player_vel[1] -= acc_y
    
    # Update the player position based on their velocity
    player_pos[0] += player_vel[0]
    player_pos[1] += player_vel[1]

    # Wrap the player around the screen if they go off the edges
    if player_pos[0] < 0:
        player_pos[0] = WIDTH
    elif player_pos[0] > WIDTH:
        player_pos[0] = 0
    if player_pos[1] < 0:
        player_pos[1] = HEIGHT
    elif player_pos[1] > HEIGHT:
        player_pos[1] = 0

    # Apply friction to the player velocity
    player_vel[0] *= player_friction
    player_vel[1] *= player_friction

    # Limit the player's maximum speed
    speed = math.sqrt(player_vel[0]**2 + player_vel[1]**2)
    if speed > player_max_speed:
        player_vel[0] *= player_max_speed/speed
        player_vel[1] *= player_max_speed/speed

    # Decrement the player's bullet cooldown
    if player_bullet_cooldown > 0:
        player_bullet_cooldown -= 1

    # Update the bullet positions and lifespans
    for bullet in player_bullets:
        # Calculate the bullet's new position
        angle_rad = math.radians(bullet[2])
        bullet[0] += player_bullet_speed * math.cos(angle_rad)
        bullet[1] -= player_bullet_speed * math.sin(angle_rad)

        # Decrement the bullet lifespan
        bullet[3] -= 1

        # Remove the bullet if its lifespan is 0
        if bullet[3] <= 0:
            player_bullets.remove(bullet)

    # Spawn a new asteroid if the asteroid spawn rate is 0
    if asteroid_spawn_rate == 0:
        # Choose a random edge of the screen to spawn the asteroid from
        edge = random.randint(1, 4)
        if edge == 1:  # Top edge
            x = random.randint(0, WIDTH)
            y = 0
        elif edge == 2:  # Right edge
            x = WIDTH
            y = random.randint(0, HEIGHT)
        elif edge == 3:  # Bottom edge
            x = random.randint(0, WIDTH)
            y = HEIGHT
        else:  # Left edge
            x = 0
            y = random.randint(0, HEIGHT)
        # Choose a random speed and size for the asteroid
        speed = random.uniform(asteroid_min_speed, asteroid_max_speed)
        size = random.randint(asteroid_min_size, asteroid_max_size)
        # Calculate the angle to the player
        dx = player_pos[0] - x
        dy = player_pos[1] - y
        angle = math.atan2(dx, dy)
        # Create the new asteroid
        new_asteroid = [x, y, angle, speed, size * 0.8, size / 10, pygame.transform.scale(asteroid_image, (size, size)), size / 10]
        asteroids.append(new_asteroid)
        # Reset the asteroid spawn rate
        asteroid_spawn_rate = asteroid_initial_spawn_rate - score
    else:
        # Decrement the asteroid spawn rate
        asteroid_spawn_rate -= 1

    # Update the asteroid positions
    for asteroid in asteroids:
        # Calculate the asteroid's new position
        asteroid[0] += asteroid[3] * math.sin(asteroid[2])
        asteroid[1] += asteroid[3] * math.cos(asteroid[2])

    # Check for collisions between bullets and asteroids
    for bullet in player_bullets:
        for asteroid in asteroids:
            # Calculate the distance between the bullet and the asteroid
            dx = bullet[0] - asteroid[0]
            dy = bullet[1] - asteroid[1]
            distance = math.sqrt(dx**2 + dy**2)
            # Check if the bullet and asteroid are colliding
            if distance < asteroid[4]:
                # Decrement the asteroid's health
                asteroid[5] -= player_bullet_damage
                # Remove the bullet
                player_bullets.remove(bullet)
                # Check if the asteroid is destroyed
                if asteroid[5] <= 0:
                    # Add the asteroid's health value to the game score
                    score += (math.floor(asteroid[7] / 5) + 1) * 5
                    # Remove the asteroid
                    asteroids.remove(asteroid)

    # Check for collisions between the player and asteroids
    for asteroid in asteroids:
        # Calculate the distance between the player and the asteroid
        dx = player_pos[0] - asteroid[0]
        dy = player_pos[1] - asteroid[1]
        distance = math.sqrt(dx**2 + dy**2)
        # Check if the player and asteroid are colliding
        if distance < asteroid[4]:
            # Decrement the player's health
            player_health -= asteroid_damage
            # Remove the asteroid
            asteroids.remove(asteroid)
            # Check if the player is dead
            if player_health <= 0:
                game_over = True

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw the player
    rotated_player_image = pygame.transform.rotate(player_image, player_angle)
    rect = rotated_player_image.get_rect()
    rect.center = player_pos
    screen.blit(rotated_player_image, rect)

    # Draw the asteroids
    for asteroid in asteroids:
        rect = pygame.Rect(0, 0, asteroid[4], asteroid[4])
        rect.center = (asteroid[0], asteroid[1])
        screen.blit(asteroid[6], rect)

    # Draw the bullets
    for bullet in player_bullets:
        rect = pygame.Rect(0, 0, 10, 10)
        rect.center = (bullet[0], bullet[1])
        screen.blit(bullet_image, rect)

    # Draw the score
    score_message = game_font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(score_message, (5, 5))

    # Draw the game over message if the game is over
    if game_over:
        screen.blit(game_over_message, game_over_rect)

    # Update the display
    pygame.display.flip()

    # Limit the frame rate
    clock.tick(60)

# Close the window
pygame.quit()
