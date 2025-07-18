import pygame, sys, random

pygame.init()
WIDTH, HEIGHT = 800, 600
WHITE, BLACK = (255,255,255), (0,0,0)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Pong Dirty")

font = pygame.font.SysFont(None, 36)

ball = pygame.Rect(WIDTH//2, HEIGHT//2, 20, 20)
player = pygame.Rect(WIDTH - 20, HEIGHT//2 - 50, 10, 100)
opponent = pygame.Rect(10, HEIGHT//2 - 50, 10, 100)

ball_speed_x = 5 * random.choice([-1, 1])
ball_speed_y = 5 * random.choice([-1, 1])
player_speed = 0
opponent_speed = 5

player_score = 0
opponent_score = 0
win_score = 7
game_over = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: pygame.quit(); sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP: player_speed = -7
            if event.key == pygame.K_DOWN: player_speed = 7
            if event.key == pygame.K_r and game_over:
                ball.center = (WIDTH//2, HEIGHT//2)
                player_score = opponent_score = 0
                ball_speed_x = 5 * random.choice([-1, 1])
                ball_speed_y = 5 * random.choice([-1, 1])
                game_over = False
        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_UP, pygame.K_DOWN): player_speed = 0

    if not game_over:
        ball.x += ball_speed_x
        ball.y += ball_speed_y

        player.y += player_speed
        player.y = max(0, min(player.y, HEIGHT - 100))

        if opponent.centery < ball.centery: opponent.y += opponent_speed
        if opponent.centery > ball.centery: opponent.y -= opponent_speed
        opponent.y = max(0, min(opponent.y, HEIGHT - 100))

        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_speed_y *= -1

        if ball.colliderect(player) or ball.colliderect(opponent):
            ball_speed_x *= -1
            ball_speed_x = max(min(ball_speed_x * 1.1, 12), -12)

        if ball.left <= 0:
            player_score += 1
            ball.center = (WIDTH//2, HEIGHT//2)
            ball_speed_x *= random.choice([-1, 1])
        if ball.right >= WIDTH:
            opponent_score += 1
            ball.center = (WIDTH//2, HEIGHT//2)
            ball_speed_x *= random.choice([-1, 1])

        if player_score == win_score or opponent_score == win_score:
            game_over = True

    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, player)
    pygame.draw.rect(screen, WHITE, opponent)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.aaline(screen, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT))

    score_text = font.render(f"{opponent_score}  {player_score}", True, WHITE)
    screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 20))

    if game_over:
        win_text = font.render("YOU WIN!" if player_score == win_score else "YOU LOSE", True, WHITE)
        screen.blit(win_text, (WIDTH//2 - win_text.get_width()//2, HEIGHT//2 - 20))
        restart = font.render("Press R to Restart", True, WHITE)
        screen.blit(restart, (WIDTH//2 - restart.get_width()//2, HEIGHT//2 + 30))

    pygame.display.flip()
    clock.tick(60)