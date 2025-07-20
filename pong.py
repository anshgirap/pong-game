import pygame, sys, random, os

# === Initialization ===
pygame.init()
WIDTH, HEIGHT = 800, 600
WHITE, BLACK = (255, 255, 255), (0, 0, 0)
GREEN, RED = (0, 255, 0), (255, 0, 0)
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
BALL_SIZE = 20
BALL_SPEED = 5
PADDLE_SPEED = 7
OPPONENT_SPEED = 4
WIN_SCORE = 7

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")
clock = pygame.time.Clock()

font_path = os.path.join("assets", "PressStart2P.ttf")
font = pygame.font.Font(font_path, 16)

# === Game Objects ===
player = pygame.Rect(WIDTH - 20, HEIGHT // 2 - 50, PADDLE_WIDTH, PADDLE_HEIGHT)
opponent = pygame.Rect(10, HEIGHT // 2 - 50, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)

ball_speed_x = BALL_SPEED * random.choice([-1, 1])
ball_speed_y = BALL_SPEED * random.choice([-1, 1])
player_score = 0
opponent_score = 0
player_speed = 0
game_over = False

# === Glow Surface ===
glow_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
for i in range(0, WIDTH, 10):
    for j in range(0, HEIGHT, 10):
        dist = ((i - WIDTH // 2) ** 2 + (j - HEIGHT // 2) ** 2) ** 0.5
        brightness = max(0, 255 - int(dist * 0.5))
        glow_surface.fill((brightness, brightness, brightness, 4), pygame.Rect(i, j, 10, 10))  # softer CRT glow

# === Functions ===
def draw():
    screen.fill(BLACK)

    if not game_over:
        # Game in progress visuals
        pygame.draw.rect(screen, WHITE, player)
        pygame.draw.rect(screen, WHITE, opponent)
        pygame.draw.ellipse(screen, WHITE, ball)
        pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

        score_text = font.render(f"{opponent_score}   {player_score}", True, WHITE)
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))

        screen.blit(glow_surface, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

    else:
        # Black screen for win/lose
        screen.fill(BLACK)
        if player_score == WIN_SCORE:
            win_text = font.render("YOU WIN!", False, GREEN)
        else:
            win_text = font.render("YOU LOSE", False, RED)
        screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2 - 20))

        restart = font.render("Press R to Restart", True, WHITE)
        screen.blit(restart, (WIDTH // 2 - restart.get_width() // 2, HEIGHT // 2 + 30))

    pygame.display.flip()

def reset_ball():
    global ball_speed_x, ball_speed_y
    ball.center = (WIDTH // 2, HEIGHT // 2)
    ball_speed_x = BALL_SPEED * random.choice([-1, 1])
    ball_speed_y = BALL_SPEED * random.choice([-1, 1])

def handle_input(event):
    global player_speed, game_over, player_score, opponent_score
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
            player_speed = -PADDLE_SPEED
        if event.key == pygame.K_DOWN:
            player_speed = PADDLE_SPEED
        if event.key == pygame.K_r and game_over:
            reset_ball()
            player_score = opponent_score = 0
            game_over = False
    if event.type == pygame.KEYUP:
        if event.key in (pygame.K_UP, pygame.K_DOWN):
            player_speed = 0

def move_opponent():
    if abs(opponent.centery - ball.centery) > 10:
        if opponent.centery < ball.centery:
            opponent.y += OPPONENT_SPEED
        elif opponent.centery > ball.centery:
            opponent.y -= OPPONENT_SPEED
    opponent.y = max(0, min(opponent.y, HEIGHT - PADDLE_HEIGHT))

def check_collision():
    global ball_speed_x, ball_speed_y
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y *= -1
    if ball.colliderect(player) or ball.colliderect(opponent):
        ball_speed_x *= -1
        ball_speed_x = max(min(ball_speed_x * 1.1, 12), -12)

# === Game Loop ===
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        handle_input(event)

    if not game_over:
        player.y += player_speed
        player.y = max(0, min(player.y, HEIGHT - PADDLE_HEIGHT))

        move_opponent()

        ball.x += ball_speed_x
        ball.y += ball_speed_y

        check_collision()

        if ball.left <= 0:
            player_score += 1
            reset_ball()
        if ball.right >= WIDTH:
            opponent_score += 1
            reset_ball()

        if player_score == WIN_SCORE or opponent_score == WIN_SCORE:
            game_over = True

    draw()
    clock.tick(60)