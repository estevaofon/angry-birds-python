import os
import sys
import math
import time
import pickle
current_path = os.getcwd()

import pymunk as pm
import pygame

from polygon import Polygon
from characters import Bird, Pig
from level import Level


pygame.init()
GRID_SIZE = 16
WOOD_STRENGTH_CONST = 300

screen = pygame.display.set_mode((1200, 650))
SCREENW, SCREENH = pygame.display.get_surface().get_size()

redbird = pygame.image.load(
    "../resources/images/red-bird3.png").convert_alpha()
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
bird_path = []
counter = 0
restart_counter = False
bonus_score_once = True
bold_font = pygame.font.SysFont("arial", 30, bold=True)
bold_font2 = pygame.font.SysFont("arial", 40, bold=True)
bold_font3 = pygame.font.SysFont("arial", 50, bold=True)
wall = False

# Static floor
static_body = pm.Body(body_type=pm.Body.STATIC)
static_lines = [pm.Segment(static_body, (0.0, 060.0), (1200.0, 060.0), 0.0)]
static_lines1 = [pm.Segment(static_body, (1200.0, 060.0), (1200.0, 800.0), 0.0)]
for line in static_lines:
    line.elasticity = 0.95
    line.friction = 1
    line.collision_type = 3
for line in static_lines1:
    line.elasticity = 0.95
    line.friction = 1
    line.collision_type = 3
space.add(static_lines)


def to_pygame(p):
    """Convert pymunk to pygame coordinates"""
    return int(p.x), int(-p.y+600)


def vector(p0, p1):
    """Return the vector of the points
    p0 = (xo,yo), p1 = (x1,y1)"""
    a = p1[0] - p0[0]
    b = p1[1] - p0[1]
    return (a, b)


def unit_vector(v):
    """Return the unit vector of the points
    v = (a,b)"""
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
    """Load the music"""
    song1 = '../resources/sounds/angry-birds.ogg'
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


def draw_level_cleared():
    """Draw level cleared"""
    global game_state
    global bonus_score_once
    global score
    level_cleared = bold_font3.render("Level Cleared!", 1, WHITE)
    score_level_cleared = bold_font2.render(str(score), 1, WHITE)
    if level.number_of_birds >= 0 and len(pigs) == 0:
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


def draw_level_failed():
    """Draw level failed"""
    global game_state
    failed = bold_font3.render("Level Failed", 1, WHITE)
    if level.number_of_birds <= 0 and time.time() - t2 > 5 and len(pigs) > 0:
        game_state = 3
        rect = pygame.Rect(300, 0, 600, 800)
        pygame.draw.rect(screen, BLACK, rect)
        screen.blit(failed, (450, 90))
        screen.blit(pig_happy, (380, 120))
        screen.blit(replay_button, (520, 460))


def restart():
    """Delete all objects of the level"""
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


def post_solve_bird_pig(arbiter, space, _):
    """Collision between bird and pig"""
    surface=screen
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


def post_solve_bird_wood(arbiter, space, _):
    """Collision between bird and wood"""
    poly_to_remove = []
    if arbiter.total_impulse.length > arbiter.shapes[1].body.mass * WOOD_STRENGTH_CONST:
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


def post_solve_pig_wood(arbiter, space, _):
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

