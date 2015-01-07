import os
import sys
import math
import time
import pygame
current_path = os.getcwd()
sys.path.insert(0, os.path.join(current_path, "../pymunk-4.0.0"))
import pymunk as pm
from pymunk import Vec2d
from pymunk.pygame_util import from_pygame
from characters import Bird
from level import Level


pygame.init()
screen = pygame.display.set_mode((1200, 650))
redbird = pygame.image.load("../resources/images/red-bird3.png").convert_alpha()
background2 = pygame.image.load(
    "../resources/images/background3.png").convert_alpha()
sling_image = pygame.image.load(
    "../resources/images/sling-3.png").convert_alpha()
full_sprite = pygame.image.load(
    "../resources/images/full-sprite.png").convert_alpha()
rect = pygame.Rect(181, 1050, 50, 50)
cropped = full_sprite.subsurface(rect).copy()
pig_image = pygame.transform.scale(cropped, (30, 30))
buttons = pygame.image.load(
    "../resources/images/selected-buttons.png").convert_alpha()
pig_happy = pygame.image.load(
    "../resources/images/pig_failed.png").convert_alpha()
stars = pygame.image.load(
    "../resources/images/stars-edited.png").convert_alpha()
rect = pygame.Rect(0, 0, 200, 200)
star1 = stars.subsurface(rect).copy()
rect = pygame.Rect(204, 0, 200, 200)
star2 = stars.subsurface(rect).copy()
rect = pygame.Rect(426, 0, 200, 200)
star3 = stars.subsurface(rect).copy()
rect = pygame.Rect(164, 10, 60, 60)
pause_button = buttons.subsurface(rect).copy()
rect = pygame.Rect(24, 4, 100, 100)
replay_button = buttons.subsurface(rect).copy()
rect = pygame.Rect(142, 365, 130, 100)
next_button = buttons.subsurface(rect).copy()
clock = pygame.time.Clock()
rect = pygame.Rect(18, 212, 100, 100)
play_button = buttons.subsurface(rect).copy()
clock = pygame.time.Clock()
running = True
# the base of the physics
space = pm.Space()
space.gravity = (0.0, -700.0)
pigs = []
birds = []
balls = []
polys = []
beams = []
columns = []
poly_points = []
ball_number = 0
polys_dict = {}
mouse_distance = 0
rope_lenght = 90
angle = 0
x_mouse = 0
y_mouse = 0
count = 0
mouse_pressed = False
t1 = 0
tick_to_next_circle = 10
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
sling_x, sling_y = 135, 450
sling2_x, sling2_y = 160, 450
score = 0
game_state = 0
number_level = 0
bird_path = []
counter = 0
restart_counter = False
bonus_score_once = True

# walls
static_body = pm.Body()
static_lines = [pm.Segment(static_body, (0.0, 060.0), (1200.0, 060.0), 0.0)]
for line in static_lines:
    line.elasticity = 0.95
    line.friction = 1
    line.collision_type = 3
space.add(static_lines)


def to_pygame(p):
    """Convert pymunk to pygame coordinates"""
    return int(p.x), int(-p.y+600)


def vector(p0, p1):
    """Return the vector of the points"""
    "(xo,yo), (x1,y1)"
    a = p1[0] - p0[0]
    b = p1[1] - p0[1]
    return (a, b)


def unit_vector(v):
    """Return the unit vector of the points"""
    "(a,b)"
    h = ((v[0]**2)+(v[1]**2))**0.5
    if h == 0:
        h = 0.000000000000001
    ua = v[0] / h
    ub = v[1] / h
    return (ua, ub)


def distance(xo, yo, x, y):
    """distance between points"""
    dx = x - xo
    dy = y - yo
    d = ((dx ** 2) + (dy ** 2)) ** 0.5
    return d


def load_music():
    """Load the musics of a list"""
    song1 = '../resources/sounds/angry-birds.mp3'
    pygame.mixer.music.load(song1)
    pygame.mixer.music.play(-1)


