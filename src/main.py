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
from characters import Bird, Pig
from polygon import Polygon


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
x_pymunk = 0
y_pymunk = 0
x_pygame_mouse = 0
y_pygame_mouse = 0
count = 0
mouse_pressed = False
t1 = 0
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
sling_x, sling_y = 135, 450
sling2_x, sling2_y = 160, 450

# walls
static_body = pm.Body()
static_lines = [pm.Segment(static_body, (0.0, 060.0), (1200.0, 060.0), 0.0)]
for line in static_lines:
    line.elasticity = 0.95
    line.friction = 1
    line.collision_type = 3
space.add(static_lines)


def flipy(y):
    """Convert chipmunk physics to pygame coordinates"""
    return -y+600


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
    global x_pymunk
    global y_pymunk
    global x_pygame_mouse
    global y_pygame_mouse
    # Getting mouse position
    x_pymunk, y_pymunk = from_pygame(Vec2d(pygame.mouse.get_pos()), screen)
    x_pygame_mouse, y_pygame_mouse = (x_pymunk, flipy(y_pymunk))
    y_pygame_mouse = y_pygame_mouse + 52
    # Fixing bird to the sling rope
    v = vector((sling_x, sling_y), (x_pygame_mouse, y_pygame_mouse))
    uv = unit_vector(v)
    uv1 = uv[0]
    uv2 = uv[1]
    mouse_distance = distance(sling_x, sling_y, x_pygame_mouse, y_pygame_mouse)
    pu = (uv1*rope_lenght+sling_x, uv2*rope_lenght+sling_y)
    bigger_rope = 102
    x_redbird = x_pygame_mouse - 20
    y_redbird = y_pygame_mouse - 20
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
    dy = y_pygame_mouse - sling_y
    dx = x_pygame_mouse - sling_x
    if dx == 0:
        dx = 0.00000000000001
    angle = math.atan((float(dy))/dx)


def level_1():
    """ Set up level 1"""
    pig1 = Pig(980, 100, space)
    pig2 = Pig(985, 185, space)
    pigs.append(pig1)
    pigs.append(pig2)
    p = (950, 80)
    columns.append(Polygon(p, 20, 85, space))
    p = (1010, 80)
    columns.append(Polygon(p, 20, 85, space))
    p = (980, 150)
    beams.append(Polygon(p, 85, 20, space))
    p = (950, 200)
    columns.append(Polygon(p, 20, 85, space))
    p = (1010, 200)
    columns.append(Polygon(p, 20, 85, space))
    p = (980, 240)
    beams.append(Polygon(p, 85, 20, space))


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
            pig.life -= 10
            pigs_to_remove.append(pig)
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


def post_solve_pig_wood(space, arbiter):
    """Collision between pig and wood"""
    pigs_to_remove = []
    if arbiter.total_impulse.length > 750:
        pig_shape, wood_shape = arbiter.shapes
        for pig in pigs:
            if pig_shape == pig.shape:
                pig.life -= 10
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
#load_music()
level_1()

while running:
    # Input handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
        if pygame.mouse.get_pressed()[0]:
            mouse_pressed = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            mouse_pressed = False
            t1 = time.time()
            xo = 154
            yo = 156
            if mouse_distance > rope_lenght:
                mouse_distance = rope_lenght
            if x_pygame_mouse < sling_x+5:
                bird = Bird(mouse_distance, angle, xo, yo, space)
                birds.append(bird)
            else:
                bird = Bird(-mouse_distance, angle, xo, yo, space)
                birds.append(bird)

    # Drawing background
    screen.fill((130, 200, 100))
    screen.blit(background2, (0, -50))
    rect = pygame.Rect(50, 0, 70, 220)
    screen.blit(sling_image, (138, 420), rect)
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
        pygame.draw.lines(screen, BLACK, False, [p1, p2])
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
    # Flip screen
    pygame.display.flip()
    clock.tick(50)
    pygame.display.set_caption("fps: " + str(clock.get_fps()))
