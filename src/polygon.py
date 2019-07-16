import pymunk as pm
from pymunk import Vec2d
import pygame
import math


class Polygon():
    def __init__(self, pos, length, height, space = None, mass=5):
        moment = 1000
        body = pm.Body(mass, moment)
        body.position = Vec2d(pos)
        shape = pm.Poly.create_box(body, (length, height))
        shape.color = (0, 0, 255)
        shape.friction = 0.5
        self.mass = mass
        shape.collision_type = 2
        if space != None:
            space.add(body, shape)
        self.body = body
        self.space = space
        self.shape = shape
        self.length = length
        self.height = height
        if mass > 20:
            stone = pygame.image.load("../resources/images/stone.png").convert_alpha()
            rect = pygame.Rect(404, 128, 83, 20)
            self.beam_image = stone.subsurface(rect).copy()
            self.column_image = pygame.transform.rotate(stone.subsurface(rect).copy(), 90)
        elif mass > 3.0:
            wood = pygame.image.load("../resources/images/wood.png").convert_alpha()
            wood2 = pygame.image.load("../resources/images/wood2.png").convert_alpha()
            rect = pygame.Rect(251, 357, 86, 22)
            self.beam_image = wood.subsurface(rect).copy()
            rect = pygame.Rect(16, 252, 22, 84)
            self.column_image = wood2.subsurface(rect).copy()
        else:
            ice = pygame.image.load("../resources/images/ice.png").convert_alpha()
            rect = pygame.Rect(288, 347, 83, 20)
            self.beam_image = ice.subsurface(rect).copy()
            self.column_image = pygame.transform.rotate(ice.subsurface(rect).copy(), 90)
            

    def to_pygame(self, p):
        """Convert pymunk to pygame coordinates"""
        return int(p.x), int(-p.y+600)

    def draw_poly(self, element, screen):
        """Draw beams and columns"""
        poly = self.shape
        ps = poly.get_vertices()
        ps.append(ps[0])
        ps = map(self.to_pygame, ps)
        ps = list(ps)
        color = (255, 0, 0)
        pygame.draw.lines(screen, color, False, ps)
        if element == 'beams':
            p = poly.body.position
            p = Vec2d(self.to_pygame(p))
            angle_degrees = math.degrees(poly.body.angle) + 180
            rotated_logo_img = pygame.transform.rotate(self.beam_image,
                                                       angle_degrees)
            offset = Vec2d(rotated_logo_img.get_size()) / 2.
            p = p - offset
            np = p
            screen.blit(rotated_logo_img, (np.x, np.y))
        if element == 'columns':
            p = poly.body.position
            p = Vec2d(self.to_pygame(p))
            angle_degrees = math.degrees(poly.body.angle) + 180
            rotated_logo_img = pygame.transform.rotate(self.column_image,
                                                       angle_degrees)
            offset = Vec2d(rotated_logo_img.get_size()) / 2.
            p = p - offset
            np = p
            screen.blit(rotated_logo_img, (np.x, np.y))
    def __reduce__(self):
        return self.pickleKeywordargs, (self, (self.body.position, self.length, self.height, {'mass': self.mass}))
    def pickleKeywordargs(self, args, kwargs):
        return self.__class__(*args, **kwargs)