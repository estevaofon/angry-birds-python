import os
import sys
current_path = os.getcwd()
sys.path.insert(0, os.path.join(current_path, "../pymunk-4.0.0"))

import pygame
from pygame.locals import *
from pygame.color import *
import pymunk as pm
from pymunk import Vec2d
import math
import pymunk.util as u
from pymunk.pygame_util import from_pygame


COLLTYPE_DEFAULT = 0
COLLTYPE_MOUSE = 1

pygame.init()
screen = pygame.display.set_mode((1200, 650))
redbird=pygame.image.load("../resources/images/red-bird2.png").convert_alpha()
background = pygame.image.load("../resources/images/background.png").convert_alpha()
background1 = pygame.image.load("../resources/images/background1.jpg").convert_alpha()
background2 = pygame.image.load("../resources/images/background3.png").convert_alpha()
wood = pygame.image.load("../resources/images/wood.png").convert_alpha()
sling_image = pygame.image.load("../resources/images/sling-2.png").convert_alpha()
clock = pygame.time.Clock()
running = True
# Physics stuff
space = pm.Space()
space.gravity = (0.0, -900.0)
#pygame.mouse.set_visible(0)

balls = []
polys = []
poly_points = []
ball_number = 0

# walls
static_body = pm.Body()
static_lines = [pm.Segment(static_body, (0.0, 060.0), (1200.0, 060.0), 0.0)
                ]
for line in static_lines:
    line.elasticity = 0.95
    line.friction = 1
space.add(static_lines)

ticks_to_next_ball = 10


def vector(p0, p1):
    "(xo,yo), (x1,y1)"
    a = p1[0] - p0[0]
    b = p1[1] - p0[1]
    return (a, b)


def unit_vector(v):
    "(a,b)"
    h = ((v[0]**2)+(v[1]**2))**0.5
    ua = v[0] / h
    ub = v[1] / h
    return (ua, ub)
def to_pygame(p):
    """Small hack to convert pymunk to pygame coordinates"""
    return int(p.x), int(-p.y+600)

def to_pygame2(x,y):
    """Small hack to convert pymunk to pygame coordinates"""
    return int(x), int(-y+600)

def create_box(pos, size=8, height=60, mass=5.0):
    box_points = map(Vec2d, [(-size, -size), (-size, height),
                             (size, height), (size, -size)])
    return create_poly(box_points, mass=mass, pos=pos)


def create_horizontal_box(pos, size=8, width=80, mass=5.0):
    box_points = map(Vec2d, [(-size, -size), (-size, size),
                             (width, size), (width, -size)])
    return create_poly(box_points, mass=mass, pos=pos)


def create_poly(points, mass=5.0, pos=(0, 0)):
    moment = pm.moment_for_poly(mass, points, Vec2d(0, 0))
    # moment = 1000
    body = pm.Body(mass, moment)
    body.position = Vec2d(pos)
    print body.position
    shape = pm.Poly(body, points, Vec2d(0, 0))
    shape.friction = 0.5
    shape.collision_type = COLLTYPE_DEFAULT
    space.add(body, shape)
    return shape


def draw_poly(poly):
    ps = poly.get_vertices()
    ps.append(ps[0])
    ps = map(flipyv, ps)
    if u.is_clockwise(ps):
        color = THECOLORS["green"]
    else:
        color = THECOLORS["red"]
    pygame.draw.lines(screen, color, False, ps)
    #rect = pygame.Rect(250, 380, 86, 100)
    #screen.blit(wood, ps[0], rect)


def flipyv(v):
    h = 600
    return int(v.x), int(-v.y+h)


def distance(xo, yo, x, y):
    """
    distance between players
    """
    dx = x - xo
    dy = y - yo
    d = ((dx ** 2) + (dy ** 2)) ** 0.5
    return d

p = (800, 150)
polys.append(create_box(pos=p))
p = (870, 150)
polys.append(create_box(pos=p))
p = (800, 220)
polys.append(create_horizontal_box(pos=p))
p = (800, 230)
polys.append(create_box(pos=p))
p = (870, 230)
polys.append(create_box(pos=p))
p = (800, 320)
polys.append(create_horizontal_box(pos=p))


def create_ball(distance, angle, x, y):
    # ticks_to_next_ball = 500
    mass = 5
    radius = 16
    inertia = pm.moment_for_circle(mass, 0, radius, (0, 0))
    body = pm.Body(mass, inertia)
    #body.position = 140, 200
    body.position = x, y
    power = distance * 45
    impulse = power * Vec2d(1, 0)
    angle = -angle
    body.apply_impulse(impulse.rotated(angle))
    shape = pm.Circle(body, radius, (0, 0))
    shape.elasticity = 0.95
    shape.friction = 1
    space.add(body, shape)
    balls.append(shape)

