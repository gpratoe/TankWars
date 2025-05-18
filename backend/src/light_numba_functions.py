from numba import jit

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


