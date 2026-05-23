from pygame import *

#SCORE#
score_left = 0
score_right = 0

#SPRITES#
class GameSprite(sprite.Sprite):
    def __init__(self, color, x, y, speed, width, height):
        super().__init__()
        self.width = width
        self.height = height
        self.image = Surface((self.width, self.height))
        self.image.fill(color)
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player1(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()

        if (keys_pressed[K_w]) and self.rect.y > 5:
            self.rect.y -= self.speed

        if (keys_pressed[K_s]) and self.rect.y < 400:
            self.rect.y += self.speed


class Player2(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()

        if (keys_pressed[K_UP]) and self.rect.y > 5:
            self.rect.y -= self.speed

        if (keys_pressed[K_DOWN]) and self.rect.y < 400:
            self.rect.y += self.speed


class Ball(GameSprite):
    def __init__(self, color, x, y, speed_x, speed_y, width, height):
        super().__init__(color, x, y, 0, width, height)
        self.speed_x = speed_x
        self.speed_y = speed_y

    def update(self):
        global score_left
        global score_right

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Bounce off top and bottom walls
        if self.rect.y <= 0 or self.rect.y >= 480:
            self.speed_y *= -1

        # Left player misses
        if self.rect.x <= 0:
            score_right += 1
            self.rect.x = 350
            self.rect.y = 250
            self.speed_x *= -1

        # Right player misses
        if self.rect.x >= 680:
            score_left += 1
            self.rect.x = 350
            self.rect.y = 250
            self.speed_x *= -1


#SETUP#
width = 700
height = 500

window = display.set_mode((width, height))
display.set_caption("Ping Pong")

background = Surface((width, height))
background.fill((0, 0, 0))

clock = time.Clock()
FPS = 60

#MUSIC#
mixer.init()
mixer.music.load("bgm.mp3")
mixer.music.play()

#TEXT#s
font.init()
style = font.SysFont('Arial', 36)

txt_win_left = style.render("LEFT PLAYER WINS!", True, (255, 255, 255))
txt_win_right = style.render("RIGHT PLAYER WINS!", True, (255, 255, 255))

#SPRITES#
paddle_left = Player1((255, 255, 255), 30, 200, 7, 20, 100)
paddle_right = Player2((255, 255, 255), 650, 200, 7, 20, 100)

ball = Ball((255, 255, 255), 350, 250, 5, 5, 20, 20)

#GAME LOOP#
game = True
finish = False

while game:

    for e in event.get():
        if e.type == QUIT:
            game = False

    if finish != True:

        window.blit(background, (0, 0))

        # Draw middle line
        draw.line(window, (255, 255, 255), (350, 0), (350, 500), 5)

        # Update sprites
        paddle_left.update()
        paddle_right.update()
        ball.update()

        # Ball collision with paddles
        if sprite.collide_rect(ball, paddle_left) or sprite.collide_rect(ball, paddle_right):
            ball.speed_x *= -1

        # Draw sprites
        paddle_left.reset()
        paddle_right.reset()
        ball.reset()

        # Score text
        text_score = style.render(str(score_left) + " : " + str(score_right), 1, (255, 255, 255))
        window.blit(text_score, (310, 20))

        # Win conditions
        if score_left >= 5:
            window.blit(txt_win_left, (180, 230))
            finish = True

        if score_right >= 5:
            window.blit(txt_win_right, (160, 230))
            finish = True

        clock.tick(FPS)
        display.update()