def sling_action():
    """Set up sling behavior"""
    global mouse_distance
    global rope_lenght
    global angle
    global x_mouse
    global y_mouse
    # Fixing bird to the sling rope
    v = vector((sling_x, sling_y), (x_mouse, y_mouse))
    uv = unit_vector(v)
    uv1 = uv[0]
    uv2 = uv[1]
    mouse_distance = distance(sling_x, sling_y, x_mouse, y_mouse)
    pu = (uv1*rope_lenght+sling_x, uv2*rope_lenght+sling_y)
    bigger_rope = 102
    x_redbird = x_mouse - 20
    y_redbird = y_mouse - 20
    if mouse_distance > rope_lenght:
        pux, puy = pu
        pux -= 20
        puy -= 20
        pul = pux, puy
        screen.blit(redbird, pul)
        pu2 = (uv1*bigger_rope+sling_x, uv2*bigger_rope+sling_y)
        pygame.draw.line(screen, (0, 0, 0), (sling2_x, sling2_y), pu2, 5)
        screen.blit(redbird, pul)
        pygame.draw.line(screen, (0, 0, 0), (sling_x, sling_y), pu2, 5)
    else:
        mouse_distance += 10
        pu3 = (uv1*mouse_distance+sling_x, uv2*mouse_distance+sling_y)
        pygame.draw.line(screen, (0, 0, 0), (sling2_x, sling2_y), pu3, 5)
        screen.blit(redbird, (x_redbird, y_redbird))
        pygame.draw.line(screen, (0, 0, 0), (sling_x, sling_y), pu3, 5)
    # Angle of impulse
    dy = y_mouse - sling_y
    dx = x_mouse - sling_x
    if dx == 0:
        dx = 0.00000000000001
    angle = math.atan((float(dy))/dx)


def restart():
    pigs_to_remove = []
    birds_to_remove = []
    columns_to_remove = []
    beams_to_remove = []
    for pig in pigs:
        pigs_to_remove.append(pig)
    for pig in pigs_to_remove:
        space.remove(pig.shape, pig.shape.body)
        pigs.remove(pig)
    for bird in birds:
        birds_to_remove.append(bird)
    for bird in birds_to_remove:
        space.remove(bird.shape, bird.shape.body)
        birds.remove(bird)
    for column in columns:
        columns_to_remove.append(column)
    for column in columns_to_remove:
        space.remove(column.shape, column.shape.body)
        columns.remove(column)
    for beam in beams:
        beams_to_remove.append(beam)
    for beam in beams_to_remove:
        space.remove(beam.shape, beam.shape.body)
        beams.remove(beam)


def post_solve_bird_pig(space, arbiter, surface=screen):
    """Collision between bird and pig"""
    a, b = arbiter.shapes
    bird_body = a.body
    pig_body = b.body
    p = to_pygame(bird_body.position)
    p2 = to_pygame(pig_body.position)
    r = 30
    pygame.draw.circle(surface, BLACK, p, r, 4)
    pygame.draw.circle(surface, RED, p2, r, 4)
    pigs_to_remove = []
    for pig in pigs:
        if pig_body == pig.body:
            pig.life -= 20
            pigs_to_remove.append(pig)
            global score
            score += 10000
    for pig in pigs_to_remove:
        space.remove(pig.shape, pig.shape.body)
        pigs.remove(pig)


def post_solve_bird_wood(space, arbiter):
    """Collision between bird and wood"""
    poly_to_remove = []
    if arbiter.total_impulse.length > 1100:
        a, b = arbiter.shapes
        for column in columns:
            if b == column.shape:
                poly_to_remove.append(column)
        for beam in beams:
            if b == beam.shape:
                poly_to_remove.append(beam)
        for poly in poly_to_remove:
            if poly in columns:
                columns.remove(poly)
            if poly in beams:
                beams.remove(poly)
        space.remove(b, b.body)
        global score
        score += 5000


