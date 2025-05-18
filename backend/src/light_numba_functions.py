from numba import jit
import numpy as np

def warmup_numba_functions():
    print("warming up")
    bounce_on_rect_numba(1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0)
    move_to_target_numba(1.0,1.0,1.0,1.0,1.0,False)
    circle_circle_collide_numba(1.0,1.0,1.0,1.0,1.0,1.0)
    move_to_target_numba(1.0,1.0,1.0,1.0,1.0,True)
    circle_rect_collide_numba(1.0,1.0,1.0,1.0,1.0,1.0,1.0)


@jit(nopython=True)
def circle_rect_collide_numba(x, y, rx, ry, r_hw, r_hh, radius):
    closest_x = max(rx - r_hw, min(x, rx + r_hw))
    closest_y = max(ry - r_hh, min(y, ry + r_hh))
    x_dist = x - closest_x
    y_dist = y - closest_y
    center_dist = (x_dist**2 + y_dist**2)
    return center_dist <= radius * radius


@jit(nopython=True)
def circle_circle_collide_numba(x, y, cx, cy, radius, cradius):
    x_dist = abs(x - cx)
    y_dist = abs(y - cy)
    center_dist = (x_dist**2 + y_dist**2)
    radius_sum = radius + cradius

    return center_dist <= radius_sum * radius_sum # lets just compare to its squared to avoid using sqrt

@jit(nopython=True)
def bounce_on_rect_numba(
    x, y, radius, vx, vy,
    rect_x, rect_y, rect_hw, rect_hh
):
    # Clamp
    closest_x = max(rect_x - rect_hw, min(x, rect_x + rect_hw))
    closest_y = max(rect_y - rect_hh, min(y, rect_y + rect_hh))

    # Vector normal
    normal_x = x - closest_x
    normal_y = y - closest_y
    norm = (normal_x ** 2 + normal_y ** 2) ** 0.5

    if norm == 0:
        dx = x - rect_x
        dy = y - rect_y
        overlap_x = (rect_hw + radius) - abs(dx)
        overlap_y = (rect_hh + radius) - abs(dy)
        if overlap_x < overlap_y:
            normal_x = (dx > 0) - (dx < 0)
            normal_y = 0
        else:
            normal_x = 0
            normal_y = (dy > 0) - (dy < 0)
        prct_in = radius
    else:
        normal_x /= norm
        normal_y /= norm
        prct_in = radius - norm

    if prct_in > 0:
        x += normal_x * prct_in
        y += normal_y * prct_in

    dot = vx * normal_x + vy * normal_y
    new_vx = vx - 2 * dot * normal_x
    new_vy = vy - 2 * dot * normal_y

    return x, y, new_vx, new_vy

@jit(nopython=True)
def move_to_target_numba(target_x, target_y, x, y, wh, is_shooting=False):
    dx = target_x - x
    dy = target_y - y

    angle = np.arctan2(dy, dx)

    mag_sq = dx**2 + dy**2
    topSpeed = 1500
    if mag_sq >= wh * wh and not is_shooting:
        mag = np.sqrt(mag_sq) # lets use sqrt once we actually decided to move
        normDx = dx / mag
        normDy = dy / mag
        ds = (mag * 50) / wh
        speed = min(topSpeed, ds)
        velocity = (speed * normDx, speed * normDy)
    else:
        velocity = (0, 0)

    return velocity, angle
