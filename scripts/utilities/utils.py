import math

def get_rect_offset(entity, size):
    return entity.rect.centerx//size[0], entity.rect.centery//size[1]

def get_offset(pos, size):
    return pos[0]//size[0], pos[1]//size[1]

def get_distance(a, b):
    return math.sqrt((b[0] - a[0])**2 + (b[1] - a[1])**2)