def to_pygame(p):
    """Convert pymunk to pygame coordinates"""
    return int(p.x), int(-p.y + SCREENW // 2)
def to_pymunk(p):
    """pygame coords -> pymunk coords"""
    return int(p[0]), int(SCREENW // 2 - (p[1]))

# bird and pigs
space.add_collision_handler(0, 1).post_solve=post_solve_bird_pig
# bird and wood
space.add_collision_handler(0, 2).post_solve=post_solve_bird_wood
# pig and wood
space.add_collision_handler(1, 2).post_solve=post_solve_pig_wood
load_music()
level = Level(pigs, columns, beams, space)
level.number = 0
level.load_level()
bpressed = [0, 0, 0, 0, 0, 0]

# Dragging in editor mode
holding_body = None
holding_constraint_rot = None
holding_constraint_lin = None
mouse_body = pm.Body()
mouse_shape = pm.Circle(mouse_body,4)
space.add(mouse_body, mouse_shape)
editor_mode = False
saving_level = False
loading_level = False
curr_text = ''

while running:
    # Input handling
    for event in pygame.event.get():
        if (pygame.mouse.get_pressed()[0] and x_mouse > 100 and
                x_mouse < 250 and y_mouse > 370 and y_mouse < 550):
            mouse_pressed = True
        if event.type == pygame.QUIT:
            running = False
        if editor_mode:
            if not (loading_level or saving_level):
                space.step(0.000000001) # Update body positions without actually moving anything
                if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                    editor_mode = False
                    space.gravity = (0., -700)
                    # Exit editor mode
                if event.type == pygame.MOUSEBUTTONDOWN:
                    bpressed[event.button] = 1
                    if bpressed[1]:
                    
                        qpos = to_pymunk(event.pos)
                        for shape in [*[i.shape for i in [*pigs, *columns, *beams]]]:
                            #print(shape.point_query(qpos)[0])
                            if shape.point_query(qpos)[0] < 0:
                                holding_body = shape
                elif event.type == pygame.MOUSEBUTTONUP:
                    bpressed[event.button] = 0
                    if event.button == 1:
                        pass
                        if holding_body:
                            holding_body = None
                elif event.type == pygame.MOUSEMOTION:
                    #print(holding_body)
                    if holding_body:
                        #print('ss')
                        event.pos = list(event.pos)
                        event.pos[0] = event.pos[0] // GRID_SIZE * GRID_SIZE
                        event.pos[1] = event.pos[1] // GRID_SIZE * GRID_SIZE
                        event.pos = tuple(event.pos)
                        holding_body.body.position = to_pymunk(event.pos)
                elif event.type == pygame.KEYDOWN:
                    if holding_body:
                        if event.key == pygame.K_a:
                            # Rotate counterclockwise
                            holding_body.body.angle += math.pi / 4
                            # Snap angle
                            holding_body.body.angle = holding_body.body.angle // (math.pi / 4) * (math.pi / 4)
                        elif event.key == pygame.K_d:
                            # Rotate clockwise
                            holding_body.body.angle -= math.pi / 4 
                            # Snap angle
                            holding_body.body.angle = holding_body.body.angle // (math.pi / 4) * (math.pi / 4)
                    elif event.key == pygame.K_n:
                        # New level
                        restart()
                    elif event.key == pygame.K_m:
                        columns.append(Polygon(to_pymunk(pygame.mouse.get_pos()), 20, 85, space))

                    elif event.key == pygame.K_b:
                        pig = Pig(*to_pymunk(pygame.mouse.get_pos()), space)
                        pigs.append(pig)    
                    elif event.key == pygame.K_s:
                        saving_level = True
                    elif event.key == pygame.K_l:
                        loading_level = True
            elif (saving_level or loading_level) and event.type == pygame.KEYUP:
                # Add character to saving buffer
                # make sure the user hasn't typed anything evil
                assert pygame.key.name(event.key) not in ['/','.']
                if event.key == pygame.K_RETURN:
                    if saving_level:
                        saving_level = False
                        with open('../levels/%s.pickle' % curr_text, 'wb')  as f:
                            pickle.dump((beams, pigs, columns), f)
                    elif loading_level:
                        loading_level = False
                        with open('../levels/%s.pickle' % curr_text, 'rb')  as f:
                            restart()
                            beams, pigs, columns = pickle.load(f)
                            for i in [*beams, *pigs, *columns]:
                                space.add(i.body, i.shape)
                    curr_text = ''
                elif event.key == pygame.K_BACKSPACE:
                    curr_text = curr_text[:-1]
                if len(pygame.key.name(event.key)) > 1: # Dirty way of checking that the user hasn't typed a control character
                    continue                 
                curr_text += pygame.key.name(event.key)
                print(pygame.key.name(event.key))
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                # Toggle wall
                if wall:
                    space.remove(static_lines1)
                    wall = False
                else:
                    space.add(static_lines1)
                    wall = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                editor_mode = True
                space.gravity = 0., 0
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                if level.bool_space:
                    space.gravity = (0.0, -700.0)
                else:
                    space.gravity = (0.0, -10.0)
                level.bool_space = not level.bool_space
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:

                # Restart in the paused screen
                restart()
                level.load_level()
                game_state = 0
                bird_path = []
            if (event.type == pygame.MOUSEBUTTONUP and
                    event.button == 1 and mouse_pressed):
                # Release new bird
                mouse_pressed = False
                if level.number_of_birds > 0:
                    level.number_of_birds -= 1
                    t1 = time.time()*1000
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
                    if level.number_of_birds == 0:
                        t2 = time.time()
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if (x_mouse < 60 and y_mouse < 60):
                    game_state = 1
                if game_state == 1:
                    if x_mouse > 500 and y_mouse > 200 and y_mouse < 300:
                        # Resume in the paused screen
                        game_state = 0
                    if x_mouse > 500 and y_mouse > 300:
                        # Restart in the paused screen
                        restart()
                        level.load_level()
                        game_state = 0
                        bird_path = []
                if game_state == 3:
                    # Restart in the failed level screen
                    if x_mouse > 500 and x_mouse < 620 and y_mouse > 450:
                        restart()
                        level.load_level()
                        game_state = 0
                        bird_path = []
                        score = 0
                if game_state == 4:
                    # Build next level
                    if x_mouse > 610 and y_mouse > 450:
                        restart()
                        level.number += 1
                        game_state = 0
                        level.load_level()
                        score = 0
                        bird_path = []
                        bonus_score_once = True
                    if x_mouse < 610 and x_mouse > 500 and y_mouse > 450:
                        # Restart in the level cleared screen
                        restart()
                        level.load_level()
                        game_state = 0
                        bird_path = []
                        score = 0
    x_mouse, y_mouse = pygame.mouse.get_pos()
    # Draw background
    screen.fill((130, 200, 100))
    screen.blit(background2, (0, -50))
    # Draw first part of the sling
    rect = pygame.Rect(50, 0, 70, 220)
    screen.blit(sling_image, (138, 420), rect)
    # Draw the trail left behind
    for point in bird_path:
        pygame.draw.circle(screen, WHITE, point, 5, 0)
    # Draw the birds in the wait line
    if level.number_of_birds > 0:
        for i in range(level.number_of_birds-1):
            x = 100 - (i*35)
            screen.blit(redbird, (x, 508))
    # Draw sling behavior
    if mouse_pressed and level.number_of_birds > 0:
        sling_action()
    else:
        if time.time()*1000 - t1 > 300 and level.number_of_birds > 0:
            screen.blit(redbird, (130, 426))
        else:
            pygame.draw.line(screen, (0, 0, 0), (sling_x, sling_y-8),
                             (sling2_x, sling2_y-7), 5)
    birds_to_remove = []
    pigs_to_remove = []
    counter += 1
    # Draw birds
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
        if counter >= 3 and time.time() - t1 < 5:
            bird_path.append(p)
            restart_counter = True
    if restart_counter:
        counter = 0
        restart_counter = False
    # Remove birds and pigs
    for bird in birds_to_remove:
        space.remove(bird.shape, bird.shape.body)
        birds.remove(bird)
    for pig in pigs_to_remove:
        space.remove(pig.shape, pig.shape.body)
        pigs.remove(pig)
    # Draw static lines
    for line in static_lines:
        body = line.body
        pv1 = body.position + line.a.rotated(body.angle)
        pv2 = body.position + line.b.rotated(body.angle)
        p1 = to_pygame(pv1)
        p2 = to_pygame(pv2)
        pygame.draw.lines(screen, (150, 150, 150), False, [p1, p2])
    i = 0
    # Draw pigs
    for pig in pigs:
        i += 1
        # print (i,pig.life)
        pig = pig.shape
        if pig.body.position.y < 0:
            pigs_to_remove.append(pig)

        p = to_pygame(pig.body.position)
        x, y = p

        angle_degrees = math.degrees(pig.body.angle)
        img = pygame.transform.rotate(pig_image, angle_degrees)
        w,h = img.get_size()
        x -= w*0.5
        y -= h*0.5
        screen.blit(img, (x, y))
        pygame.draw.circle(screen, BLUE, p, int(pig.radius), 2)
    # Draw columns and Beams
    for column in columns:
        column.draw_poly('columns', screen)
    for beam in beams:
        beam.draw_poly('beams', screen)
    # Update physics
    dt = 1.0/50.0/2.
    for x in range(2):
        if not editor_mode: # No physics in editor mode
            space.step(dt) # make two updates per frame for better stability
    # Drawing second part of the sling
    rect = pygame.Rect(0, 0, 60, 200)
    screen.blit(sling_image, (120, 420), rect)
    # Draw score
    score_font = bold_font.render("SCORE", 1, WHITE)
    number_font = bold_font.render(str(score), 1, WHITE)
    screen.blit(score_font, (1060, 90))
    if score == 0:
        screen.blit(number_font, (1100, 130))
    else:
        screen.blit(number_font, (1060, 130))
    screen.blit(pause_button, (10, 10))
    # Pause option
    if game_state == 1:
        screen.blit(play_button, (500, 200))
        screen.blit(replay_button, (500, 300))
    if not editor_mode:
        draw_level_cleared()
        draw_level_failed()
    if loading_level:
        
        screen.blit( bold_font.render("Loading from %s.pickle" % curr_text , 1, RED) , (100,0))
    elif saving_level:
        screen.blit( bold_font.render("Saving as %s.pickle" % curr_text , 1, RED) , (100,0))
    elif editor_mode:
        screen.blit( bold_font.render("EDITOR MODE", 1, RED) , (100,0)) 
    
    pygame.display.flip()
    clock.tick(50)
    pygame.display.set_caption("fps: " + str(clock.get_fps()))