def post_solve_pig_wood(space, arbiter):
    """Collision between pig and wood"""
    pigs_to_remove = []
    if arbiter.total_impulse.length > 700:
        pig_shape, wood_shape = arbiter.shapes
        for pig in pigs:
            if pig_shape == pig.shape:
                pig.life -= 20
                global score
                score += 10000
                if pig.life <= 0:
                    pigs_to_remove.append(pig)
    for pig in pigs_to_remove:
        space.remove(pig.shape, pig.shape.body)
        pigs.remove(pig)


# bird and pigs
space.add_collision_handler(0, 1, post_solve=post_solve_bird_pig)
# bird and wood
space.add_collision_handler(0, 2, post_solve=post_solve_bird_wood)
# pig and wood
space.add_collision_handler(1, 2, post_solve=post_solve_pig_wood)
load_music()
level = Level(pigs, columns, beams, space)
level.load_level(number_level)

while running:
    # Input handling
    x_mouse , y_mouse = pygame.mouse.get_pos()
    # Getting mouse position
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
        if pygame.mouse.get_pressed()[0] and x_mouse > 100 and x_mouse < 250 and y_mouse > 370 and y_mouse < 550:
            mouse_pressed = True
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and mouse_pressed:
            if game_state == 0:
                level.number_of_birds -= 1
            mouse_pressed = False
            t1 = time.time()
            xo = 154
            yo = 156
            if mouse_distance > rope_lenght:
                mouse_distance = rope_lenght
            if x_mouse < sling_x+5:
                bird = Bird(mouse_distance, angle, xo, yo, space)
                birds.append(bird)
            else:
                bird = Bird(-mouse_distance, angle, xo, yo, space)
                birds.append(bird)
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if x_mouse < 60 and y_mouse < 155 and y_mouse > 90:
                 game_state = 1
            if game_state == 1:
                if x_mouse > 500 and y_mouse > 200 and y_mouse < 300:
                    game_state = 0
                if x_mouse> 500 and y_mouse > 300:
                    restart()
                    level.load_level(number_level)
                    game_state = 0
                    bird_path = []
            if game_state == 3:
                if x_mouse > 500 and x_mouse < 620 and y_mouse > 450:
                    restart()
                    level.load_level(number_level)
                    game_state = 0
                    bird_path = []
                    score = 0
            if game_state == 4:
                if  x_mouse > 610 and y_mouse > 450:
                    restart()
                    number_level += 1
                    game_state = 0
                    level.load_level(number_level)
                    score = 0
                    bird_path = []
                    bonus_score_once = True
                    if level.no_more_level:
                        number_level = 0
                        level.no_more_level = False
                if  x_mouse < 610 and x_mouse > 500 and y_mouse > 450:
                    restart()
                    level.load_level(number_level)
                    game_state = 0
                    bird_path = []
                    score = 0
    # Drawing background
    screen.fill((130, 200, 100))
    screen.blit(background2, (0, -50))
    rect = pygame.Rect(50, 0, 70, 220)
    screen.blit(sling_image, (138, 420), rect)
    for point in bird_path:
        pygame.draw.circle(screen, WHITE, point, 5, 0)
    if mouse_pressed:
        sling_action()
    else:
        if time.time() - t1 > 1:
            screen.blit(redbird, (130, 426))
        else:
            pygame.draw.line(screen, (0, 0, 0), (sling_x, sling_y-8),
                             (sling2_x, sling2_y-7), 5)
    birds_to_remove = []
    pigs_to_remove = []
    counter += 1
    for bird in birds:
        if bird.shape.body.position.y < 0:
            birds_to_remove.append(bird)
        p = to_pygame(bird.shape.body.position)
        x, y = p
        x -= 22
        y -= 20
        screen.blit(redbird, (x, y))
        pygame.draw.circle(screen, BLUE,
                           p, int(bird.shape.radius), 2)
        #print tick_to_next_circle
        if counter >=3 and time.time() - t1 < 5:
            bird_path.append(p)
            restart_counter = True
    if restart_counter == True:
        counter = 0
        restart_counter = False

    for bird in birds_to_remove:
        space.remove(bird.shape, bird.shape.body)
        birds.remove(bird)
    for pig in pigs_to_remove:
        space.remove(pig.shape, pig.shape.body)
        pigs.remove(pig)

    for line in static_lines:
        body = line.body
        pv1 = body.position + line.a.rotated(body.angle)
        pv2 = body.position + line.b.rotated(body.angle)
        p1 = to_pygame(pv1)
        p2 = to_pygame(pv2)
        pygame.draw.lines(screen, (150,150,150), False, [p1, p2])
    i = 0
    for pig in pigs:
        i += 1
        # print (i,pig.life)
        pig = pig.shape
        if pig.body.position.y < 0:
            pigs_to_remove.append(pig)

        p = to_pygame(pig.body.position)
        x, y = p
        x -= 22
        y -= 20
        screen.blit(pig_image, (x+7, y+4))
        pygame.draw.circle(screen, BLUE, p, int(pig.radius), 2)
    for column in columns:
        column.draw_poly('columns', screen)
    for beam in beams:
        beam.draw_poly('beams', screen)
    # Update physics
    dt = 1.0/60.0
    for x in range(1):
        space.step(dt)
    # Drawing second part of the sling
    rect = pygame.Rect(0, 0, 60, 200)
    screen.blit(sling_image, (120, 420), rect)
    bold_font = pygame.font.SysFont("arial", 30, bold=True)
    bold_font_bigger = pygame.font.SysFont("arial", 40, bold=True)
    failed_font = pygame.font.SysFont("arial", 50, bold=True)
    score_font = bold_font.render("SCORE", 1, (255, 255, 255))
    failed = failed_font.render("Level Failed", 1, (255, 255, 255))
    level_cleared = failed_font.render("Level Cleared!", 1, (255, 255, 255))
    number_font = bold_font.render(str(score), 1, (255, 255, 255))
    score_level_cleared = bold_font_bigger.render(str(score), 1, (255, 255, 255))
    arial = pygame.font.SysFont("arial", 35, bold=True)
    pause_font = arial.render("II", 1, (255, 255, 255))
    screen.blit(score_font, (1060, 90))
    if score == 0:
        screen.blit(number_font, (1100, 130))
    else:
        screen.blit(number_font, (1060, 130))
    screen.blit(pause_button, (10, 90))
    if game_state == 1:
        screen.blit(play_button, (500, 200))
        screen.blit(replay_button, (500, 300))
    if level.number_of_birds <= 0:
        game_state = 3
        rect = pygame.Rect(300, 0, 600, 800)
        pygame.draw.rect(screen, BLACK, rect)
        screen.blit(failed, (450, 90))
        screen.blit(pig_happy, (380, 120))
        screen.blit(replay_button, (520, 460))
    if level.number_of_birds > 0 and len(pigs) == 0:
        if bonus_score_once:
            score += (level.number_of_birds-1) * 10000
        bonus_score_once = False
        game_state = 4
        rect = pygame.Rect(300, 0, 600, 800)
        pygame.draw.rect(screen, BLACK, rect)
        screen.blit(level_cleared, (450, 90))
        if score >= level.one_star and score <= level.two_star:
            screen.blit(star1, (310, 190))
        if score >= level.two_star and score <= level.three_star:
            screen.blit(star1, (310, 190))
            screen.blit(star2, (500, 170))
        if score >= level.three_star:
            screen.blit(star1, (310, 190))
            screen.blit(star2, (500, 170))
            screen.blit(star3, (700, 200))
        screen.blit(score_level_cleared, (550, 400))
        screen.blit(replay_button, (510, 480))
        screen.blit(next_button, (620, 480))
    # Flip screen
    pygame.display.flip()
    clock.tick(50)
    pygame.display.set_caption("fps: " + str(clock.get_fps()))
