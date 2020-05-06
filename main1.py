from random import randint
import pygame
pygame.init()

game_width = 600
game_height = 600

game_window = pygame.display.set_mode((game_width, game_height))
pygame.display.set_caption('Space Invader')
bg = [pygame.image.load('img\\bg1.jpg'), pygame.image.load('img\\bg2.jpg'),
      pygame.image.load('img\\bg3.jpg'), pygame.image.load('img\\bg4.jpg'),
      pygame.image.load('img\\bg5.jpg'), pygame.image.load('img\\bg6.jpg'),
      pygame.image.load('img\\bg7.jpg'), pygame.image.load('img\\bg8.jpg'),
      pygame.image.load('img\\bg9.jpg'), pygame.image.load('img\\bg10.jpg'),
      pygame.image.load('img\\bg11.jpg'), pygame.image.load('img\\bg12.jpg')]

ship1 = pygame.image.load('img\\player.png')
ship2 = pygame.image.load('img\\enemy.png')
life = pygame.image.load('img\\life.png')
fire = pygame.mixer.Sound('sounds\\bulletFire.wav')
blast = pygame.mixer.Sound('sounds\\blast.wav')
lostLife = pygame.mixer.Sound('sounds\\lifeLost.wav')
music1 = pygame.mixer.music.load('sounds\\music.mp3')
pygame.mixer.music.play(-1)
clock = pygame.time.Clock()


class Player:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.hitBox = (self.x + 5, self.y + 5, self.width - 10, self.height - 10)
        self.lifeCount = 3
        self.score = 0

    def draw(self):
        for i in range(self.lifeCount):
            game_window.blit(life, (30 + (i * 40), 30))
        game_window.blit(ship1, (self.x, self.y))
        self.hitBox = (self.x + 5, self.y + 5, self.width - 10, self.height - 10)


class Enemy:
    def __init__(self, max_x, y, width, height):
        self.x = randint(0, max_x)
        self.y = y
        self.width = width
        self.height = height
        self.vel = 4
        self.hitBox = (self.x + 5, self.y + 5, self.width - 10, self.height - 10)
        self.isVisible = True

    def draw_enemy(self):
        if self.isVisible:
            game_window.blit(ship2, (self.x, self.y))
            self.y += self.vel
            self.hitBox = (self.x + 5, self.y + 5, self.width - 10, self.height - 10)


class Projectile:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.vel = 8

    def draw_bullet(self):
        pygame.draw.circle(game_window, self.color, (self.x, self.y), self.radius)


def draw_game_window():
    global bg_count
    if bg_count >= 36:
        bg_count = 0
    game_window.blit(bg[bg_count // 3], (0, 0))
    bg_count += 1
    guardian.draw()
    file2 = open('textforhc\\highScore.txt', 'r')
    high_score = int(file2.read())
    file2.close()
    text_h_score = font.render('High Score: ' + str(high_score), 1, (120, 0, 120))
    game_window.blit(text_h_score, (game_width - text_h_score.get_width() - 5, 50))
    if high_score < guardian.score:
        score_color = (0, 120, 0)
    else:
        score_color = (120, 120, 120)
    text = font.render('Score: ' + str(guardian.score), 1, score_color)
    game_window.blit(text, (game_width - 140, 30))
    for rounds in bullets:
        rounds.draw_bullet()
    invader.draw_enemy()
    if not invader.isVisible:
        invader.draw_enemy()
        invader.__init__(game_width - 64, 0, 64, 64)
    pygame.draw.line(game_window, (200, 0, 0), (0, game_height), (game_width, game_height), 8)
    pygame.display.update()


guardian = Player(game_width // 2 - 32, game_height - 90, 64, 71)
bullets = []
bg_count = 0
shoot_loop = 0
intro = 0
invader = Enemy(game_width - 64, 0, 64, 64)
font = pygame.font.SysFont('comicsans', 30, True)

'# main loop'
run = True
while run:
    clock.tick(36)
    if shoot_loop > 0:
        shoot_loop += 1
    if shoot_loop > 4:
        shoot_loop = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    for bullet in bullets:
        if invader.hitBox[1] + invader.hitBox[3] - 10 > bullet.y > invader.hitBox[1] and \
                invader.isVisible:
            if invader.hitBox[0] < bullet.x < invader.hitBox[2] + invader.hitBox[0]:
                invader.isVisible = False
                guardian.score += 5
                blast.play()
                bullets.pop(bullets.index(bullet))
        if bullet.y >= 0:
            bullet.y -= bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    if guardian.hitBox[1] < invader.hitBox[1] + invader.hitBox[3] \
            < guardian.hitBox[1] + guardian.hitBox[3]:
        if guardian.hitBox[0] < invader.hitBox[0] < guardian.hitBox[0] + guardian.hitBox[2] \
            or guardian.hitBox[0] < invader.hitBox[0] + invader.hitBox[2] <\
                guardian.hitBox[0] + guardian.hitBox[2]:
            invader.isVisible = False
            lostLife.play()
            guardian.x = game_width // 2 - 32
            guardian.y = game_height - 90
            guardian.lifeCount -= 1
    elif invader.hitBox[1] > game_height:
        invader.isVisible = False
        lostLife.play()
        guardian.x = game_width // 2 - 32
        guardian.y = game_height - 90
        guardian.lifeCount -= 1

    keys = pygame.key.get_pressed()

    if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and guardian.x + guardian.width + guardian.vel < game_width:
        guardian.x += guardian.vel
    elif (keys[pygame.K_LEFT] or keys[pygame.K_a])and guardian.x - guardian.vel > 0:
        guardian.x -= guardian.vel

    if (keys[pygame.K_UP] or keys[pygame.K_w])and shoot_loop == 0:
        if len(bullets) < 6:
            fire.play()
            bullets.append(Projectile(guardian.x + guardian.width // 2, guardian.y, 6, (120, 0, 0)))
        shoot_loop = 1
    if guardian.lifeCount == 0:
        bullets = []
        file = open('textforhc\\highScore.txt', 'r')
        if guardian.score > int(file.read()):
            file1 = open('textforhc\\highScore.txt', 'w')
            file1.write(str(guardian.score))
            file1.close()
        file.close()
        text2 = font.render('Game Over! Restarting...', 1, (120, 0, 0))
        game_window.blit(text2, (game_width//2 - text2.get_width()//2, game_height//2))
        pygame.display.update()
        pygame.time.delay(2000)
        guardian.__init__(game_width // 2 - 32, game_height - 90, 64, 71)
    if guardian.lifeCount == 3 and intro == 0:
        text2 = font.render("""SPACE INVADER. Starting...""", 1, (100, 0, 120))
        game_window.blit(bg[0], (0, 0))
        game_window.blit(text2, (game_width//2 - text2.get_width()//2, game_height//2))
        pygame.display.update()
        pygame.time.delay(2000)
        intro = 1
    draw_game_window()

pygame.quit()