while running:
    # Clear screen
    screen.fill(THECOLORS["white"])
    #screen.fill((130, 200, 100))
    #screen.blit(background2, (0,-50))
    sling_x, sling_y = 170, 410
    mx, my = pygame.mouse.get_pos()
    y = my - sling_y
    x = mx - sling_x
    sling = pygame.Rect(sling_x, sling_y, 20, 80)
    pygame.draw.rect(screen, (200, 100, 0), sling)
    rope_lenght = 110
    rect = pygame.Rect(100, 0, 70, 220)
    screen.blit(sling_image, (163, 360), rect)
    if x == 0:
        x = 0.00000000000001
    if y == 0:
        y = 0.00000000000001
    angle = math.atan((float(y))/x)
    print 'angle'+str(angle)
    mouse_distance = distance(sling_x, sling_y, mx, my)
    print 'mouse distance'+str(mouse_distance)
    x_pymunk, y_pymunk = from_pygame(Vec2d(pygame.mouse.get_pos()), screen)
    x_pygame, y_pygame = to_pygame2(x_pymunk, y_pymunk)
    y_pymunk = y_pymunk - 50
    x_pygame = x_pygame - 30
    y_pygame = y_pygame + 22
    xo_sprite = x_pygame + 30
    yo_sprite = y_pygame + 30
    pygame.draw.line(screen,(0,0,255), (sling_x, sling_y), (xo_sprite, yo_sprite), 3)
    v = vector((sling_x, sling_y), (xo_sprite, yo_sprite))
    uv = unit_vector(v)
    print 'uv'+str(uv)
    uv1 = uv[0]
    uv2 = uv[1]
    pu = (uv1*110+sling_x, uv2*110+sling_y)
    print 'pu'+str(pu)
    pygame.draw.line(screen,(255,0,0), (sling_x, sling_y), pu, 3)
    if mouse_distance > rope_lenght:
        pux , puy = pu
        pux = pux - 30
        puy = puy - 30
        pul = pux, puy
        screen.blit(redbird, pul)
        x_pymunk, y_pymunk = from_pygame(Vec2d(pul), screen)
        y_pymunk = y_pymunk - 80
        x_pymunk = x_pymunk + 20
    else:
        screen.blit(redbird, (x_pygame,y_pygame))

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            running = False
        elif event.type == KEYDOWN and event.key == K_p:
            pygame.image.save(screen, "bouncing_balls.png")
        elif event.type == MOUSEBUTTONDOWN and event.button == 1: # LMB
            start_time = pygame.time.get_ticks()
            if pygame.key.get_mods() & KMOD_SHIFT:
                p = flipyv(Vec2d(event.pos))
                polys.append(create_horizontal_box(pos=p))
            else:
                if mouse_distance > rope_lenght:
                    mouse_distance = rope_lenght
                if mx < sling_x+5:
                    create_ball(mouse_distance, angle, x_pymunk, y_pymunk)
                else:
                    create_ball(-mouse_distance, angle, x_pymunk, y_pymunk)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            pass

    # Draw stuff
    balls_to_remove = []
    for ball in balls:
        if ball.body.position.y < 0: balls_to_remove.append(ball)

        p = to_pygame(ball.body.position)
        x, y = p
        x = x - 30
        y = y - 40
        screen.blit(redbird, (x,y))
        pygame.draw.circle(screen, THECOLORS["blue"], p, int(ball.radius), 2)

    for ball in balls_to_remove:
        space.remove(ball, ball.body)
        balls.remove(ball)
    for line in static_lines:
        body = line.body
        pv1 = body.position + line.a.rotated(body.angle)
        pv2 = body.position + line.b.rotated(body.angle)
        p1 = to_pygame(pv1)
        p2 = to_pygame(pv2)
        pygame.draw.lines(screen, THECOLORS["lightgray"], False, [p1, p2])
    for poly in polys:
        draw_poly(poly)
    # Update physics
    dt = 1.0/60.0
    for x in range(1):
        space.step(dt)

    rect = pygame.Rect(0, 0, 60, 200)
    screen.blit(sling_image, (120, 360), rect)
    #screen.blit(sling_image, (115,340))
    # Flip screen
    pygame.display.flip()
    clock.tick(50)
    pygame.display.set_caption("fps: " + str(clock.get_fps()))
