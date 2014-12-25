import os
import sys
current_path = os.getcwd()
sys.path.insert(0, os.path.join( current_path, "../pymunk-4.0.0" ) )

import pygame
from pygame.locals import *
from pygame.color import *
import pymunk as pm
from pymunk import Vec2d
import math, sys, random
import pymunk.util as u
import math
from pymunk.pygame_util import from_pygame


COLLTYPE_DEFAULT = 0
COLLTYPE_MOUSE = 1

pygame.init()
screen = pygame.display.set_mode((1000, 600))
clock = pygame.time.Clock()
running = True
# Physics stuff
space = pm.Space()
space.gravity = (0.0, -900.0)

balls = []
polys = []
poly_points = []
ball_number = 0

# walls
static_body = pm.Body()
static_lines = [pm.Segment(static_body, (0.0, 130.0), (1000.0, 130.0), 0.0)
                ]
for line in static_lines:
    line.elasticity = 0.95
    line.friction = 0.7
space.add(static_lines)

ticks_to_next_ball = 10

def to_pygame(p):
    """Small hack to convert pymunk to pygame coordinates"""
    return int(p.x), int(-p.y+600)

def create_box(pos, size = 8, height=60, mass = 5.0):
    box_points = map(Vec2d, [(-size, -size), (-size, height), (size, height), (size, -size)])
    return create_poly(box_points, mass = mass, pos = pos)
def create_horizontal_box(pos, size = 8, width=80, mass = 5.0):
    box_points = map(Vec2d, [(-size, -size), (-size, size), (width, size), (width, -size)])
    return create_poly(box_points, mass = mass, pos = pos)
def create_poly(points, mass = 5.0, pos = (0,0)):
    moment = pm.moment_for_poly(mass,points, Vec2d(0,0))
    #moment = 1000
    body = pm.Body(mass, moment)
    body.position = Vec2d(pos)
    print body.position
    shape = pm.Poly(body, points, Vec2d(0,0))
    shape.friction = 0.5
    shape.collision_type = COLLTYPE_DEFAULT
    space.add(body, shape)
    return shape
def draw_poly(poly):
    body = poly.body
    ps = poly.get_vertices()
    ps.append(ps[0])
    ps = map(flipyv, ps)
    if u.is_clockwise(ps):
        color = THECOLORS["green"]
    else:
        color = THECOLORS["red"]
    pygame.draw.lines(screen, color, False, ps)
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
polys.append(create_box(pos = p))
p = (870, 150)
polys.append(create_box(pos = p))
p = (800, 220)
polys.append(create_horizontal_box(pos = p))
p = (800, 230)
polys.append(create_box(pos = p))
p = (870, 230)
polys.append(create_box(pos = p))
p = (800, 320)
polys.append(create_horizontal_box(pos = p))
def create_ball(distance, angle, x, y):
    #ticks_to_next_ball = 500
    mass = 10
    radius = 15
    inertia = pm.moment_for_circle(mass, 0, radius, (0, 0))
    body = pm.Body(mass, inertia)
    body.position = 140, 200
    #body.position = x, y
    power = distance * 110
    impulse = power * Vec2d(1,0)
    #angle = 1.0
    angle = -angle
    body.apply_impulse(impulse.rotated(angle))
    shape = pm.Circle(body, radius, (0, 0))
    shape.elasticity = 0.95
    space.add(body, shape)
    balls.append(shape)

#create_ball()
while running:
    sling_x, sling_y = 120, 410
    mx, my = pygame.mouse.get_pos()
    y = my - sling_y
    x = mx - sling_x
    try:
        angle = math.atan((float(y))/x)
    except:
        print "PASSED!"
        pass
    print 'angle'+str(angle)
    mouse_distance = distance(sling_x,sling_y,mx,my)
    print mouse_distance
    mx_pymunk, my_pymunk = from_pygame( Vec2d(pygame.mouse.get_pos()), screen )
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
                polys.append(create_horizontal_box(pos = p))
            else:
                create_ball(mouse_distance, angle, mx_pymunk, my_pymunk)
                #ticks_to_next_ball -= 1
                #if ticks_to_next_ball <= 0:
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            pass

    # Clear screen
    screen.fill(THECOLORS["white"])

    # Draw stuff
    balls_to_remove = []
    for ball in balls:
        if ball.body.position.y < 120: balls_to_remove.append(ball)

        p = to_pygame(ball.body.position)
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
        pygame.draw.lines(screen, THECOLORS["lightgray"], False, [p1,p2])
    for poly in polys:
        draw_poly(poly)
    sling = pygame.Rect(sling_x, sling_y, 10, 60)
    pygame.draw.rect(screen, (200,100,0), sling)
    # Update physics
    dt = 1.0/60.0
    for x in range(1):
        space.step(dt)

    # Flip screen
    pygame.display.flip()
    clock.tick(50)
    pygame.display.set_caption("fps: " + str(clock.get_fps()))
